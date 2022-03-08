# XIQ Site Engine & Extreme Management Center Northbound Interface Clients

Client applications that utilize the NBI API provided by XIQ Site Engine / XMC / Netsight.

## How To

### XIQ Site Engine and XMC Version 8.4+ API Access

Setup the API client access via the web GUI -> Administration -> Client API Access -> Add.

## Executable NBI Clients

* [GenericNbiClient.go](GenericNbiClient.go/README.md): Application written in Go that can be used to send generic GraphQL queries to a remote XMC instance.
* [VlanLister.go](VlanLister.go/README.md): Tool that fetches the port/VLAN associations from XMC and stores the result as CSV and/or XLSX.

## XIQ Site Engine & XMC Version 8.4+ Python Class

### Python 3.5+ Scripts

| Script name   | Description   | Type   |
| ------------- | ------------- |:------:|
| [XMC_NBI](Python3/XMC_NBI.py?raw=true)|Python class 0.0.2 used by all the other scripts below. Works for XQI-Site Engine as well XMC 8.5.x|Python class|
| [get devices](Python3/get_devicese.py?raw=true)| pull all devices managed by XMC.|Python script|
| [get MACSs](Python3/get_MAC.py?raw=true)|pull all MAC addresses hosted by XMC.|Python script|
| [manage MAC's](Python3/manage_MAC.py?raw=true)|get / add update / delete MAC address in Printer End-System-Group.|Python script|
| [query](Python3/query.py?raw=true)|run native NBI query and mutation|Python script|
| [simple](Python3/simple.py?raw=true)|A simple example how to use the Python class XMC_NBI.py.|Python script|
| [site export](Python3/site_export.py?raw=true)|Export all site structure to file.|Python script|
| [site import](Python3/site_import.py?raw=true)|Import and create site structure based on file.|Python script|

## Support

_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).

>Be Extreme
