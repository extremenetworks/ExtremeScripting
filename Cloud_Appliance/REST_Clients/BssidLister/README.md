# XCA REST BssidLister (Go)

[BssidLister](BssidLister.go) retrieves the list of Access Points and associated (B)SSIDs from [ExtremeCloud Appliance](https://www.extremenetworks.com/product/extremecloud-appliance/) (XCA) via the provided REST API and prints CSV to stdout.

It started as a rewrite of [the Python script provided by GTAC](https://extremeportal.force.com/ExtrArticleDetail?an=000077243&q=How-can-I-retrieve-a-list-of-BSSIDs-from-an-XCA-controller-using-the-REST-API), but the output of BssidLister includes way more details than the GTAC script by now.

## Dependencies

BssidLister uses the modules [godotenv](https://github.com/joho/godotenv), [envordef](https://gitlab.com/rbrt-weiler/go-module-envordef) and [xcarestclient](https://gitlab.com/rbrt-weiler/go-module-xcarestclient). Execute...

1. `go get -u github.com/joho/godotenv`
1. `go get -u gitlab.com/rbrt-weiler/go-module-envordef`
1. `go get -u gitlab.com/rbrt-weiler/go-module-xcarestclient`

...before running or compiling BssidLister. All other dependencies are included in a standard Go installation.

## Running / Compiling

Use `go run ./...` to run the tool directly or `go build -o BssidLister ./...` to compile a binary. Prebuilt binaries may be available as artifacts from the GitLab CI/CD [pipeline for tagged releases](https://gitlab.com/rbrt-weiler/xca-rest-bssidlister-go/pipelines?scope=tags).

Tested with [go1.13](https://golang.org/doc/go1.13).

## Usage

`BssidLister -h`:

<pre>
Available options:
  -host string
    	XCA Hostname / IP
  -port uint
    	HTTP port where XCA is listening (default 5825)
  -secret string
    	Client Secret for authentication
  -timeout uint
    	Timeout for HTTP(S) connections (default 5)
  -userid string
    	Client ID for authentication
  -version
    	Print version information and exit

All options that take a value can be set via environment variables:
  XCAHOST           -->  -host
  XCAPORT           -->  -port
  XCATIMEOUT        -->  -timeout
  XCAUSERID         -->  -userid
  XCASECRET         -->  -secret

Environment variables can also be configured via a file called .xcaenv,
located in the current directory or in the home directory of the current
user.
</pre>

## Authentication

BssidLister uses the OAuth authentication model used by XCA's API. Authentication is possible via username/password or via API Client credentials.

## Output

BssidLister prints CSV data to stdout when no errors occur. Any exit code that is not 0 indicates an error of some sort.

The CSV output will contain the following pieces of information _per SSID_:

1. serial: AP serial number
1. model: AP hardware type
1. ip: AP IP address
1. hostname: AP hostname
1. radio: Radio index
1. band: Wireless band
1. bssid: Service BSSID
1. ssid: Service SSID
1. disabled: Indictator whether the radio is active (false) or not (true)

A header is included in the first line of the output.

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xca-rest-bssidlister-go), with a [copy over at GitHub](https://github.com/rbrt-weiler/xca-rest-bssidlister-go) for the folks over there.

## Support

_The software is provided as-is. There is no obligation to provide maintenance, support, updates, enhancements or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [the original author](https://robert.weiler.one/) is at its sole discretion._

