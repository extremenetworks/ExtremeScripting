# GenericNbiClient.go

[GenericNbiClient.go](https://github.com/extremenetworks/ExtremeScripting/blob/master/Netsight/nbi_clients/GenericNbiClient.go/GenericNbiClient.go) sends a query to the GraphQL-based API provided by the Northbound Interface (NBI) of Extreme Management Center and prints the raw JSON response to stdout.

## Compiling

Use `go run GenericNbiClient.go` to run the tool directly or `go build GenericNbiClient.go` to compile a binary.

Tested with go1.13.

## Usage

`GenericNbiClient -h`:

<pre>
Available options:
  -clientid string
        Client ID for OAuth2
  -clientsecret string
        Client Secret for OAuth2
  -host string
        XMC Hostname / IP
  -httptimeout uint
        Timeout for HTTP(S) connections (default 5)
  -insecurehttps
        Do not validate HTTPS certificates
  -nohttps
        Use HTTP instead of HTTPS
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

OAuth2 will be preferred over username/password.

All options that take a value can be set via environment variables:
  XMCHOST          -->  -host
  XMCPORT          -->  -port
  XMCNOHTTPS       -->  -nohttps
  XMCINSECURE      -->  -insecurehttps
  XMCTIMEOUT       -->  -httptimeout
  XMCCLIENTID      -->  -clientid
  XMCCLIENTSECRET  -->  -clientsecret
  XMCUSERNAME      -->  -username
  XMCPASSWORD      -->  -password
  XMCQUERY         -->  -query
</pre>

## Authentication

GenericNbiClient supports two methods of authentication: HTTP Basic Auth and OAuth2.

  * HTTP Basic Auth: To use HTTP Basic Auth, provide the parameters `username` and `password`. GenericNbiClient will transmit the supplied credentials with each API request as part of the HTTP request header.
  * OAuth2: To use OAuth2, provide the parameters `clientid` and `clientsecret`. GenericNbiClient will attempt to obtain a OAuth2 token from XMC with the supplied credentials and, if successful, submit only that token with each API request as part of the HTTP header.

As all interactions between GenericNbiClient and XMC are secured with HTTPS by default both methods should be safe for transmission over networks. It is strongly recommended to use OAuth2 though. Should the crendetials ever be compromised, for example when using them on the CLI on a shared workstation, remediation will be much easier with OAuth2. When using unencrypted HTTP transfer (`nohttps`), Basic Auth should never be used.

In order to use OAuth2 you will need to create a Client API Access client. To create such a client, visit the _Administration_ -> _Client API Access_ tab within XMC and click on _Add_. Make sure to note the returned credentials, as they will never be shown again.

## Authorization

Any user or API client who wants to access the Northbound Interface needs the appropriate access rights. In general, checking the full _Northbound API_ section within rights management will suffice. Depending on the use case, it may be feasible to go into detail and restrict the rights to the bare minimum required.

For regular users (HTTP Basic Auth) the rights are managed via _Authorization Groups_ found in the _Administration_ -> _Users_ tab within XMC. For API clients (OAuth2) the rights are defined when creating an API client and can later be adjusted in the same tab.

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xmc-nbi-genericnbiclient-go), with a [copy over at GitHub](https://github.com/rbrt-weiler/xmc-nbi-genericnbiclient-go) for the folks over there. It may be more up-to-date than the version included in ExtremeScripting.

## Support

_The software is provided as-is and neither [Extreme Networks](http://www.extremenetworks.com/) nor [BELL Computer-Netzwerke GmbH](https://www.bell.de/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [BELL Computer-Netzwerke GmbH](https://www.bell.de/) is at its sole discretion._

