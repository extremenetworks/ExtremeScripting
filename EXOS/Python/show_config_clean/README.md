# Show config "clean"

## Description
This Python script will remove unused config sections from the output of "show configuration"

### Files
* [clean_config.py](clean_config.py)
* [README.md](README.md)


### Requirements
* Firmware: ExtremeXOS(TM) 15.7 and Newer (tested on 16.1+)
* Platform(s): Any ExtremeXOS switch

## Example

```
X460_TestSwitch.12 # run script clean_config.py
Processing Configuration...
->show configuration

#
# Module devmgr configuration.
#
configure snmp sysName "X460_TestSwitch"
configure snmp sysContact "support@extremenetworks.com, +1 888 257 3000"
configure sys-recovery-level switch reset

#
# Module vlan configuration.
#
configure vlan default delete ports all
configure vr VR-Default delete ports 1-34
configure vr VR-Default add ports 1-34
configure vlan default delete ports 1-34
create vlan "lp"
configure vlan lp tag 1001
enable loopback-mode vlan lp
create vlan "v1"
configure vlan v1 tag 10
create vlan "v3"
configure vlan v3 tag 30
create vlan "x460g2"
configure vlan x460g2 tag 1500
configure vlan v1 add ports 3 tagged  
configure vlan v3 add ports 2 tagged  
configure vlan x460g2 add ports 4 tagged  
configure vlan v1 ipaddress 10.0.0.1 255.255.255.0
enable ipforwarding vlan v1
configure vlan lp ipaddress 192.168.1.1 255.255.255.0
enable ipforwarding vlan lp
configure vlan v3 ipaddress 30.0.0.2 255.255.255.0
enable ipforwarding vlan v3
configure vlan x460g2 ipaddress 172.16.11.1 255.255.255.0
enable ipforwarding vlan x460g2

#
# Module netTools configuration.
#
configure dns-client add name-server 10.1.1.1 vr VR-Default
configure dns-client add name-server 10.1.1.2 vr VR-Default
configure dns-client add domain-suffix extremenetworks.com
enable dhcp vlan Mgmt

#
# Module ospf configuration.
#
configure ospf routerid 192.168.1.1
enable ospf
create ospf area 0.0.0.2
configure ospf add vlan lp area 0.0.0.0
configure ospf add vlan v1 area 0.0.0.2 link-type point-to-point
configure ospf add vlan v3 area 0.0.0.2 link-type point-to-point
configure ospf add vlan x460g2 area 0.0.0.2 link-type point-to-point

#
# Module thttpd configuration.
#
configure ssl certificate hash-algorithm sha512
```

## License
Copyright© 2015, Extreme Networks.  All rights reserved.

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
