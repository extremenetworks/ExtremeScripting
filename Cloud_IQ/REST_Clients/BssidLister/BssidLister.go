package main

import (
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
	xiqrestclient "gitlab.com/rbrt-weiler/go-module-xiqrestclient"
)

// Definitions used within the code.
const (
	toolName     string = "BssidLister.go"
	toolVersion  string = "0.1.0"
	toolID       string = toolName + "/" + toolVersion
	toolURL      string = "https://gitlab.com/rbrt-weiler/xiq-rest-bssidlister-go"
	envFileName  string = ".xiqenv"
	jsonMimeType string = "application/json"
)

// Error codes.
const (
	errSuccess int = 0   // No error
	errUsage   int = 1   // Usage error
	errXIQAuth int = 10  // Authentication error
	errAPICall int = 11  // API Call error
	errGeneric int = 255 // Generic error
)

// AppConfig stores the application configuration once parsed by flags.
type appConfig struct {
	XIQHost         string
	HTTPTimeout     uint
	XIQOwnerID      string
	XIQAccessToken  string
	XIQClientID     string
	XIQClientSecret string
	XIQRedirectURI  string
	PrintVersion    bool
}

type deviceList struct {
	Data []struct {
		DeviceID                 int64       `json:"deviceId"`
		OwnerID                  int         `json:"ownerId"`
		MacAddress               string      `json:"macAddress"`
		Connected                bool        `json:"connected"`
		HostName                 string      `json:"hostName"`
		SerialID                 string      `json:"serialId"`
		Model                    string      `json:"model"`
		IP                       string      `json:"ip"`
		Mode                     string      `json:"mode"`
		OsVersion                string      `json:"osVersion"`
		LastUpdated              time.Time   `json:"lastUpdated"`
		MgmtStatus               string      `json:"mgmtStatus"`
		SubnetMask               string      `json:"subnetMask"`
		DefaultGateway           string      `json:"defaultGateway"`
		DNS                      string      `json:"dns"`
		SimType                  string      `json:"simType"`
		UnAssociatedClientsCount int         `json:"unAssociatedClientsCount"`
		PresenceOn               bool        `json:"presenceOn"`
		ActiveClients            int         `json:"activeClients"`
		SystemUpTime             int64       `json:"systemUpTime"`
		Locations                []string    `json:"locations"`
		ConnectedClients         interface{} `json:"connectedClients"`
	} `json:"data"`
	Error      interface{} `json:"error"`
	Pagination struct {
		Offset      int `json:"offset"`
		CountInPage int `json:"countInPage"`
		TotalCount  int `json:"totalCount"`
	} `json:"pagination"`
}

type ssidList struct {
	Data []struct {
		InterfaceName   string `json:"interfaceName"`
		DisableAllSSIDs bool   `json:"disableAllSSIDs"`
		Entries         []struct {
			ID            int64  `json:"id"`
			Name          string `json:"name"`
			BroadcastName string `json:"broadcastName"`
			RadioBand     string `json:"radioBand"`
			Disable       bool   `json:"disable"`
		} `json:"entries"`
	} `json:"data"`
	Error struct {
		Status int `json:"status"`
	} `json:"error"`
}

// Variables used to pass data between functions.
var (
	config appConfig
	xiq    xiqrestclient.RESTClient
)

func getDevices() (deviceList, error) {
	var deviceResult deviceList

	req, reqErr := xiq.GetRequest("v1/monitor/devices")
	if reqErr != nil {
		return deviceResult, fmt.Errorf("could not create HTTP(S) request: %s", reqErr)
	}

	res, resErr := xiq.PerformRequest(req)
	if resErr != nil {
		return deviceResult, fmt.Errorf("could not connect to XIQ: %s", resErr)
	}
	if res.StatusCode != http.StatusOK {
		return deviceResult, fmt.Errorf("got status code %d instead of %d", res.StatusCode, http.StatusOK)
	}
	defer res.Body.Close()

	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return deviceResult, fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	body, bodyErr := ioutil.ReadAll(res.Body)
	if bodyErr != nil {
		return deviceResult, fmt.Errorf("could not read server response: %s", bodyErr)
	}
	jsonErr := json.Unmarshal(body, &deviceResult)
	if jsonErr != nil {
		return deviceResult, fmt.Errorf("could not read server response: %s", jsonErr)
	}

	return deviceResult, nil
}

func getSSIDs(deviceID int64) (ssidList, error) {
	var ssidResult ssidList

	req, reqErr := xiq.GetRequest(fmt.Sprintf("v1/configuration/devices/%d/ssids", deviceID))
	if reqErr != nil {
		return ssidResult, fmt.Errorf("could not create HTTP(S) request: %s", reqErr)
	}

	res, resErr := xiq.PerformRequest(req)
	if resErr != nil {
		return ssidResult, fmt.Errorf("could not connect to XIQ: %s", resErr)
	}
	if res.StatusCode != http.StatusOK {
		return ssidResult, fmt.Errorf("got status code %d instead of %d", res.StatusCode, http.StatusOK)
	}
	defer res.Body.Close()

	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return ssidResult, fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	body, bodyErr := ioutil.ReadAll(res.Body)
	if bodyErr != nil {
		return ssidResult, fmt.Errorf("could not read server response: %s", bodyErr)
	}
	jsonErr := json.Unmarshal(body, &ssidResult)
	if jsonErr != nil {
		return ssidResult, fmt.Errorf("could not read server response: %s", jsonErr)
	}

	return ssidResult, nil
}

// parseCLIOptions parses all options passed by env or CLI into the Config variable.
func parseCLIOptions() {
	flag.StringVar(&config.XIQHost, "host", envordef.StringVal("XIQHOST", ""), "XIQ Hostname / IP")
	flag.UintVar(&config.HTTPTimeout, "timeout", envordef.UintVal("XIQTIMEOUT", 5), "Timeout for HTTP(S) connections")
	flag.StringVar(&config.XIQOwnerID, "ownerid", envordef.StringVal("XIQOWNERID", ""), "Owner ID of the XIQ instance to use")
	flag.StringVar(&config.XIQAccessToken, "accesstoken", envordef.StringVal("XIQACCESSTOKEN", ""), "Access token to authenticate with XIQ")
	flag.StringVar(&config.XIQClientID, "clientid", envordef.StringVal("XIQCLIENTID", ""), "Client ID for authentication")
	flag.StringVar(&config.XIQClientSecret, "clientsecret", envordef.StringVal("XIQCLIENTSECRET", ""), "Client Secret for authentication")
	flag.StringVar(&config.XIQRedirectURI, "redirecturi", envordef.StringVal("XIQREDIRECTURI", ""), "Redirect URI configured for used app")
	flag.BoolVar(&config.PrintVersion, "version", false, "Print version information and exit")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "%s\n", toolID)
		fmt.Fprintf(os.Stderr, "%s\n", toolURL)
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "This tool queries the XIQ API, fetches the list of Access Points and\n")
		fmt.Fprintf(os.Stderr, "associated (B)SSIDs and prints CSV to stdout.\n")
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Usage: %s [options]\n", path.Base(os.Args[0]))
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Available options:\n")
		flag.PrintDefaults()
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "All options that take a value can be set via environment variables:\n")
		fmt.Fprintf(os.Stderr, "  XIQHOST           -->  -host\n")
		fmt.Fprintf(os.Stderr, "  XIQTIMEOUT        -->  -timeout\n")
		fmt.Fprintf(os.Stderr, "  XIQOWNERID        -->  -ownerid\n")
		fmt.Fprintf(os.Stderr, "  XIQACCESSTOKEN    -->  -accesstoken\n")
		fmt.Fprintf(os.Stderr, "  XIQCLIENTID       -->  -clientid\n")
		fmt.Fprintf(os.Stderr, "  XIQCLIENTSECRET   -->  -clientsecret\n")
		fmt.Fprintf(os.Stderr, "  XIQREDIRECTURI    -->  -redirecturi\n")
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

	xiq = xiqrestclient.New(config.XIQHost, config.XIQOwnerID)
	xiq.SetAuth(config.XIQAccessToken, config.XIQClientID, config.XIQClientSecret, config.XIQRedirectURI)
	xiq.SetUserAgent(toolID)

	devices, devicesErr := getDevices()
	if devicesErr != nil {
		fmt.Printf("Error: %s\n", devicesErr)
		os.Exit(errGeneric)
	}
	fmt.Printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n", "serial", "model", "ip", "hostname", "radio", "band", "bssid", "ssid", "disabled")
	for _, dev := range devices.Data {
		ssids, ssidErr := getSSIDs(dev.DeviceID)
		if ssidErr != nil {
			fmt.Printf("Error: %s\n", ssidErr)
			os.Exit(errGeneric)
		}
		for _, ssid := range ssids.Data {
			for _, entry := range ssid.Entries {
				fmt.Printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%t\"\n", dev.SerialID, dev.Model, dev.IP, dev.HostName, ssid.InterfaceName, entry.RadioBand, entry.BroadcastName, entry.Name, entry.Disable)
			}
		}
	}

	os.Exit(errSuccess)
}
