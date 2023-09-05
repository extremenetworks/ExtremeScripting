# XIQ REST BssidLister (Go)

[BssidLister](BssidLister.go) retrieves the list of Access Points and associated (B)SSIDs from [ExtremeCloud IQ](https://extremecloudiq.com/) (XCA) via the provided REST API and prints CSV to stdout.

## Dependencies

BssidLister uses the modules [godotenv](https://github.com/joho/godotenv), [envordef](https://gitlab.com/rbrt-weiler/go-module-envordef) and [xiqrestclient](https://gitlab.com/rbrt-weiler/go-module-xiqrestclient). Execute...

1. `go get -u github.com/joho/godotenv`
1. `go get -u gitlab.com/rbrt-weiler/go-module-envordef`
1. `go get -u gitlab.com/rbrt-weiler/go-module-xiqrestclient`

...before running or compiling GenericNbiClient. All other dependencies are included in a standard Go installation.

## Running / Compiling

Use `go run ./...` to run the tool directly or `go build -o BssidLister ./...` to compile a binary. Prebuilt binaries may be available as artifacts from the GitLab CI/CD [pipeline for tagged releases](https://gitlab.com/rbrt-weiler/xiq-rest-bssidlister-go/pipelines?scope=tags).

Tested with [go1.13](https://golang.org/doc/go1.13).

## Usage

`BssidLister -h`:

<pre>
Available options:
  -accesstoken string
    	Access token to authenticate with XIQ
  -clientid string
    	Client ID for authentication
  -clientsecret string
    	Client Secret for authentication
  -host string
    	XIQ Hostname / IP
  -ownerid string
    	Owner ID of the XIQ instance to use
  -redirecturi string
    	Redirect URI configured for used app
  -timeout uint
    	Timeout for HTTP(S) connections (default 5)
  -version
    	Print version information and exit

All options that take a value can be set via environment variables:
  XIQHOST           -->  -host
  XIQTIMEOUT        -->  -timeout
  XIQOWNERID        -->  -ownerid
  XIQACCESSTOKEN    -->  -accesstoken
  XIQCLIENTID       -->  -clientid
  XIQCLIENTSECRET   -->  -clientsecret
  XIQREDIRECTURI    -->  -redirecturi

Environment variables can also be configured via a file called .xiqenv,
located in the current directory or in the home directory of the current
user.
</pre>

## Authentication

BssidLister uses the OAuth authentication model used by XIQ's API. Authentication requires Owner ID, Access Token, Client ID, Client Secret and Redirect URI.

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xiq-rest-bssidlister-go), with a [copy over at GitHub](https://github.com/rbrt-weiler/xiq-rest-bssidlister-go) for the folks over there.

## Support

_The software is provided as-is. There is no obligation to provide maintenance, support, updates, enhancements or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [the original author](https://robert.weiler.one/) is at its sole discretion._
