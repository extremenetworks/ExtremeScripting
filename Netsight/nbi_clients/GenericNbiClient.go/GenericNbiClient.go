package main

import (
	"flag"
	"fmt"
	"os"
	"path"
	"strconv"

	xmcnbiclient "gitlab.com/rbrt-weiler/go-module-xmcnbiclient"
)

// AppConfig stores the application configuration once parsed by flags.
type AppConfig struct {
	XMCHost       string
	XMCPort       uint
	XMCPath       string
	HTTPTimeout   uint
	NoHTTPS       bool
	InsecureHTTPS bool
	BasicAuth     bool
	XMCUserID     string
	XMCSecret     string
	XMCQuery      string
	PrintVersion  bool
}

// Definitions used within the code.
const (
	toolName      string = "XMC NBI GenericNbiClient.go"
	toolVersion   string = "0.10.0"
	versionString string = toolName + "/" + toolVersion
)

// Error codes.
const (
	errSuccess     int = 0  // No error
	errUsage       int = 1  // Usage error
	errMissArg     int = 2  // Missing arguments
	errAPIResult   int = 30 // Error retrieving a result from the API
	errHTTPPort    int = 40 // Error setting the HTTP port
	errHTTPTimeout int = 41 // Error setting the HTTP timeout
)

// Variables used to pass data between functions.
var (
	Config AppConfig
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

// parseCLIOptions parses all options passed by env or CLI into the Config variable.
func parseCLIOptions() {
	flag.StringVar(&Config.XMCHost, "host", getEnvOrDefaultString("XMCHOST", ""), "XMC Hostname / IP")
	flag.UintVar(&Config.XMCPort, "port", getEnvOrDefaultUint("XMCPORT", 8443), "HTTP port where XMC is listening")
	flag.StringVar(&Config.XMCPath, "path", getEnvOrDefaultString("XMCPATH", ""), "Path where XMC is reachable")
	flag.UintVar(&Config.HTTPTimeout, "timeout", getEnvOrDefaultUint("XMCTIMEOUT", 5), "Timeout for HTTP(S) connections")
	flag.BoolVar(&Config.NoHTTPS, "nohttps", getEnvOrDefaultBool("XMCNOHTTPS", false), "Use HTTP instead of HTTPS")
	flag.BoolVar(&Config.InsecureHTTPS, "insecurehttps", getEnvOrDefaultBool("XMCINSECURE", false), "Do not validate HTTPS certificates")
	flag.StringVar(&Config.XMCUserID, "userid", getEnvOrDefaultString("XMCUSERID", ""), "Client ID (OAuth) or username (Basic Auth) for authentication")
	flag.StringVar(&Config.XMCSecret, "secret", getEnvOrDefaultString("XMCSECRET", ""), "Client Secret (OAuth) or password (Basic Auth) for authentication")
	flag.BoolVar(&Config.BasicAuth, "basicauth", getEnvOrDefaultBool("XMCBASICAUTH", false), "Use HTTP Basic Auth instead of OAuth")
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
		fmt.Fprintf(os.Stderr, "All options that take a value can be set via environment variables:\n")
		fmt.Fprintf(os.Stderr, "  XMCHOST       -->  -host\n")
		fmt.Fprintf(os.Stderr, "  XMCPORT       -->  -port\n")
		fmt.Fprintf(os.Stderr, "  XMCPATH       -->  -path\n")
		fmt.Fprintf(os.Stderr, "  XMCTIMEOUT    -->  -timeout\n")
		fmt.Fprintf(os.Stderr, "  XMCNOHTTPS    -->  -nohttps\n")
		fmt.Fprintf(os.Stderr, "  XMCINSECURE   -->  -insecurehttps\n")
		fmt.Fprintf(os.Stderr, "  XMCUSERID     -->  -userid\n")
		fmt.Fprintf(os.Stderr, "  XMCSECRET     -->  -secret\n")
		fmt.Fprintf(os.Stderr, "  XMCBASICAUTH  -->  -basicauth\n")
		fmt.Fprintf(os.Stderr, "  XMCQUERY      -->  -query\n")
		os.Exit(errUsage)
	}
	flag.Parse()
}

// main ties everything together.
func main() {
	// Parse all valid CLI options into variables.
	parseCLIOptions()

	// Print version information and exit.
	if Config.PrintVersion {
		fmt.Println(versionString)
		os.Exit(errSuccess)
	}
	// Check that the option "host" has been set.
	if Config.XMCHost == "" {
		fmt.Fprintln(os.Stderr, "Variable -host must be defined. Use -h to get help.")
		os.Exit(errMissArg)
	}

	// Set up a NBI client
	client := xmcnbiclient.New(Config.XMCHost)
	client.SetUserAgent(versionString)
	portErr := client.SetPort(Config.XMCPort)
	if portErr != nil {
		fmt.Fprintf(os.Stderr, "Port could not be set: %s\n", portErr)
		os.Exit(errHTTPPort)
	}
	if Config.NoHTTPS {
		client.UseHTTP()
	}
	if Config.InsecureHTTPS {
		client.UseInsecureHTTPS()
	}
	timeoutErr := client.SetTimeout(Config.HTTPTimeout)
	if timeoutErr != nil {
		fmt.Fprintf(os.Stderr, "Timeout could not be set: %s\n", timeoutErr)
		os.Exit(errHTTPTimeout)
	}
	client.SetBasePath(Config.XMCPath)
	client.UseOAuth(Config.XMCUserID, Config.XMCSecret)
	if Config.BasicAuth {
		client.UseBasicAuth(Config.XMCUserID, Config.XMCSecret)
	}

	// Call the API and print the result.
	apiResult, apiError := client.QueryAPI(Config.XMCQuery)
	if apiError != nil {
		fmt.Fprintf(os.Stderr, "Could not retrieve API result: %s\n", apiError)
		os.Exit(errAPIResult)
	}
	fmt.Println(string(apiResult))

	// Exit with an appropriate exit code.
	os.Exit(errSuccess)
}
