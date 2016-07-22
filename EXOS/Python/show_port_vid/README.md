# Show Port VID

## Description
This script displays the VLAN assignment and tagging configuration for all or sellected ports on the switch.  You can also see vlan descriptions.

### Files
* [showportvid.py](showportvid.py)
* [README.md](README.md)

### Requirements
ExtremeXOS 15.6.2 and later

### Usage
```
Switch#run script showportvid.py -h
usage: showportvid [-h] [-p PORTS] [-P] [-n] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to display. Default is all ports
  -P, --port_numbers    Only show port numbers. Default: show port display
                        string
  -n, --names           VLANs are displayed in name order. Default: VID order
  -d, --description     Show VLAN description 
```


### Example 1
```
Switch# run script showportvid.py -d -p 1-5
         Untagged
Port     /Tagged   VID VLAN Name            VLAN Description
-------- -------- ---- -------------------- ------------------------------------
LongDisplayStringFor
         Untagged    1 Default
         Tagged     30 VLAN_0030            Finance
                    31 VLAN_0031
                    32 VLAN_0032            Engineering II
                    33 VLAN_0033            Here is an example of a very long
                                            VLAN description. The usr can
                    34 VLAN_0034
                    40 VLAN_0040
                    41 VLAN_0041            Carries heavy traffic between
                                            Building 17 and Building 2
                    42 VLAN_0042            123456789012345678901234567890123456
                                            7890123456789012345678901234
                    43 VLAN_0043
                    44 VLAN_0044
                    45 VLAN_0045
                  1000 BigData
2        None          None
12345678901234567890
         Untagged    1 Default
         Tagged     30 VLAN_0030            Finance
                    31 VLAN_0031
                    32 VLAN_0032            Engineering II
                    33 VLAN_0033            Here is an example of a very long
                                            VLAN description. The usr can
                    34 VLAN_0034
                    40 VLAN_0040
                    41 VLAN_0041            Carries heavy traffic between
                                            Building 17 and Building 2
                    42 VLAN_0042            123456789012345678901234567890123456
                                            7890123456789012345678901234
                    43 VLAN_0043
                    44 VLAN_0044
                    45 VLAN_0045
                  1000 BigData
4        Untagged    1 Default
         Tagged     30 VLAN_0030            Finance
                    31 VLAN_0031
                    32 VLAN_0032            Engineering II
                    33 VLAN_0033            Here is an example of a very long
                                            VLAN description. The usr can
                    34 VLAN_0034
5        Untagged      None
         Tagged     30 VLAN_0030            Finance
                    31 VLAN_0031
                    32 VLAN_0032            Engineering II
                    33 VLAN_0033            Here is an example of a very long
                                            VLAN description. The usr can
                    34 VLAN_0034
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
