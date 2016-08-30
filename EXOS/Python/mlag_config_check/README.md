# MLAG Config Check

## Description
This script will check a switch's MLAG config to ensure that there is only one port in the ISC
vlan, all vlans added to MLAG port also exist on the ISC port, and that all MLAG and ISC ports 
are active (and added to the aggregator if in a LAG).  

If a VLAN is not present on the ISC an option to auto-correct the configuration is provided

The tool also now supports multi-peer MLAG

This does not ensure that the tagging on vlans matches across MLAG peers.

### Files
* [mlag_config_check.py](https://raw.githubusercontent.com/extremenetworks/ExtremeScripting/master/EXOS/Python/mlag_config_check/mlag_config_check.py)
* [README.md](README.md)

### Requirements
* Firmware: ExtremeXOS(TM) 15.6+
* Platform(s): Any ExtremeXOS switch

### Example

Correct MLAG configuration:
```
 PEER_2.152 # run script mlag_config_check.py

>> Checking MLAG Configuration and Status...

>> Checking MLAG Peer "PEER_1"...
No problems found on peer "PEER_1"

>> Checking MLAG Peer "PEER_3"...
No problems found on peer "PEER_3"

>> MLAG config check completed.
```

Incorrect MLAG configuration:
```
* PEER_2.142 # run script mlag_config_check.py

>> Checking MLAG Configuration and Status...

>> Checking MLAG Peer "PEER_1"...
>> CONFIG ERROR: Port 2, a LAG member of the ISC for peer PEER_1, is down.  Please resolve.
>> CONFIG ERROR: MLAG port 6 for peer PEER_1 is down.  Please resolve.
>> CONFIG ERROR: VLAN VLAN_0100 is found on an MLAG port but not added to ISC port 1
>> CONFIG ERROR: VLAN VLAN_0200 is found on an MLAG port but not added to ISC port 1
>> Would you like to add the missing vlans to the ISC? (y/n)

>> Checking MLAG Peer "PEER_3"...
>> CONFIG ERROR: ISC for PEER_3 is not a LAG.  It is recommended that all ISC connections use link aggregation
>> CONFIG ERROR: ISC port 3 for Peer PEER_3 not active. Please resolve.

>> MLAG config check completed.
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
