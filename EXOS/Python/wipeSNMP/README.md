# Wipe SNMP configuration

## Description
This widget provides a method of deleting the SNMP configuration a switch.

### Files
* [wipeSNMP.py](wipeSNMP.py)
* [README.md](README.md)


### Requirements
* Firmware: ExtremeXOS(TM) 15.6 and Newer
* Platform(s): Any ExtremeXOS switch

## Example
```
* X670G2-72x.8 # run script wipeSNMP
!!!WARNING!!! THIS SCRIPT WILL WIPE ALL SNMP CONFIGURATION ON THE SWITCH!!!
Wipe SNMPv3 settings? (yes or no): yes
Deleting SNMP configuration...
Deleting trap receivers...
Deleting notification logs...
Deleting non-default SNMPv3 access profiles...
Deleting non-default SNMPv3 communities...
Deleting filters...
Deleting filter profiles...
Deleting non-default mib views...
Deleting non-default notify configurations...
Deleting notify target addresses...
Deleting target parameters...
Deleting non-default SNMPv3 users...
Deleting non-default communities...
Deleting SNMP readonly communities...
Enabling SNMPv3 default group...
Enabling SNMPv3 default user...
Deletion of SNMP configuration completed successfully.
* X670G2-72x.9 # 

```

## Notes:

Specifically, this widget performs the following functions:


1.  Delete trap receivers
2.  Delete notification logs
3.  Delete non-default SNMPv3 access profiles
4.  Delete non-default SNMPv3 communities
5.  Delete filters
6.  Delete filter profiles
7.  Delete non-default mib views
8.  Delete non-default notify configurations
9.  Delete notify target addresses
10. Delete target parameters
11. Delete non-default SNMPv3 users
12. Delete non-default communities
13. Delete SNMP readonly communities
14. Enable SNMPv3 default group
15. Enable SNMPv3 default user

In this current iteration, this script does not:

1. Reset SNMPv3 access profiles


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