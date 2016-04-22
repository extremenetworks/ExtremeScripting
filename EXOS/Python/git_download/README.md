# GitHub Python Script Downloader

## Description
This tool runs on a EXOS switch running 21.1+ and displays all python scripts on GitHub and allows you to download the scripts directly to your switch.  git_download.py will only access the Internet through VR-Default and VR-Mgmt right now.
  
Note: Make sure your switch has DNS configured, and has Internet access before using.

### Files
* [git_download.py](git_download.py)
* [README.md](README.md)

### Requirements
* ExtremeXOS 21.1+
* Switch must have Internet access
* DNS client configured
```configure dns-client add name-server <DNS IP> vr <vr name>```

### Usage
run script git_download.py


### Example
```
Switch# run script git_download.py

Internet Connection found on VR-Mgmt
Script:                             Description:
------------------------------------------------
 1: autofsbackup                     Runs automated back up on all scripts, including configuration, policy and scripts.
 2: cleanswitch                      Provides a method of deleting all configuration parameters and files from an EXOS switch.
 3: command watch                    Simple script that repeats a CLI command every *n* seconds
 4: eaps_checker                     This script will check eaps config and status from a PC/Server.
 5: edp_and_port_vlan_check          This Script uses EDP to check if the local and remote port have the same vlans added to the ports.
 6: enablefeaturescheck              Identifies the features enabled on a switch
 7: Email_event                      This EXOS script will send an email when an event is logged
 8: fdb_oui                          Scans the FDB table and reports the vendor of the device connected.
 9: flowtracker                      Creates a dynamic ACL to count packets.
10: mlag_config_check                Checks to ensure that all VLANs on MLAG ports are also present on the ISC.
11: non_stacking_config_converter    Converts a non stacking configuration to a stacking configuration.
12: qosconfig                        Wizard to aid in creating QoS profiles
13: radiusmgmtconfig                 Wizard for configuring an ExtremeXOS
14: radiusnetloginconfig             Wizard for configuring an ExtremeXOS
15: show_config_clean                Hides unused config sections from the output of "show configuration"
16: snmpv1v2config                   Wizard for SNMP V1/V2 configuration for an ExtremeXOS
17: sntpconfig                       Example for Simple Network Time Protocol 
18: vlanPortInfo                     This script displays the VLAN assignment and tagging configuration for all ports on the switch.
19: vlan_elrp_check                  This script will run ELRP on all VLANS on an EXOS switch.
20: vlan_copy_port                   This EXOS script will copy/move vlans from one port to another.
What script would you like to download? 20

By downloading this file you agree to the License
Terms in the readme, available at the URL below.

https://github.com/extremenetworks/ExtremeScripting/blob/master/EXOS/Python/vlan_copy_port/README.md

vlan_copy_port.py was downloaded to /usr/local/cfg/.
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
