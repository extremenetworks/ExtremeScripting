# generic XIQ REST API (Python)

[XIQ](XIQ.py) Python class using the [XIQ-API](https://developer.extremecloudiq.com/)
[get_clients](get_clients.py) pull all clients using the XIQ Python class
[get_devices](get_devices.py) pull all devices using the XIQ Python class
[APs_show_version](ap_show_version.py) execute commands against AP using the XIQ Python class

## Dependencies

The XIQ Python class using the module called [requests] you may have to install using "pip install requests".

## Usage

Before you execute you have to edit the file to provide you own login
xiqUser   = 'xxxxxxxx'
xiqPasswd = 'xxxxxxxx'

To discover all available call, please use the [Swagger UI] (https://api.extremecloudiq.com/swagger-ui/index.html?configUrl=/openapi/swagger-config&layout=BaseLayout)

## Support

_The software is provided as-is. There is no obligation to provide maintenance, support, updates, enhancements or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) or [the original author](https://robert.weiler.one/) is at its sole discretion._
