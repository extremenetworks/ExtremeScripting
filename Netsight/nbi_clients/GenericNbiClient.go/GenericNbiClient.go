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
	"crypto/tls"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path"
	"time"
)

const (
	toolName         string = "BELL XMC NBI GenericNbiClient.go"
	toolVersion      string = "0.3.0"
	httpUserAgent    string = toolName + "/" + toolVersion
	errSuccess       int    = 0  // No error
	errUsage         int    = 1  // Usage error
	errMissArg       int    = 2  // Missing arguments
	errHTTPRequest   int    = 10 // Error creating the HTTPS request
	errXMCConnect    int    = 11 // Error connecting to XMC
	errHTTPSResponse int    = 12 // Error parsing the HTTPS response
)

func main() {
	var xmcHost string
	var httpPort uint
	var httpTimeout uint
	var insecureHTTPS bool
	var httpUsername string
	var httpPassword string
	var xmcQuery string
	var printVersion bool

	flag.StringVar(&xmcHost, "host", "", "XMC Hostname / IP")
	flag.UintVar(&httpPort, "port", 8443, "HTTP port where XMC is listening")
	flag.UintVar(&httpTimeout, "httptimeout", 5, "Timeout for HTTP(S) connections")
	flag.BoolVar(&insecureHTTPS, "insecurehttps", false, "Do not validate HTTPS certificates")
	flag.StringVar(&httpUsername, "username", "admin", "Username for HTTP auth")
	flag.StringVar(&httpPassword, "password", "", "Password for HTTP auth")
	flag.StringVar(&xmcQuery, "query", "query { network { devices { up ip sysName nickName } } }", "GraphQL query to send to XMC")
	flag.BoolVar(&printVersion, "version", false, "Print version information and exit")
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "This tool queries the XMC API and prints the raw reply (JSON) to stdout.\n")
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Usage: %s [options]\n", path.Base(os.Args[0]))
		fmt.Fprintf(os.Stderr, "\n")
		fmt.Fprintf(os.Stderr, "Available options:\n")
		flag.PrintDefaults()
		os.Exit(errUsage)
	}
	flag.Parse()

	if printVersion {
		fmt.Println(httpUserAgent)
		os.Exit(errSuccess)
	}

	if xmcHost == "" {
		fmt.Fprintln(os.Stderr, "Variable -host must be defined. Use -h to get help.")
		os.Exit(errMissArg)
	}

	var apiURL string = "https://" + xmcHost + ":" + fmt.Sprint(httpPort) + "/nbi/graphql"
	httpTransport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: insecureHTTPS},
	}
	nbiClient := http.Client{
		Transport: httpTransport,
		Timeout:   time.Second * time.Duration(httpTimeout),
	}

	req, reqErr := http.NewRequest(http.MethodGet, apiURL, nil)
	if reqErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not create HTTPS request: %s\n", reqErr)
		os.Exit(errHTTPRequest)
	}

	req.Header.Set("User-Agent", httpUserAgent)
	req.SetBasicAuth(httpUsername, httpPassword)

	httpQuery := req.URL.Query()
	httpQuery.Add("query", xmcQuery)
	req.URL.RawQuery = httpQuery.Encode()

	res, getErr := nbiClient.Do(req)
	if getErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not connect to XMC: %s\n", getErr)
		os.Exit(errXMCConnect)
	}
	if res.StatusCode != 200 {
		fmt.Fprintf(os.Stderr, "Error: Got status code %d instead of 200\n", res.StatusCode)
		os.Exit(errXMCConnect)
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		fmt.Fprintf(os.Stderr, "Error: Could not read server response: %s\n", readErr)
		os.Exit(errHTTPSResponse)
	}
	fmt.Println(string(body))

	os.Exit(errSuccess)
}
