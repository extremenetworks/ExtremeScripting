# GenericNbiClient.go

[GenericNbiClient.go](GenericNbiClient.go?raw=true) sends a query to the GraphQL-based API provided by the Northbound Interface (NBI) of Extreme Management Center (XMC; formerly known as NetSight) and prints the raw JSON response to stdout.

## Dependencies

This tool uses Go modules to handle dependencies.

## Running / Compiling

Use `go run ./...` to run the tool directly or `go build -o GenericNbiClient ./...` to compile a binary. Prebuilt binaries may be available as artifacts from the GitLab CI/CD [pipeline for tagged releases](https://gitlab.com/rbrt-weiler/xmc-nbi-genericnbiclient-go/pipelines?scope=tags).

Tested with [go1.15](https://golang.org/doc/go1.15).

## Usage

`GenericNbiClient --help`:

```text
Available options:
  -h, --host string     XMC Hostname / IP
      --port uint       HTTP port where XMC is listening (default 8443)
      --path string     Path where XMC is reachable
      --timeout uint    Timeout for HTTP(S) connections (default 5)
      --nohttps         Use HTTP instead of HTTPS
      --insecurehttps   Do not validate HTTPS certificates
  -u, --userid string   Client ID (OAuth) or username (Basic Auth) for authentication
  -s, --secret string   Client Secret (OAuth) or password (Basic Auth) for authentication
      --basicauth       Use HTTP Basic Auth instead of OAuth
      --version         Print version information and exit

If not provided, query will default to:
query { network { devices { up ip sysName nickName } } }

All options that take a value can be set via environment variables:
  XMCHOST           -->  --host
  XMCPORT           -->  --port
  XMCPATH           -->  --path
  XMCTIMEOUT        -->  --timeout
  XMCNOHTTPS        -->  --nohttps
  XMCINSECUREHTTPS  -->  --insecurehttps
  XMCUSERID         -->  --userid
  XMCSECRET         -->  --secret
  XMCBASICAUTH      -->  --basicauth

Environment variables can also be configured via a file called .xmcenv, located in the current directory or in the home directory of the current user.
```

## Authentication

GenericNbiClient supports two methods of authentication: OAuth2 and HTTP Basic Auth.

* OAuth2: To use OAuth2, provide the parameters `userid` and `secret`. GenericNbiClient will attempt to obtain an OAuth2 token from XMC with the supplied credentials and, if successful, submit only that token with each API request as part of the HTTP header.
* HTTP Basic Auth: To use HTTP Basic Auth, provide the parameters `userid` and `secret` as well as `basicauth`. GenericNbiClient will transmit the supplied credentials with each API request as part of the HTTP request header.

As all interactions between GenericNbiClient and XMC are secured with HTTPS by default both methods should be safe for transmission over networks. It is strongly recommended to use OAuth2 though. Should the credentials ever be compromised, for example when using them on the CLI on a shared workstation, remediation will be much easier with OAuth2. When using unencrypted HTTP transfer (`nohttps`), Basic Auth should never be used.

In order to use OAuth2 you will need to create a Client API Access client. To create such a client, visit the _Administration_ -> _Client API Access_ tab within XMC and click on _Add_. Make sure to note the returned credentials, as they will never be shown again.

## Authorization

Any user or API client who wants to access the Northbound Interface needs the appropriate access rights. In general, checking the full _Northbound API_ section within rights management will suffice. Depending on the use case, it may be feasible to go into detail and restrict the rights to the bare minimum required.

For API clients (OAuth2) the rights are defined when creating an API client and can later be adjusted in the same tab. For regular users (HTTP Basic Auth) the rights are managed via _Authorization Groups_ found in the _Administration_ -> _Users_ tab within XMC.

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xmc-nbi-genericnbiclient-go), with a [copy over at GitHub](https://github.com/rbrt-weiler/xmc-nbi-genericnbiclient-go) for the folks over there. It may be more up-to-date than the version included in ExtremeScripting.

## Support

_The software is provided as-is. There is no obligation to provide maintenance, support, updates, enhancements or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/), [BELL Computer-Netzwerke GmbH](https://www.bell.de/) or [Robert Weiler](https://robert.weiler.one/) is at its sole discretion._
