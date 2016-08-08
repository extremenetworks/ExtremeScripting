# Create and delete SNMPv3 configuration

## Description
This widget provides a method of deleting and creating the SNMP configuration of a switch.

### Files
* [snmpassist.py](snmpassist.py)
* [README.md](README.md)


### Requirements
* Tested on 21.1.1.4
* Platform(s): Any ExtremeXOS switch

## Example
```
* X440G2-12t8fxG4.13 # run script snmpassist
Would you like to (D)elete or (C)onfigure SNMPv3? d
This script will completely delete the currently existing SNMPv3 configuration. Are you sure you wish to do this? (y/n): y
Deleting SNMP configuration...
Deleting trap receivers...
Deleting notification logs...
Deleting non-default SNMPv3 groups
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
Deleting groups...
Enabling SNMPv3 default group...
Enabling SNMPv3 default user...

SNMP configuration has been deleted.

* X440G2-12t8fxG4.16 # run script snmpassist
Would you like to (D)elete or (C)onfigure SNMPv3? c
Please enter your SNMPv3 User name: extreme
Please enter your SNMPv3 User password (8 to 49 char): be3xtr3m3
Please enter your SNMPv3 privacy password (8 to 49 char): be3xtr3m3
Please enter your authentication type (SHA/MD5): MD5
Please enter your encryption type (3DES, AES, DES, HEX): AES

SSH2 must be enabled to configure privacy type as AES. If you choose to 
enable it, key generation can take 10-15 minutes to complete and the 
CLI will be unavailable during that time. 
Would you like to enable it? (y/n): y
After running the script, please restart process snmpMaster and snmpSubagent

SNMP Group name is used to link multiple SNMP users together. Its not something that Netsight/ExtremeControl asks for.
Please enter your SNMPv3 Group name: v3group
Please enter your SNMPv3 Access preferences: adminaccess
Would you like to disable SNMP v1v2c access? (y/n): y
Would you like to disable the default SNMPv3 user? (y/n): y
Would you like to disable the default SNMPv3 group? (y/n): y
SNMPv3 configuration has been completed
* X440G2-12t8fxG4.16 # 
```

## Notes:

The Delete portion of the script does the following:

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

The Configure portion of the scripts asks a series of questions relating to the user name, group configuration, and access profile information. 
The configure portion of the script also asks the user if they want to disable SNMP v1v2c access, disable the default SNMPv3 user, and disable 
the default SNMPV3 group.

In order to use 3DES or AES encryption, the SSH module is required to be installed, configured, and enabled. The script will automatically check to see if SSH is enabled.
If running EXOS version 21 or later, The switch will enable SSH for you. If running EXOS version 16 or earlier, and SSH is not enabled, the switch will prompt the user to
download SSH from https://support.extremenetworks.com .

In this current iteration, this script does not:

1. Reset SNMPv3 access profiles


## License
Copyright© 2016, Extreme Networks.  All rights reserved.

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