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

	godotenv "github.com/joho/godotenv"
	envordef "gitlab.com/rbrt-weiler/go-module-envordef"
	xcarestclient "gitlab.com/rbrt-weiler/go-module-xcarestclient"
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

type apDetails struct {
	SerialNumber    string   `json:"serialNumber"`
	CanEdit         bool     `json:"canEdit"`
	CanDelete       bool     `json:"canDelete"`
	Proxied         string   `json:"proxied"`
	ApName          string   `json:"apName"`
	Hostname        string   `json:"hostname"`
	MacAddress      string   `json:"macAddress"`
	HardwareType    string   `json:"hardwareType"`
	PlatformName    string   `json:"platformName"`
	Description     string   `json:"description"`
	SoftwareVersion string   `json:"softwareVersion"`
	IPAddress       string   `json:"ipAddress"`
	MgmtVlanID      int      `json:"mgmtVlanId"`
	Environment     string   `json:"environment"`
	ForcePoEPlus    bool     `json:"forcePoEPlus"`
	Lag             bool     `json:"lag"`
	EthMode         string   `json:"ethMode"`
	EthSpeed        string   `json:"ethSpeed"`
	Home            string   `json:"home"`
	AdoptedBy       string   `json:"adoptedBy"`
	HostSite        string   `json:"hostSite"`
	ProfileID       string   `json:"profileId"`
	RfMgmtPolicyID  string   `json:"rfMgmtPolicyId"`
	EthPowerStatus  string   `json:"ethPowerStatus"`
	Services        []string `json:"services"`
	Radios          []struct {
		RadioIndex           int           `json:"radioIndex"`
		AdminState           bool          `json:"adminState"`
		Mode                 string        `json:"mode"`
		Channelwidth         string        `json:"channelwidth"`
		UseSmartRf           bool          `json:"useSmartRf"`
		ReqChannel           string        `json:"reqChannel"`
		TxMaxPower           int           `json:"txMaxPower"`
		OpChannel            string        `json:"opChannel"`
		TxPower              int           `json:"txPower"`
		AdminStateOvr        bool          `json:"adminStateOvr"`
		AggregateMpdu        string        `json:"aggregateMpdu"`
		Ldpc                 string        `json:"ldpc"`
		Stbc                 bool          `json:"stbc"`
		TxBf                 string        `json:"txBf"`
		Attenuation          int           `json:"attenuation"`
		Mbr                  string        `json:"mbr"`
		MbrOvr               bool          `json:"mbrOvr"`
		Dtim                 int           `json:"dtim"`
		DtimOvr              bool          `json:"dtimOvr"`
		Dot11GPM             string        `json:"dot11gPM"`
		Dot11GPMOvr          bool          `json:"dot11gPMOvr"`
		AggMsdu              bool          `json:"aggMsdu"`
		AggMsduOvr           bool          `json:"aggMsduOvr"`
		AggMpduOvr           bool          `json:"aggMpduOvr"`
		AggMpduSF            int           `json:"aggMpduSF"`
		AggMpduSFOvr         bool          `json:"aggMpduSFOvr"`
		Addba                bool          `json:"addba"`
		AddbaOvr             bool          `json:"addbaOvr"`
		LdpcOvr              bool          `json:"ldpcOvr"`
		StbcOvr              bool          `json:"stbcOvr"`
		TxbfOvr              bool          `json:"txbfOvr"`
		ProbeSuppRssTh       int           `json:"probeSuppRssTh"`
		ProbeSuppOnLowRss    bool          `json:"probeSuppOnLowRss"`
		DeasscOnLowRss       bool          `json:"deasscOnLowRss"`
		ProbeSuppRssThOvr    bool          `json:"probeSuppRssThOvr"`
		ProbeSuppOnLowRssOvr bool          `json:"probeSuppOnLowRssOvr"`
		DeasscOnLowRssOvr    bool          `json:"deasscOnLowRssOvr"`
		Ofdma                string        `json:"ofdma"`
		Bsscolor             int           `json:"bsscolor"`
		Twt                  bool          `json:"twt"`
		OfdmaOvr             bool          `json:"ofdmaOvr"`
		BsscolorOvr          bool          `json:"bsscolorOvr"`
		TwtOvr               bool          `json:"twtOvr"`
		Services             []string      `json:"services"`
		ServicesOvr          bool          `json:"servicesOvr"`
		FallbackChannels     []interface{} `json:"fallbackChannels"`
		Wlan                 []struct {
			Bssid string `json:"bssid"`
			Ssid  string `json:"ssid"`
		} `json:"wlan"`
	} `json:"radios"`
	Location                string        `json:"location"`
	MaintainClientSession   string        `json:"maintainClientSession"`
	ApPersistence           string        `json:"apPersistence"`
	McastAssembly           bool          `json:"mcastAssembly"`
	PollTimeout             int           `json:"pollTimeout"`
	PollTimeoutOvr          bool          `json:"pollTimeoutOvr"`
	LedStatus               string        `json:"ledStatus"`
	LedStatusOvr            bool          `json:"ledStatusOvr"`
	ApprovedStatus          string        `json:"approvedStatus"`
	AddrAssn                bool          `json:"addrAssn"`
	IPNetmask               string        `json:"ipNetmask"`
	IPGateway               string        `json:"ipGateway"`
	IotEnabled              bool          `json:"iotEnabled"`
	IotAppID                string        `json:"iotAppId"`
	IotiBeaconMajor         int           `json:"iotiBeaconMajor"`
	IotiBeaconMajorOvr      bool          `json:"iotiBeaconMajorOvr"`
	IotiBeaconMinor         int           `json:"iotiBeaconMinor"`
	IotiBeaconMinorOvr      bool          `json:"iotiBeaconMinorOvr"`
	IotEddistoneURL         string        `json:"iotEddistoneUrl"`
	IotEddistoneURLOvr      bool          `json:"iotEddistoneUrlOvr"`
	IotMeasuredRssi         int           `json:"iotMeasuredRssi"`
	IotMeasuredRssiOverride bool          `json:"iotMeasuredRssiOverride"`
	IotAntennaModelID       int           `json:"iotAntennaModelId"`
	Mtu                     int           `json:"mtu"`
	MtuOvr                  bool          `json:"mtuOvr"`
	MgmtVlanIDOvr           bool          `json:"mgmtVlanIdOvr"`
	LagOvr                  bool          `json:"lagOvr"`
	ApAntennaModels         interface{}   `json:"apAntennaModels"`
	Meshpoints              []interface{} `json:"meshpoints"`
	SupportedCountries      []string      `json:"supportedCountries"`
	Features                []string      `json:"features"`
}

// Definitions used within the code.
const (
	toolName     string = "BssidLister.go"
	toolVersion  string = "0.3.0"
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
	config appConfig
	xca    xcarestclient.RESTClient
)

func getAccessPoints() (apResultSet, error) {
	var apList apResultSet

	req, reqErr := xca.GetRequest("v1/aps")
	if reqErr != nil {
		return apList, fmt.Errorf("could not create HTTP(S) request: %s", reqErr)
	}
	query := req.URL.Query()
	query.Add("inventory", "true")
	req.URL.RawQuery = query.Encode()

	// Try to get a result from the API.
	res, resErr := xca.PerformRequest(req)
	if resErr != nil {
		return apList, fmt.Errorf("could not connect to XCA: %s", resErr)
	}
	if res.StatusCode != http.StatusOK {
		return apList, fmt.Errorf("got status code %d instead of %d", res.StatusCode, http.StatusOK)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return apList, fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	// Read and parse the body of the HTTP response.
	body, bodyErr := ioutil.ReadAll(res.Body)
	if bodyErr != nil {
		return apList, fmt.Errorf("could not read server response: %s", bodyErr)
	}
	jsonErr := json.Unmarshal(body, &apList)
	if jsonErr != nil {
		return apList, fmt.Errorf("could not read server response: %s", jsonErr)
	}

	return apList, nil
}

func getAPDetails(serial string) (apDetails, error) {
	var details apDetails

	req, reqErr := xca.GetRequest(fmt.Sprintf("v1/aps/%s", serial))
	if reqErr != nil {
		return details, fmt.Errorf("could not create HTTP(S) request: %s", reqErr)
	}

	// Try to get a result from the API.
	res, resErr := xca.PerformRequest(req)
	if resErr != nil {
		return details, fmt.Errorf("could not connect to XCA: %s", resErr)
	}
	if res.StatusCode != http.StatusOK {
		return details, fmt.Errorf("got status code %d instead of %d", res.StatusCode, http.StatusOK)
	}
	defer res.Body.Close()

	// Check if the HTTP response has yielded the expected content type.
	resContentType := res.Header.Get("Content-Type")
	if strings.Index(resContentType, jsonMimeType) != 0 {
		return details, fmt.Errorf("Content-Type %s returned instead of %s", resContentType, jsonMimeType)
	}

	// Read and parse the body of the HTTP response.
	body, bodyErr := ioutil.ReadAll(res.Body)
	if bodyErr != nil {
		return details, fmt.Errorf("could not read server response: %s", bodyErr)
	}
	jsonErr := json.Unmarshal(body, &details)
	if jsonErr != nil {
		return details, fmt.Errorf("could not read server response: %s", jsonErr)
	}

	return details, nil
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

	xca = xcarestclient.New(config.XCAHost)
	xca.SetPort(config.XCAPort)
	xca.UseInsecureHTTPS()
	xca.SetAuth(config.XCAUserID, config.XCASecret)
	xca.SetUserAgent(toolID)

	if authErr := xca.Authenticate(); authErr != nil {
		fmt.Printf("Could not authenticate: %s\n", authErr)
		os.Exit(errXCAAuth)
	}

	accessPoints, apErr := getAccessPoints()
	if apErr != nil {
		fmt.Printf("Could not obtain AP list: %s\n", apErr)
		os.Exit(errAPICall)
	}
	fmt.Printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n", "serial", "model", "ip", "hostname", "radio", "band", "bssid", "ssid", "disabled")
	for _, singleAP := range accessPoints {
		details, detailsErr := getAPDetails(singleAP.SerialNumber)
		if detailsErr != nil {
			fmt.Printf("Could not get AP details: %s\n", detailsErr)
			os.Exit(errAPICall)
		}
		for _, radio := range details.Radios {
			for _, wlan := range radio.Wlan {
				fmt.Printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%d\",\"%s\",\"%s\",\"%s\",\"%t\"\n", singleAP.SerialNumber, details.HardwareType, details.IPAddress, details.Hostname, radio.RadioIndex, radio.Mode, wlan.Bssid, wlan.Ssid, !radio.AdminState)
			}
		}
	}

	os.Exit(errSuccess)
}
