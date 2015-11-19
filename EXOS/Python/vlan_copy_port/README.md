# Vlan copy port script
This tool needs to be run on an EXOS switch and will copy all vlans and vmans from one port to another.

### Description
This script will take the exact vlan config of 1 port and copy that to another port. After that it asks if the port where the vlans are copied from need to be cleaned (move)

**Please review the configuration before loading the configuration on a switch**

### Files
* [The Core Python Script - vlan_copy_port.py](vlan_copy_port.py)
* [README.md](README.md)


### Requirements
Firmware: ExtremeXOS(TM)
This script was tested on 15.7 and 16.1.

### Features
* This Script can be run on EXOS.
 

### How to use
* Copy the script to the switch
* run the script with options -s (source port) and -d (destination port)

## EXOS run example:
```
* X460-48t.4 # run script vlan_copy_port -s 5 -d 6
Do you want to delete all vlans from port 5 (y/N) ? y
Deleting vlans from port 5.
* X460-48t.5 #

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

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).

>Be Extreme
