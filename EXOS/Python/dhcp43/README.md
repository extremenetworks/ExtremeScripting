# dhcp43
dhcp43 is a script that will take generate the command needed to configure an EXOS switch's built in DHCP server to provide DHCP option 43 for EXOS ZTP automated config download.

## Description
This script takes arguments of filenames or URLS, and optionally a server IP address and a VLAN.

If the VLAN is provided, the script will configure the DHCP options on the specified vlan. Otherwise, it will simply provide the command needed to make this configuration change (without the VLAN specified)

### Files
* [dhcp43.py](dhcp43.py)
* [README.md](README.md)

### Requirements
ExtremeXOS 15.6+

### Usage
run script dhcp43.py [-h] [-s SERVER_ADDRESS] [-v VLAN_NAME] files [files ...]

### Example
```
X620-16x.1 # run script dhcp43.py -s 192.168.1.101 config.xsf summitX-21.1.2.14.xos
configure vlan <vlan_name> dhcp-options code 43 hex 64:04:c0:a8:01:65:65:0a:63:6f:6e:66:69:67:2e:78:73:66:65:15:73:75:6d:6d:69:74:58:2d:32:31:2e:31:2e:32:2e:31:34:2e:78:6f:73
```


## License
Copyright© 2016, Extreme Networks
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
The software is provided as is and Extreme Networks has no obligation to provide
maintenance, support, updates, enhancements or modifications.
Any support provided by Extreme Networks is at its sole discretion.

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).

>Be Extreme