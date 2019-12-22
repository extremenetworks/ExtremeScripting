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
	"encoding/base64"
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
	accessScheme    string
	XMCHost         string
	XMCPort         uint
	HTTPTimeout     uint
	NoHTTPS         bool
	InsecureHTTPS   bool
	XMCClientID     string
	XMCClientSecret string
	XMCUsername     string
	XMCPassword     string
	XMCQuery        string
	UseOAuth        bool
	PrintVersion    bool
}

// OAuth2Token stores the OAuth2 Token used for authentication.
type OAuth2Token struct {
	TokenType     string `json:"token_type"`
	AccessToken   string `json:"access_token"`
	TokenElements OAuth2TokenElements
}

// OAuth2TokenElements stores decoded information contained in a valid OAuth2 token.
type OAuth2TokenElements struct {
	Header    OAuth2HeaderElements
	Payload   OAuth2PayloadElements
	Signature []byte
}

// OAuth2HeaderElements stores decoded information contained in the header part of an OAuth2 token.
type OAuth2HeaderElements struct {
	Algorithm string `json:"alg"`
}

// OAuth2PayloadElements stores decoded information contained in the payload part of an OAuth2 token.
type OAuth2PayloadElements struct {
	Issuer           string    `json:"iss,omitempty"`
	Subject          string    `json:"sub,omitempty"`
	JWTID            string    `json:"jti,omitempty"`
	Roles            []string  `json:"roles,omitempty"`
	IsuedAtUnixfmt   int64     `json:"iat,omitempty"`
	NotBeforeUnixfmt int64     `json:"nbf,omitempty"`
	ExpiresAtUnixfmt int64     `json:"exp,omitempty"`
	IssuedAt         time.Time `json:"-"`
	NotBefore        time.Time `json:"-"`
	ExpiresAt        time.Time `json:"-"`
	LongLived        bool      `json:"longLived,omitempty"`
}

// Definitions used within the code.
const (
	toolName      string = "XMC NBI GenericNbiClient.go"
	toolVersion   string = "0.8.0"
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
func retrieveOAuthToken() (OAuth2Token, error) {
	var tokenData OAuth2Token

	tokenURL := Config.accessScheme + "://" + Config.XMCHost + ":" + fmt.Sprint(Config.XMCPort) + "/oauth/token/access-token?grant_type=client_credentials"

	// Generate an actual HTTP request.
	req, reqErr := http.NewRequest(http.MethodPost, tokenURL, nil)
	if reqErr != nil {
		return tokenData, fmt.Errorf("Could not create HTTPS request: %s", reqErr)
	}
	req.Header.Set("User-Agent", httpUserAgent)
	req.Header.Set("Cache-Control", "no-cache")
	req.Header.Set("Accept", jsonMimeType)
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.SetBasicAuth(Config.XMCClientID, Config.XMCClientSecret)

	// Try to get a result from the API.
	res, resErr := NBIClient.Do(req)
	if resErr != nil {
		return tokenData, fmt.Errorf("Could not connect to XMC: %s", resErr)
	}
	if res.StatusCode != 200 {
		return tokenData, fmt.Errorf("Got status code %d instead of 200", res.StatusCode)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return tokenData, fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	// Read and parse the body of the HTTP response.
	xmcToken, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		return tokenData, fmt.Errorf("Could not read server response: %s", readErr)
	}
	jsonErr := json.Unmarshal(xmcToken, &tokenData)
	if jsonErr != nil {
		return tokenData, fmt.Errorf("Could not read server response: %s", jsonErr)
	}

	return tokenData, nil
}

// decodeOAuthToken decodes the JSON Web Token used for OAuth.
func decodeOAuthToken(accessToken string) (OAuth2TokenElements, error) {
	var tokenElements OAuth2TokenElements

	// Seperate the parts of the token.
	tokenParts := strings.Split(accessToken, ".")

	// Decode each part.
	header, headerErr := decodeOAuthHeader(tokenParts[0])
	if headerErr != nil {
		return tokenElements, headerErr
	}
	tokenElements.Header = header
	payload, payloadErr := decodeOAuthPayload(tokenParts[1])
	if payloadErr != nil {
		return tokenElements, payloadErr
	}
	tokenElements.Payload = payload
	signature, signatureErr := base64.RawURLEncoding.DecodeString(tokenParts[2])
	if signatureErr != nil {
		return tokenElements, signatureErr
	}
	tokenElements.Signature = signature

	return tokenElements, nil
}

// decodeOAuthPayload decodes the header part of the JSON Web Token used for OAuth
func decodeOAuthHeader(header64 string) (OAuth2HeaderElements, error) {
	var headerElements OAuth2HeaderElements

	// Decode the base64url encoded JSON.
	headerData, headerErr := base64.RawURLEncoding.DecodeString(header64)
	if headerErr != nil {
		return headerElements, headerErr
	}

	// Parse the JSON into our struct.
	decodeErr := json.Unmarshal(headerData, &headerElements)
	if decodeErr != nil {
		return headerElements, decodeErr
	}

	return headerElements, nil
}

// decodeOAuthPayload decodes the payload part of the JSON Web Token used for OAuth
func decodeOAuthPayload(payload64 string) (OAuth2PayloadElements, error) {
	var payloadElements OAuth2PayloadElements

	// Decode the base64url encoded JSON.
	payloadData, payloadErr := base64.RawURLEncoding.DecodeString(payload64)
	if payloadErr != nil {
		return payloadElements, payloadErr
	}

	// Parse the JSON into our struct.
	decodeErr := json.Unmarshal(payloadData, &payloadElements)
	if decodeErr != nil {
		return payloadElements, decodeErr
	}

	// Transform UNIX timestamps into time.Time objects.
	payloadElements.IssuedAt = time.Unix(payloadElements.IsuedAtUnixfmt, 0)
	payloadElements.NotBefore = time.Unix(payloadElements.NotBeforeUnixfmt, 0)
	payloadElements.ExpiresAt = time.Unix(payloadElements.ExpiresAtUnixfmt, 0)

	return payloadElements, nil
}

// retrieveAPIResult sends the given query to XMC and returns the raw JSON result, an error code for os.Exit() and the actual error.
func retrieveAPIResult(query string) (string, int, error) {
	apiURL := Config.accessScheme + "://" + Config.XMCHost + ":" + fmt.Sprint(Config.XMCPort) + "/nbi/graphql"

	// Generate an actual HTTP request.
	jsonQuery, jsonQueryErr := json.Marshal(map[string]string{"query": query})
	if jsonQueryErr != nil {
		return "", errHTTPRequest, fmt.Errorf("Could not encode query into JSON: %s", jsonQueryErr)
	}
	req, reqErr := http.NewRequest(http.MethodPost, apiURL, bytes.NewBuffer(jsonQuery))
	if reqErr != nil {
		return "", errHTTPRequest, fmt.Errorf("Could not create HTTPS request: %s", reqErr)
	}
	req.Header.Set("User-Agent", httpUserAgent)
	req.Header.Set("Cache-Control", "no-cache")
	req.Header.Set("Content-Type", jsonMimeType)
	req.Header.Set("Accept", jsonMimeType)
	if Config.UseOAuth {
		req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", OAuth.AccessToken))
	} else {
		req.SetBasicAuth(Config.XMCUsername, Config.XMCPassword)
	}

	// Try to get a result from the API.
	res, resErr := NBIClient.Do(req)
	if resErr != nil {
		return "", errXMCConnect, fmt.Errorf("Could not connect to XMC: %s", resErr)
	}
	if res.StatusCode != 200 {
		return "", errXMCConnect, fmt.Errorf("Got status code %d instead of 200", res.StatusCode)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return "", errHTTPResponse, fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	// Read the body of the HTTP response.
	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		return "", errHTTPResponse, fmt.Errorf("Could not read server response: %s", readErr)
	}

	return string(body), errSuccess, nil
}

// parseCLIOptions parses all options passed by env or CLI into the Config variable.
func parseCLIOptions() {
	flag.StringVar(&Config.XMCHost, "host", getEnvOrDefaultString("XMCHOST", ""), "XMC Hostname / IP")
	flag.UintVar(&Config.XMCPort, "port", getEnvOrDefaultUint("XMCPORT", 8443), "HTTP port where XMC is listening")
	flag.UintVar(&Config.HTTPTimeout, "httptimeout", getEnvOrDefaultUint("XMCTIMEOUT", 5), "Timeout for HTTP(S) connections")
	flag.BoolVar(&Config.NoHTTPS, "nohttps", getEnvOrDefaultBool("XMCNOHTTPS", false), "Use HTTP instead of HTTPS")
	flag.BoolVar(&Config.InsecureHTTPS, "insecurehttps", getEnvOrDefaultBool("XMCINSECURE", false), "Do not validate HTTPS certificates")
	flag.StringVar(&Config.XMCClientID, "clientid", getEnvOrDefaultString("XMCCLIENTID", ""), "Client ID for OAuth2")
	flag.StringVar(&Config.XMCClientSecret, "clientsecret", getEnvOrDefaultString("XMCCLIENTSECRET", ""), "Client Secret for OAuth2")
	flag.StringVar(&Config.XMCUsername, "username", getEnvOrDefaultString("XMCUSERNAME", "admin"), "Username for HTTP auth")
	flag.StringVar(&Config.XMCPassword, "password", getEnvOrDefaultString("XMCPASSWORD", ""), "Password for HTTP auth")
	flag.StringVar(&Config.XMCQuery, "query", getEnvOrDefaultString("XMCQUERY", "query { network { devices { up ip sysName nickName } } }"), "GraphQL query to send to XMC")
	flag.BoolVar(&Config.PrintVersion, "version", false, "Print version information and exit")
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
		fmt.Fprintf(os.Stderr, "  XMCNOHTTPS       -->  -nohttps\n")
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

	if Config.NoHTTPS {
		Config.accessScheme = "http"
	} else {
		Config.accessScheme = "https"
	}
}

// main ties everything together.
func main() {
	// Parse all valid CLI options into variables.
	parseCLIOptions()

	// Print version information and exit.
	if Config.PrintVersion {
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
	Config.UseOAuth = false
	if Config.XMCClientID != "" && Config.XMCClientSecret != "" {
		tokenData, oAuthErr := retrieveOAuthToken()
		if oAuthErr != nil {
			fmt.Fprintf(os.Stderr, "Could not retrieve OAuth token: %s\n", oAuthErr)
			os.Exit(errHTTPOAuth)
		}
		OAuth = tokenData
		tokenElements, decodeErr := decodeOAuthToken(OAuth.AccessToken)
		if decodeErr != nil {
			fmt.Fprintf(os.Stderr, "Could not decode OAuth token: %s\n", decodeErr)
			os.Exit(errHTTPOAuth)
		}
		OAuth.TokenElements = tokenElements
		Config.UseOAuth = true
	}

	// Call the API and print the result.
	apiResult, exitCode, apiError := retrieveAPIResult(Config.XMCQuery)
	if apiError != nil {
		fmt.Fprintf(os.Stderr, "Could not retrieve API result: %s\n", apiError)
	} else {
		fmt.Println(string(apiResult))
	}

	// Exit with an appropriate exit code.
	os.Exit(exitCode)
}
