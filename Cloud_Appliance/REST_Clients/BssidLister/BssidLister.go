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
	"strings"
	"time"

	godotenv "github.com/joho/godotenv"
	envordef "gitlab.com/rbrt-weiler/go-module-envordef"
)

// AppConfig stores the application configuration once parsed by flags.
type appConfig struct {
	XCAHost      string
	XCAPort      uint
	HTTPTimeout  uint
	XCAUserID    string
	XCASecret    string
	PrintVersion bool
}

type oAuthRequest struct {
	GrantType string `json:"grantType"`
	UserID    string `json:"userId"`
	Password  string `json:"password"`
	Scope     string `json:"scope"`
}

type oAuthToken struct {
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	ExpiresIn    int    `json:"expires_in"`
	IdleTimeout  int    `json:"idle_timeout"`
	RefreshToken string `json:"refresh_token"`
	AdminRole    string `json:"adminRole"`
	TokenHeader  struct {
		KID      string `json:"kid"`
		Type     string `json:"typ"`
		Algorith string `json:"alg"`
	}
	TokenPayload struct {
		JWTID            string    `json:"jti"`
		Subject          string    `json:"sub"`
		Issuer           string    `json:"iss"`
		ExtremeRole      string    `json:"extreme_role"`
		ExpiresAt        time.Time `json:"-"`
		ExpiresAtUnixfmt int64     `json:"exp"`
	}
	TokenSignature []byte
}

type apResultSet []struct {
	SerialNumber string `json:"serialNumber"`
	CanEdit      bool   `json:"canEdit"`
	CanDelete    bool   `json:"canDelete"`
	Proxied      string `json:"proxied"`
	Radios       []struct {
		RadioIndex int `json:"radioIndex"`
		Wlan       []struct {
			Bssid string `json:"bssid"`
			Ssid  string `json:"ssid"`
		} `json:"wlan"`
	} `json:"radios"`
}

// Definitions used within the code.
const (
	toolName     string = "BssidLister.go"
	toolVersion  string = "0.1.1"
	toolID       string = toolName + "/" + toolVersion
	toolURL      string = "https://gitlab.com/rbrt-weiler/xca-rest-bssidlister-go"
	envFileName  string = ".xcaenv"
	jsonMimeType string = "application/json"
)

// Error codes.
const (
	errSuccess int = 0  // No error
	errUsage   int = 1  // Usage error
	errXCAAuth int = 10 // Authentication error
	errAPICall int = 11 // API Call error
)

// Variables used to pass data between functions.
var (
	config   appConfig
	xcaToken oAuthToken
	apResult apResultSet
)

func xcaAuthentication() error {
	// Empty token structure to start with.
	var tokenData oAuthToken

	var tokenURL string = fmt.Sprintf("https://%s:%d/management/v1/oauth2/token", config.XCAHost, config.XCAPort)
	httpTransport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	httpClient := &http.Client{
		Timeout:   time.Second * time.Duration(config.HTTPTimeout),
		Transport: httpTransport,
	}

	var tokenRequest oAuthRequest
	tokenRequest.GrantType = "password"
	tokenRequest.UserID = config.XCAUserID
	tokenRequest.Password = config.XCASecret
	tokenRequest.Scope = ""

	// Generate an actual HTTP request.
	payload, _ := json.Marshal(tokenRequest)
	req, reqErr := http.NewRequest(http.MethodPost, tokenURL, bytes.NewBuffer(payload))
	if reqErr != nil {
		return fmt.Errorf("could not create HTTP(S) request: %s", reqErr)
	}
	req.Header.Set("User-Agent", toolID)
	req.Header.Set("Cache-Control", "no-cache")
	req.Header.Set("Accept", jsonMimeType)
	req.Header.Set("Content-Type", jsonMimeType)

	// Try to get a result from the API.
	res, resErr := httpClient.Do(req)
	if resErr != nil {
		return fmt.Errorf("could not connect to XMC: %s", resErr)
	}
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("got status code %d instead of %d", res.StatusCode, http.StatusOK)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	// Read and parse the body of the HTTP response.
	body, bodyErr := ioutil.ReadAll(res.Body)
	if bodyErr != nil {
		return fmt.Errorf("could not read server response: %s", bodyErr)
	}
	jsonErr := json.Unmarshal(body, &tokenData)
	if jsonErr != nil {
		return fmt.Errorf("could not read server response: %s", jsonErr)
	}

	tokenFields := strings.Split(tokenData.AccessToken, ".")
	tokenHeader, _ := base64.RawURLEncoding.DecodeString(tokenFields[0])
	if headerErr := json.Unmarshal(tokenHeader, &tokenData.TokenHeader); headerErr != nil {
		fmt.Printf("Could not decode header: %s\n", headerErr)
	}
	tokenPayload, _ := base64.RawURLEncoding.DecodeString(tokenFields[1])
	if payloadErr := json.Unmarshal(tokenPayload, &tokenData.TokenPayload); payloadErr != nil {
		fmt.Printf("Could not decode payload: %s\n", payloadErr)
	}
	tokenData.TokenPayload.ExpiresAt = time.Unix(tokenData.TokenPayload.ExpiresAtUnixfmt, 0)
	tokenSignature, _ := base64.RawURLEncoding.DecodeString(tokenFields[2])
	tokenData.TokenSignature = tokenSignature

	xcaToken = tokenData

	return nil
}

func getSSIDs() error {
	var apURL string = fmt.Sprintf("https://%s:%d/management/v1/aps", config.XCAHost, config.XCAPort)
	httpTransport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	httpClient := &http.Client{
		Timeout:   time.Second * time.Duration(config.HTTPTimeout),
		Transport: httpTransport,
	}

	req, reqErr := http.NewRequest(http.MethodGet, apURL, nil)
	if reqErr != nil {
		return fmt.Errorf("could not create HTTP(S) request: %s", reqErr)
	}
	req.Header.Set("User-Agent", toolID)
	req.Header.Set("Cache-Control", "no-cache")
	req.Header.Set("Accept", jsonMimeType)
	//req.Header.Set("Content-Type", jsonMimeType)
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", xcaToken.AccessToken))
	query := req.URL.Query()
	query.Add("inventory", "true")
	req.URL.RawQuery = query.Encode()

	// Try to get a result from the API.
	res, resErr := httpClient.Do(req)
	if resErr != nil {
		return fmt.Errorf("could not connect to XCA: %s", resErr)
	}
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("got status code %d instead of %d", res.StatusCode, http.StatusOK)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	// Read and parse the body of the HTTP response.
	body, bodyErr := ioutil.ReadAll(res.Body)
	if bodyErr != nil {
		return fmt.Errorf("could not read server response: %s", bodyErr)
	}
	jsonErr := json.Unmarshal(body, &apResult)
	if jsonErr != nil {
		return fmt.Errorf("could not read server response: %s", jsonErr)
	}

	return nil
}

// parseCLIOptions parses all options passed by env or CLI into the Config variable.
func parseCLIOptions() {
	flag.StringVar(&config.XCAHost, "host", envordef.StringVal("XCAHOST", ""), "XCA Hostname / IP")
	flag.UintVar(&config.XCAPort, "port", envordef.UintVal("XCAPORT", 5825), "HTTP port where XCA is listening")
	flag.UintVar(&config.HTTPTimeout, "timeout", envordef.UintVal("XCATIMEOUT", 5), "Timeout for HTTP(S) connections")
	flag.StringVar(&config.XCAUserID, "userid", envordef.StringVal("XCAUSERID", ""), "Client ID for authentication")
	flag.StringVar(&config.XCASecret, "secret", envordef.StringVal("XCASECRET", ""), "Client Secret for authentication")
	flag.BoolVar(&config.PrintVersion, "version", false, "Print version information and exit")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "%s\n", toolID)
		fmt.Fprintf(os.Stderr, "%s\n", toolURL)
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "This tool queries the XCA API, fetches the list of Access Points and\n")
		fmt.Fprintf(os.Stderr, "associated (B)SSIDs and prints CSV to stdout.\n")
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Usage: %s [options]\n", path.Base(os.Args[0]))
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Available options:\n")
		flag.PrintDefaults()
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "All options that take a value can be set via environment variables:\n")
		fmt.Fprintf(os.Stderr, "  XCAHOST           -->  -host\n")
		fmt.Fprintf(os.Stderr, "  XCAPORT           -->  -port\n")
		fmt.Fprintf(os.Stderr, "  XCATIMEOUT        -->  -timeout\n")
		fmt.Fprintf(os.Stderr, "  XCAUSERID         -->  -userid\n")
		fmt.Fprintf(os.Stderr, "  XCASECRET         -->  -secret\n")
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Environment variables can also be configured via a file called %s,\n", envFileName)
		fmt.Fprintf(os.Stderr, "located in the current directory or in the home directory of the current\n")
		fmt.Fprintf(os.Stderr, "user.\n")
		os.Exit(errUsage)
	}
	flag.Parse()
}

// init loads environment files if available.
func init() {
	// if envFileName exists in the current directory, load it
	localEnvFile := fmt.Sprintf("./%s", envFileName)
	if _, localEnvErr := os.Stat(localEnvFile); localEnvErr == nil {
		if loadErr := godotenv.Load(localEnvFile); loadErr != nil {
			fmt.Fprintf(os.Stderr, "Could not load env file <%s>: %s", localEnvFile, loadErr)
		}
	}

	// if envFileName exists in the user's home directory, load it
	if homeDir, homeErr := os.UserHomeDir(); homeErr == nil {
		homeEnvFile := fmt.Sprintf("%s/%s", homeDir, ".xmcenv")
		if _, homeEnvErr := os.Stat(homeEnvFile); homeEnvErr == nil {
			if loadErr := godotenv.Load(homeEnvFile); loadErr != nil {
				fmt.Fprintf(os.Stderr, "Could not load env file <%s>: %s", homeEnvFile, loadErr)
			}
		}
	}
}

// main ties everything together.
func main() {
	parseCLIOptions()

	// Print version information and exit.
	if config.PrintVersion {
		fmt.Println(toolID)
		os.Exit(errSuccess)
	}

	if authErr := xcaAuthentication(); authErr != nil {
		fmt.Printf("Could not authenticate: %s\n", authErr)
		os.Exit(errXCAAuth)
	}

	if ssidErr := getSSIDs(); ssidErr != nil {
		fmt.Printf("Could not obtain AP list: %s\n", ssidErr)
		os.Exit(errAPICall)
	}

	fmt.Printf("\"%s\",\"%s\",\"%s\",\"%s\"\n", "serial", "radio", "bssid", "ssid")
	for _, singleAP := range apResult {
		for _, radio := range singleAP.Radios {
			for _, wlan := range radio.Wlan {
				fmt.Printf("\"%s\",\"%d\",\"%s\",\"%s\"\n", singleAP.SerialNumber, radio.RadioIndex, wlan.Bssid, wlan.Ssid)
			}
		}
	}

	os.Exit(errSuccess)
}
