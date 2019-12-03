/*
Copyright (c) 2019 BELL Computer-Netzwerke GmbH
Copyright (c) 2019 Robert Weiler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

package main

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path"
	"strconv"
	"strings"
	"time"
)

// AppConfig stores the application configuration once parsed by flags.
type AppConfig struct {
	XMCHost         string
	XMCPort         uint
	HTTPTimeout     uint
	InsecureHTTPS   bool
	XMCClientID     string
	XMCClientSecret string
	XMCUsername     string
	XMCPassword     string
	XMCQuery        string
}

// OAuth2Token stores the OAuth2 Token used for authentication.
type OAuth2Token struct {
	AccessToken string `json:"access_token"`
	TokenType   string `json:"token_type"`
}

// Definitions used within the code.
const (
	toolName      string = "XMC NBI GenericNbiClient.go"
	toolVersion   string = "0.6.0"
	httpUserAgent string = toolName + "/" + toolVersion
	jsonMimeType  string = "application/json"
)

// Error codes.
const (
	errSuccess      int = 0  // No error
	errUsage        int = 1  // Usage error
	errMissArg      int = 2  // Missing arguments
	errHTTPRequest  int = 10 // Error creating the HTTPS request
	errXMCConnect   int = 11 // Error connecting to XMC
	errHTTPResponse int = 12 // Error parsing the HTTPS response
	errHTTPOAuth    int = 20 // Error authenticating to XMC (OAuth)
)

// Variables used to pass data between functions.
var (
	Config    AppConfig
	NBIClient http.Client
	OAuth     OAuth2Token
)

// getEnvOrDefaultString returns the string value of the environment variable "name" or "defaultVal" if that variable does not exist.
func getEnvOrDefaultString(name string, defaultVal string) string {
	retVal := defaultVal
	envVal, ok := os.LookupEnv(name)
	if ok {
		retVal = envVal
	}
	return retVal
}

// getEnvOrDefaultUint returns the uint value of the environment variable "name" or "defaultVal" if that variable does not exist.
func getEnvOrDefaultUint(name string, defaultVal uint) uint {
	retVal := defaultVal
	envVal, ok := os.LookupEnv(name)
	if ok {
		intVal, _ := strconv.Atoi(envVal)
		retVal = uint(intVal)
	}
	return retVal
}

// getEnvOrDefaultBool returns the bool value of the environment variable "name" or "defaultVal" if that variable does not exist.
func getEnvOrDefaultBool(name string, defaultVal bool) bool {
	retVal := defaultVal
	envVal, ok := os.LookupEnv(name)
	if ok {
		retVal, _ = strconv.ParseBool(envVal)
	}
	return retVal
}

// retrieveOAuthToken retrieves a usable OAuth token from XMC.
func retrieveOAuthToken() bool {
	tokenURL := "https://" + Config.XMCHost + ":" + fmt.Sprint(Config.XMCPort) + "/oauth/token/access-token?grant_type=client_credentials"

	req, reqErr := http.NewRequest(http.MethodPost, tokenURL, nil)
	if reqErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not create HTTPS request: %s\n", reqErr)
		return false
	}
	req.Header.Set("User-Agent", httpUserAgent)
	req.Header.Set("Accept", jsonMimeType)
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.SetBasicAuth(Config.XMCClientID, Config.XMCClientSecret)

	res, resErr := NBIClient.Do(req)
	if resErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not connect to XMC: %s\n", resErr)
		return false
	}
	if res.StatusCode != 200 {
		fmt.Fprintf(os.Stderr, "Error: Got status code %d instead of 200\n", res.StatusCode)
		return false
	}
	defer res.Body.Close()

	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		fmt.Fprintf(os.Stderr, "Error: Content-Type %s returned instead of %s\n", resContentType, jsonMimeType)
		return false
	}

	xmcToken, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not read server response: %s\n", readErr)
		return false
	}

	jsonErr := json.Unmarshal(xmcToken, &OAuth)
	if jsonErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not read server response: %s\n", jsonErr)
		return false
	}

	return true
}

func main() {
	// Variables used for storing options that are not pushed to Config.
	var xmcQuery string
	var printVersion bool
	var useOAuth bool

	// Parse all valid CLI options into variables.
	flag.StringVar(&Config.XMCHost, "host", getEnvOrDefaultString("XMCHOST", ""), "XMC Hostname / IP")
	flag.UintVar(&Config.XMCPort, "port", getEnvOrDefaultUint("XMCPORT", 8443), "HTTP port where XMC is listening")
	flag.UintVar(&Config.HTTPTimeout, "httptimeout", getEnvOrDefaultUint("XMCTIMEOUT", 5), "Timeout for HTTP(S) connections")
	flag.BoolVar(&Config.InsecureHTTPS, "insecurehttps", getEnvOrDefaultBool("XMCINSECURE", false), "Do not validate HTTPS certificates")
	flag.StringVar(&Config.XMCClientID, "clientid", getEnvOrDefaultString("XMCCLIENTID", ""), "Client ID for OAuth2")
	flag.StringVar(&Config.XMCClientSecret, "clientsecret", getEnvOrDefaultString("XMCCLIENTSECRET", ""), "Client Secret for OAuth2")
	flag.StringVar(&Config.XMCUsername, "username", getEnvOrDefaultString("XMCUSERNAME", "admin"), "Username for HTTP auth")
	flag.StringVar(&Config.XMCPassword, "password", getEnvOrDefaultString("XMCPASSWORD", ""), "Password for HTTP auth")
	flag.StringVar(&xmcQuery, "query", getEnvOrDefaultString("XMCQUERY", "query { network { devices { up ip sysName nickName } } }"), "GraphQL query to send to XMC")
	flag.BoolVar(&printVersion, "version", false, "Print version information and exit")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "This tool queries the XMC API and prints the raw reply (JSON) to stdout.\n")
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Usage: %s [options]\n", path.Base(os.Args[0]))
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Available options:\n")
		flag.PrintDefaults()
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "OAuth2 will be preferred over username/password.\n")
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "All options that take a value can be set via environment variables:\n")
		fmt.Fprintf(os.Stderr, "  XMCHOST          -->  -host\n")
		fmt.Fprintf(os.Stderr, "  XMCPORT          -->  -port\n")
		fmt.Fprintf(os.Stderr, "  XMCINSECURE      -->  -insecurehttps\n")
		fmt.Fprintf(os.Stderr, "  XMCTIMEOUT       -->  -httptimeout\n")
		fmt.Fprintf(os.Stderr, "  XMCCLIENTID      -->  -clientid\n")
		fmt.Fprintf(os.Stderr, "  XMCCLIENTSECRET  -->  -clientsecret\n")
		fmt.Fprintf(os.Stderr, "  XMCUSERNAME      -->  -username\n")
		fmt.Fprintf(os.Stderr, "  XMCPASSWORD      -->  -password\n")
		fmt.Fprintf(os.Stderr, "  XMCQUERY         -->  -query\n")
		os.Exit(errUsage)
	}
	flag.Parse()

	// Print version information and exit.
	if printVersion {
		fmt.Println(httpUserAgent)
		os.Exit(errSuccess)
	}

	// Check that the option "host" has been set.
	if Config.XMCHost == "" {
		fmt.Fprintln(os.Stderr, "Variable -host must be defined. Use -h to get help.")
		os.Exit(errMissArg)
	}

	// Create an HTTP client to talk to XMC.
	httpTransport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: Config.InsecureHTTPS},
	}
	NBIClient = http.Client{
		Transport: httpTransport,
		Timeout:   time.Second * time.Duration(Config.HTTPTimeout),
	}

	// Try to get an OAuth token if we have OAuth authentication data.
	useOAuth = false
	if Config.XMCClientID != "" && Config.XMCClientSecret != "" {
		if retrieveOAuthToken() != true {
			os.Exit(errHTTPOAuth)
		}
		useOAuth = true
	}

	// Generate an actual HTTP request.
	apiURL := "https://" + Config.XMCHost + ":" + fmt.Sprint(Config.XMCPort) + "/nbi/graphql"
	jsonQuery, jsonQueryErr := json.Marshal(map[string]string{"query": xmcQuery})
	if jsonQueryErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not encode query into JSON: %s", jsonQueryErr)
		os.Exit(errHTTPRequest)
	}
	req, reqErr := http.NewRequest(http.MethodPost, apiURL, bytes.NewBuffer(jsonQuery))
	if reqErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not create HTTPS request: %s\n", reqErr)
		os.Exit(errHTTPRequest)
	}
	req.Header.Set("User-Agent", httpUserAgent)
	req.Header.Set("Cache-Control", "no-cache")
	req.Header.Set("Content-Type", jsonMimeType)
	req.Header.Set("Accept", jsonMimeType)
	if useOAuth {
		req.Header.Set("Authorization", "Bearer "+OAuth.AccessToken)
	} else {
		req.SetBasicAuth(Config.XMCUsername, Config.XMCPassword)
	}

	// Try to get a result from the API.
	res, getErr := NBIClient.Do(req)
	if getErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not connect to XMC: %s\n", getErr)
		os.Exit(errXMCConnect)
	}
	if res.StatusCode != 200 {
		fmt.Fprintf(os.Stderr, "Error: Got status code %d instead of 200\n", res.StatusCode)
		os.Exit(errXMCConnect)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		fmt.Fprintf(os.Stderr, "Error: Content-Type %s returned instead of %s\n", resContentType, jsonMimeType)
		os.Exit(errHTTPResponse)
	}

	// Read and print the body of the HTTP response to stdout.
	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not read server response: %s\n", readErr)
		os.Exit(errHTTPResponse)
	}
	fmt.Println(string(body))

	// Indicate a successful execution of the program.
	os.Exit(errSuccess)
}
