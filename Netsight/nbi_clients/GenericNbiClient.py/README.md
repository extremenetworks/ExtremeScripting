# GenericNbiClient.py

[GenericNbiClient.py](https://github.com/extremenetworks/ExtremeScripting/blob/master/Netsight/nbi_clients/GenericNbiClient.py/GenericNbiClient.py) sends a query to the GraphQL-based API provided by the Northbound Interface (NBI) of Extreme Management Center and prints the raw JSON response to stdout.

## Dependencies

GenericNbiClient.py requires the Python module `requests` to be installed. PIP may be used to install it:

`pip install requests`

## Usage

Tested with Python 3.8.0.

`GenericNbiClient.py -h`:

<pre>
  -h, --help            show this help message and exit
  --host HOST           XMC Hostname / IP
  --port PORT           HTTP port where XMC is listening
  --httptimeout HTTPTIMEOUT
                        Timeout for HTTP(S) connections
  --insecurehttps       Do not validate HTTPS certificates
  --username USERNAME   Username for HTTP auth
  --password PASSWORD   Password for HTTP auth
  --query QUERY         GraphQL query to send to XMC
  --version             Print version information and exit
</pre>

## Source

The original project is [hosted at GitLab](https://gitlab.com/rbrt-weiler/xmc-nbi-genericnbiclient-py), with a [copy over at GitHub](https://github.com/rbrt-weiler/xmc-nbi-genericnbiclient-py) for the folks over there.

## Support

_The software is provided as-is and neither [Extreme Networks](http://www.extremenetworks.com/) nor [the original author](https://robert.weiler.one/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [the original author](https://robert.weiler.one/) is at its sole discretion._
