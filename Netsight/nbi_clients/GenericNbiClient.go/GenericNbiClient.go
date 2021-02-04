package main

import (
	"fmt"
	"os"
	"path"
	"strings"

	consolehelper "gitlab.com/rbrt-weiler/go-module-consolehelper"
	envordef "gitlab.com/rbrt-weiler/go-module-envordef"
	godotenv "github.com/joho/godotenv"
	pflag "github.com/spf13/pflag"
	xmcnbiclient "gitlab.com/rbrt-weiler/go-module-xmcnbiclient"
)

// appConfig stores the application configuration once parsed by flags.
type appConfig struct {
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
	toolName        string = "GenericNbiClient.go"
	toolVersion     string = "1.0.1"
	toolID          string = toolName + "/" + toolVersion
	toolURL         string = "https://gitlab.com/rbrt-weiler/xmc-nbi-genericnbiclient-go"
	envFileName     string = ".xmcenv"
	defaultXMCQuery string = "query { network { devices { up ip sysName nickName } } }"
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

// Global variables used throughout the program.
var (
	config appConfig                   // User configuration
	cons   consolehelper.ConsoleHelper // Pretty printing
)

// parseCLIOptions parses all options passed by env or CLI into the Config variable.
func parseCLIOptions() {
	pflag.CommandLine.SortFlags = false
	pflag.StringVarP(&config.XMCHost, "host", "h", envordef.StringVal("XMCHOST", ""), "XMC Hostname / IP")
	pflag.UintVar(&config.XMCPort, "port", envordef.UintVal("XMCPORT", 8443), "HTTP port where XMC is listening")
	pflag.StringVar(&config.XMCPath, "path", envordef.StringVal("XMCPATH", ""), "Path where XMC is reachable")
	pflag.UintVar(&config.HTTPTimeout, "timeout", envordef.UintVal("XMCTIMEOUT", 5), "Timeout for HTTP(S) connections")
	pflag.BoolVar(&config.NoHTTPS, "nohttps", envordef.BoolVal("XMCNOHTTPS", false), "Use HTTP instead of HTTPS")
	pflag.BoolVar(&config.InsecureHTTPS, "insecurehttps", envordef.BoolVal("XMCINSECUREHTTPS", false), "Do not validate HTTPS certificates")
	pflag.StringVarP(&config.XMCUserID, "userid", "u", envordef.StringVal("XMCUSERID", ""), "Client ID (OAuth) or username (Basic Auth) for authentication")
	pflag.StringVarP(&config.XMCSecret, "secret", "s", envordef.StringVal("XMCSECRET", ""), "Client Secret (OAuth) or password (Basic Auth) for authentication")
	pflag.BoolVar(&config.BasicAuth, "basicauth", envordef.BoolVal("XMCBASICAUTH", false), "Use HTTP Basic Auth instead of OAuth")
	pflag.BoolVar(&config.PrintVersion, "version", false, "Print version information and exit")
	pflag.Usage = func() {
		cons.Fprintf(os.Stderr, "%s\n", toolID)
		cons.Fprintf(os.Stderr, "%s\n", toolURL)
		cons.Fprintf(os.Stderr, "\n")
		cons.Fprintf(os.Stderr, "This tool queries the Northbound Interface (NBI) of Extreme Management Center (XMC) and prints the raw reply (in JSON format) to stdout.\n")
		cons.Fprintf(os.Stderr, "\n")
		cons.Fprintf(os.Stderr, "Usage: %s [options] query\n", path.Base(os.Args[0]))
		cons.Fprintf(os.Stderr, "\n")
		cons.Fprintf(os.Stderr, "Available options:\n")
		pflag.PrintDefaults()
		cons.Fprintf(os.Stderr, "\n")
		cons.Fprintf(os.Stderr, "If not provided, query will default to:\n")
		cons.Fprintf(os.Stderr, "%s\n", defaultXMCQuery)
		cons.Fprintf(os.Stderr, "\n")
		cons.Fprintf(os.Stderr, "All options that take a value can be set via environment variables:\n")
		cons.Fprintf(os.Stderr, "  XMCHOST           -->  --host\n")
		cons.Fprintf(os.Stderr, "  XMCPORT           -->  --port\n")
		cons.Fprintf(os.Stderr, "  XMCPATH           -->  --path\n")
		cons.Fprintf(os.Stderr, "  XMCTIMEOUT        -->  --timeout\n")
		cons.Fprintf(os.Stderr, "  XMCNOHTTPS        -->  --nohttps\n")
		cons.Fprintf(os.Stderr, "  XMCINSECUREHTTPS  -->  --insecurehttps\n")
		cons.Fprintf(os.Stderr, "  XMCUSERID         -->  --userid\n")
		cons.Fprintf(os.Stderr, "  XMCSECRET         -->  --secret\n")
		cons.Fprintf(os.Stderr, "  XMCBASICAUTH      -->  --basicauth\n")
		cons.Fprintf(os.Stderr, "\n")
		cons.Fprintf(os.Stderr, "Environment variables can also be configured via a file called %s, located in the current directory or in the home directory of the current user.\n", envFileName)
		os.Exit(errUsage)
	}
	pflag.Parse()
	config.XMCQuery = strings.Join(pflag.CommandLine.Args(), " ")
	if config.XMCQuery == "" {
		config.XMCQuery = defaultXMCQuery
	}
}

// init loads environment files if available.
func init() {
	// initialize console size
	cons.UpdateDimensions()

	// if envFileName exists in the current directory, load it
	localEnvFile := fmt.Sprintf("./%s", envFileName)
	if _, localEnvErr := os.Stat(localEnvFile); localEnvErr == nil {
		if loadErr := godotenv.Load(localEnvFile); loadErr != nil {
			cons.Fprintf(os.Stderr, "Could not load env file <%s>: %s", localEnvFile, loadErr)
		}
	}

	// if envFileName exists in the user's home directory, load it
	if homeDir, homeErr := os.UserHomeDir(); homeErr == nil {
		homeEnvFile := fmt.Sprintf("%s/%s", homeDir, ".xmcenv")
		if _, homeEnvErr := os.Stat(homeEnvFile); homeEnvErr == nil {
			if loadErr := godotenv.Load(homeEnvFile); loadErr != nil {
				cons.Fprintf(os.Stderr, "Could not load env file <%s>: %s", homeEnvFile, loadErr)
			}
		}
	}
}

// main ties everything together.
func main() {
	// Parse all valid CLI options into variables.
	parseCLIOptions()

	// Print version information and exit.
	if config.PrintVersion {
		cons.Println(toolID)
		os.Exit(errSuccess)
	}
	// Check that the option "host" has been set.
	if config.XMCHost == "" {
		cons.Fprintln(os.Stderr, "Variable --host must be defined. Use --help to get help.")
		os.Exit(errMissArg)
	}

	// Set up a NBI client
	client := xmcnbiclient.New(config.XMCHost)
	client.SetUserAgent(toolID)
	if portErr := client.SetPort(config.XMCPort); portErr != nil {
		cons.Fprintf(os.Stderr, "XMC port could not be set: %s\n", portErr)
		os.Exit(errHTTPPort)
	}
	if config.NoHTTPS {
		client.UseHTTP()
	}
	if config.InsecureHTTPS {
		client.UseInsecureHTTPS()
	}
	if timeoutErr := client.SetTimeout(config.HTTPTimeout); timeoutErr != nil {
		cons.Fprintf(os.Stderr, "HTTP timeout could not be set: %s\n", timeoutErr)
		os.Exit(errHTTPTimeout)
	}
	client.SetBasePath(config.XMCPath)
	client.UseOAuth(config.XMCUserID, config.XMCSecret)
	if config.BasicAuth {
		client.UseBasicAuth(config.XMCUserID, config.XMCSecret)
	}

	// Call the API and print the result.
	apiResult, apiError := client.QueryAPI(config.XMCQuery)
	if apiError != nil {
		cons.Fprintf(os.Stderr, "Could not retrieve API result: %s\n", apiError)
		os.Exit(errAPIResult)
	}
	cons.Println(string(apiResult))

	// Exit with an appropriate exit code.
	os.Exit(errSuccess)
}
