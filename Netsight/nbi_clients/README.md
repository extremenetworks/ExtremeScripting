# XIQ Site Engine & Extreme Management Center Northbound Interface Clients

Client applications that utilize the NBI API provided by XIQ Site Engine - XMC - Netsight.

## How To
### XIQ Site Engine and XMC version 8.4+
* setup the API client access = Open the web GUI -> Administration -> Client API Access -> Add

## generic NBI client examples
* [GenericNbiClient.go](GenericNbiClient.go/README.md): Application written in Go that can be used to send generic GraphQL queries to a remote XMC instance.
* [GenericNbiClient.py](GenericNbiClient.py/README.md) (deprecated): Application written in Python that can be used to send generic GraphQL queries to a remote XMC instance.
* [VlanLister.go](VlanLister.go/README.md): Tool that fetches the port/VLAN associations from XMC and stores the result as CSV and/or XLSX.

# XIQ Site Engine & XMC version 8.4+ Python class
## Python 3.5+ scripts
| Script name   | Description   | Type   |
| ------------- | ------------- |:------:|
| [XMC_NBI](Python3/XMC_NBI.py?raw=true)|Python class used by all the other scripts below.|Python class|
| [get all devices](Python3/get_all_devicese_from_XMC.py?raw=true)| pull all devices managed by XMC.|Python script|
| [get all MACs](Python3/get-all-MAC-from-XMC.py?raw=true)|pull all MAC addresses hosted by XMC.|Python script|
| [manage MAC](Python3/manage_MAC_in_XMC.py?raw=true)|get / add update / delete MAC address in Printer End-System-Group.|Python script|

## Support

_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com).

>Be Extreme
