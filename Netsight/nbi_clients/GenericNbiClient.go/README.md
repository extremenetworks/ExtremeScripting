# GenericNbiClient.go

[GenericNbiClient.go](https://github.com/extremenetworks/ExtremeScripting/blob/master/Netsight/nbi_clients/GenericNbiClient.go/GenericNbiClient.go) sends a query to the GraphQL-based API provided by the Northbound Interface (NBI) of Extreme Management Center and prints the raw JSON response to stdout.

## Compiling

Use `go run GenericNbiClient.go` to run the tool directly or `go build GenericNbiClient.go` to compile a binary.

Tested with go1.11 and go1.13.

## Usage

`GenericNbiClient -h`:

<pre>
  -host string
        XMC Hostname / IP
  -httptimeout uint
        Timeout for HTTP(S) connections (default 5)
  -insecurehttps
        Do not validate HTTPS certificates
  -password string
        Password for HTTP auth
  -port uint
        HTTP port where XMC is listening (default 8443)
  -query string
        GraphQL query to send to XMC (default "query { network { devices { up ip sysName nickName } } }")
  -username string
        Username for HTTP auth (default "admin")
  -version
        Print version information and exit
</pre>

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xmc-nbi-genericnbiclient-go), with a [copy over at GitHub](https://github.com/rbrt-weiler/xmc-nbi-genericnbiclient-go) for the folks over there.

## Support

_The software is provided as-is and neither [Extreme Networks](http://www.extremenetworks.com/) nor [BELL Computer-Netzwerke GmbH](https://www.bell.de/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [BELL Computer-Netzwerke GmbH](https://www.bell.de/) is at its sole discretion._
