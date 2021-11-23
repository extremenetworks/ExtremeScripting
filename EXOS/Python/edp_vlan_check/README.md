# Local and remote port VLAN check for EXOS

## Description

This Script uses EDP to check if the local and remote port have the same vlans added to the ports.  EDP needs to be enabled on both sides of the link for the script to work.

## Files

* [edp_vlan_check](edp_vlan_check.py)
* [README.md](README.md)


### Requirements
* Firmware: ExtremeXOS(TM) 15.6
* This script was tested on 15.6 and older.

### Features
* This Script Checkes local and remote port vlan configurations to check to see if they Match. 
* The script does not check to see if the vlans are tagged or untagged on the port.
 

### How to use
* Run the script on a switch with EXOS 15.6 and higher.

##### Switch script example

```
Switch# load sc edp_vlan_check.py
What port would you like to check?: 2

Local port 2 and/or remote port 1:2 configurations do NOT match!!!

Please add the below vlans to port 2.
['SYS_VLAN_0002', 'SYS_VLAN_2051', 'SYS_VLAN_2200', 'SYS_VLAN_2201', 'SYS_VLAN_2202', 'SYS_VLAN_2204']

Please add the below vlans to the remote port 1:2.
['SYS_VLAN_0010', 'SYS_VLAN_0011', 'SYS_VLAN_0012', 'Data']

Switch# # load sc edp_vlan_check.py
What port would you like to check?: 1:11

Local and remote port vlan configurations match.

```

## License
Copyright© 2015, Extreme Networks
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

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).

>Be Extreme
