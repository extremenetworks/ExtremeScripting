# VlanLister.go

VlanLister uses the GraphQL-based API provided by the Northbound Interface (NBI) of [Extreme Management Center](https://www.extremenetworks.com/product/extreme-management-center/) (XMC; formerly known as NetSight) to generate a CSV/XLSX file that lists all VLANs that are configured on all up switches along with port associations. The tool is intended to be used during audits and for general network documentation.

## Dependencies

VlanLister uses the modules [excelize](https://github.com/360EntSecGroup-Skylar/excelize), [godotenv](https://github.com/joho/godotenv), [envordef](https://gitlab.com/rbrt-weiler/go-module-envordef) and [xmcnbiclient](https://gitlab.com/rbrt-weiler/go-module-xmcnbiclient). Execute...

1. `go get -u github.com/360EntSecGroup-Skylar/excelize`
1. `go get -u github.com/joho/godotenv`
1. `go get -u gitlab.com/rbrt-weiler/go-module-envordef`
1. `go get -u gitlab.com/rbrt-weiler/go-module-xmcnbiclient`

...before running or compiling VlanLister. All other dependencies are included in a standard Go installation.

## Running / Compiling

Use `go run ./...` to run the tool directly or `go build -o VlanLister ./...` to compile a binary. Prebuilt binaries may be available as artifacts from the GitLab CI/CD [pipeline for tagged releases](https://gitlab.com/rbrt-weiler/xmc-nbi-vlanlister-go/pipelines?scope=tags).

Tested with [go1.13](https://golang.org/doc/go1.13) against XMC 8.4.1.24.

## Usage

`VlanLister -h`:

```text
Available options:
  -basicauth
    	Use HTTP Basic Auth instead of OAuth
  -host string
    	XMC Hostname / IP
  -includedown
    	Include inactive devices in result
  -insecurehttps
    	Do not validate HTTPS certificates
  -nohttps
    	Use HTTP instead of HTTPS
  -norefresh
    	Do not refresh (rediscover) devices
  -outfile value
    	File to write data to
  -path string
    	Path where XMC is reachable
  -port uint
    	HTTP port where XMC is listening (default 8443)
  -refreshinterval uint
    	Seconds to wait between triggering each refresh (default 5)
  -refreshwait uint
    	Minutes to wait after refreshing devices (default 15)
  -secret string
    	Client Secret (OAuth) or password (Basic Auth) for authentication
  -timeout uint
    	Timeout for HTTP(S) connections (default 5)
  -userid string
    	Client ID (OAuth) or username (Basic Auth) for authentication
  -version
    	Print version information and exit

It is required to provide at least one outfile. File types are determined
by the prefix FILETYPE: or the suffix .FILETYPE. Prefixes take priority
over suffixes. Valid FILETYPEs are:
  csv     -->  writes data a CSV file
  stdout  -->  prints CSV data to stdout
  xlsx    -->  writes data a XLSX file
When using stdout, you should remove all stderr output (2>/dev/null).

Nearly all options that take a value can be set via environment variables:
  XMCHOST             -->  -host
  XMCPORT             -->  -port
  XMCPATH             -->  -path
  XMCTIMEOUT          -->  -timeout
  XMCNOHTTPS          -->  -nohttps
  XMCINSECUREHTTPS    -->  -insecurehttps
  XMCUSERID           -->  -userid
  XMCSECRET           -->  -secret
  XMCBASICAUTH        -->  -basicauth
  XMCNOREFRESH        -->  -norefresh
  XMCREFRESHINTERVAL  -->  -refreshinterval
  XMCREFRESHWAIT      -->  -refreshwait
  XMCINCLUDEDOWN      -->  -includedown

Environment variables can also be configured via a file called .xmcenv,
located in the current directory or in the home directory of the current
user.
```

### Examples

1. `VlanLister -host xmc.example.com -insecurehttps -basicauth -userid root -secret abc123 -includedown -outfile xmc-vlans.csv`  
   Connect to xmc.example.com as root using HTTP Basic Auth. Skip HTTPS certificate checking and include devices that are down. Write results to xmc-vlans.csv.
1. `VlanLister -host xmc.example.com -basicauth -userid root -secret abc123 -outfile xmc-vlans.csv`  
   Same as above, but with HTTPS certificate checking and without including down devices in the outfile.
1. `VlanLister -host xmc.example.com -userid XMCOAuthID -secret 01234567-89ab-cdef-0123-456789abcdef -outfile xmc-vlans.csv -outfile xmc-vlans.xlsx`  
   Connect to xmc.example.com using OAuth authentication and HTTPS certificate checking. Write the results to both xmc-vlans.csv (in CSV format) and xmc-vlans.xlsx (in Excel format). File type is determined by suffix in this case.
1. `VlanLister -host xmc.example.com -userid XMCOAuthID -secret 01234567-89ab-cdef-0123-456789abcdef -outfile xlsx:xmc-vlans.archive`  
   Connect to xmc.example.com using OAuth authentication and HTTPS certificate checking. Write the results to xmc-vlans.archive in Excel format. File type is defined by prefix in this case.
1. `VlanLister -host xmc.example.com -userid XMCOAuthID -secret 01234567-89ab-cdef-0123-456789abcdef -outfile stdout: 2>/dev/null`  
   Connect to xmc.example.com using OAuth authentication and HTTPS certificate checking. Print the result to stdout in CSV format while surpressing all output to stderr.

## Authentication

VlanLister supports two methods of authentication: OAuth2 and HTTP Basic Auth.

* OAuth2: To use OAuth2, provide the parameters `userid` and `secret`. VlanLister will attempt to obtain an OAuth2 token from XMC with the supplied credentials and, if successful, submit only that token with each API request as part of the HTTP header.
* HTTP Basic Auth: To use HTTP Basic Auth, provide the parameters `userid` and `secret` as well as `basicauth`. VlanLister will transmit the supplied credentials with each API request as part of the HTTP request header.

As all interactions between VlanLister and XMC are secured with HTTPS by default both methods should be safe for transmission over networks. It is strongly recommended to use OAuth2 though. Should the credentials ever be compromised, for example when using them on the CLI on a shared workstation, remediation will be much easier with OAuth2. When using unencrypted HTTP transfer (`nohttps`), Basic Auth should never be used.

In order to use OAuth2 you will need to create a Client API Access client. To create such a client, visit the _Administration_ -> _Client API Access_ tab within XMC and click on _Add_. Make sure to note the returned credentials, as they will never be shown again.

## Authorization

Any user or API client who wants to access the Northbound Interface needs the appropriate access rights. In general, checking the full _Northbound API_ section within rights management will suffice. Depending on the use case, it may be feasible to go into detail and restrict the rights to the bare minimum required.

For API clients (OAuth2) the rights are defined when creating an API client and can later be adjusted in the same tab. For regular users (HTTP Basic Auth) the rights are managed via _Authorization Groups_ found in the _Administration_ -> _Users_ tab within XMC.

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xmc-nbi-vlanlister-go), with a [copy over at GitHub](https://github.com/rbrt-weiler/xmc-nbi-vlanlister-go) for the folks over there. It may be more up-to-date than the version included in ExtremeScripting.

## Support

_The software is provided as-is and neither [Extreme Networks](http://www.extremenetworks.com/) nor [the original author](https://robert.weiler.one/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [the original author](https://robert.weiler.one/) is at its sole discretion._
