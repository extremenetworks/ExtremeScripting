# Wipe SNMP configuration

## Description
This widget provides a method of deleting the SNMP configuration a switch and creating an SNMPv3 configuration.

### Files
* [configSNMP.py](configSNMP.py)
* [README.md](README.md)


### Requirements
* Firmware: ExtremeXOS(TM) 15.6 and Newer
* Platform(s): Any ExtremeXOS switch

## Example
```
* X460G2-48t-G4.119 # run script configSNMP -h
usage: SNMPtogether.py [-h] [-d] [-c]

This script can configure SNMPv3 and remove SNMPv3 configuration

optional arguments:
  -h, --help       show this help message and exit
  -d, --delete     removes SNMPv3 Configuration
  -c, --configure  configures SNMPv3 Configuration
* X460G2-48t-G4.120 # run script configSNMP -c
Please enter your SNMPv3 User name: foo
Please enter your SNMPv3 User password (7 to 49 char): foopassword
Please enter your SNMPv3 privacy password (7 to 49 char): fooprivacy
Please enter your SNMPv3 Group name: foogroup
Please enter your SNMPv3 Access preferences: admin
Would you like to disable SNMP v1v2c access?(yes or no): yes
Would you like to disable the default SNMPv3 user?(yes or no): yes
Would you like to disable the default SNMPv3 group? (yes or no): yes

SNMPv3 has been configured successfully
* X460G2-48t-G4.121 # run script configSNMP -d
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

Deletion of SNMP configuration completed successfully.
* X460G2-48t-G4.122 #
```

## Notes:
### For SNMP configuration deletion

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

### For SNMPv3 configuration

Specifically, this widget performs the following functions:

1. Asks the user for the SNMPv3 user name
2. Asks the user for the SNMPv3 user password
3. Asks the user for the SNMPv3 privacy (encryption) password
4. Asks the user for the preconfigured access profile
5. Asks the user if they would like to disable SNMP v1v2c access
6. Asks the user if they would like to disable the default SNMPv3 user
7. Asks the user if they would like to disable the default SNMPv3 group

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