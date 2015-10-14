Easy tool to apply ACL counters to troubleshoot packet loss and identify flows
*****************************

Files:
*****************************
flowtrack.py 	-  The Core Python Script
FlowtrackReadme.txt	-  This Readme

Infrastructure Requirements:
*******************************
Firmware: ExtremeXOS(TM) 15.6

Description:
*****************************
Flowtrack was created to help in troubleshooting packet loss on Extreme Networks Switches.
This script can only be ran on EXOS switches running 15.6 and newer.
It easily creates dynamic ACL counters that count traffic that the user has select to match on.
If the Flow_track ACL already exist then the script will remove it for easy ACL changing.

Features:
*****************************
* Source and/or Destination MAC address matching 48 mask only
* Source and/or Destination IP address matching 32 mask only
* Ingress and Egress ACL counter direction
* Apply ACL counter to a port group
* protocol icmp matching with "-p icmp" option
* ACL removal with -r option
* Allows for '-' or ':' delimited MAC addresses.
* Only support static ACL and counter called "Flow_track"
* If the Flow_track ACL already exist then the script will remove it for easy ACL changing.

Example Commands:
*****************************
```
run script flowtrack.py -sm 11:11:11:11:11:11 -dm 11-11-11-11-11-11  -p icmp -i 22
run script flowtrack.py -dm 11-11-11-11-11-11 -i 22
run script flowtrack.py -dm 11-11-11-11-11-11 -i 22 -e
run script flowtrack.py -sip 4.4.4.4 -dip 2.2.2.2 -i 22
run script flowtrack.py -sip 4.4.4.4 -p icmp -i 22
run script flowtrack.py -dip 4.4.4.4 -p icmp -i 1-10,15
run script flowtrack.py -dip 4.4.4.4 -p icmp -i 1-10,15 -e
run script flowtrack.py -r
run script flowtrack.py -h
```

Command Help:
*****************************
```
X450G2-48p-10G4.55 # run script flowtrack.py -h

usage: flowtrack.py [-h] [-r] [-p [PROTOCOL]] [-sm [SOURCE_MAC]]
                    [-dm [DESTINATION_MAC]] [-sip [SOURCE_IP]]
                    [-dip [DESTINATION_IP]] [-i [INTERFACE]] [-e]

This program is used to create a dynamic acl to count L2 or L3 packets. The
ACL will not deny any traffic. If creating an L3 flow tracker use -i, -sip,
-dip arguments. If creating an L2 flow tracker use -i, -sm, -dm arguments.To
match on ICMP use '-p icmp'. For egress ACL use '-e'

optional arguments:
  -h, --help            show this help message and exit
  -r, --remove          removes all Flow_track ACLs from the switch
  -p [PROTOCOL], --protocol [PROTOCOL]
                        Protocol to match on. ("ICMP") only
  -sm [SOURCE_MAC], --source_mac [SOURCE_MAC]
                        Source MAC address
  -dm [DESTINATION_MAC], --destination_mac [DESTINATION_MAC]
                        Destination MAC address
  -sip [SOURCE_IP], --source_ip [SOURCE_IP]
                        Source IP address
  -dip [DESTINATION_IP], --destination_ip [DESTINATION_IP]
                        Destination IP address
  -i [INTERFACE], --interface [INTERFACE]
                        Switch Port number to apply the ACL counter
  -e, --egress          Make egress ACL (default: ingress)
```
  
Example 1:

```
X460G2-24p-G4.43 # run script flowtrack.py -sip 1.1.1.1 -i 2 -p icmp

+--------------------------------------------------+
|          Removed ACL Flow_track                  |
+--------------------------------------------------+
| Commands used to remove ACL:                     |
| configure access-list delete Flow_track all      |
| delete access-list Flow_track                    |
+--------------------------------------------------+


     L3 ACL applied correctly
_____________________________________
|               ACL                 |
_____________________________________

entry Flow_track {
if match all {
    protocol icmp ;
    source-address 1.1.1.1/32 ;
} then {
    permit  ;
    count Flow_track ;
} }




_____________________________________
|         ACL COUNTER               |
_____________________________________

 Vlan Name        Port   Direction
    Counter Name                   Packet Count         Byte Count
==================================================================
 *                2      ingress
    Flow_track                0



Commands used to apply ACL:
create access-list Flow_track "protocol icmp;source-address 1.1.1.1/32" "permit;count Flow_track"
configure access-list add Flow_track first ports 2 ingress

```

Example 2:

```
X460G2-24p-G4.5 # run script flowtrack.py -sip 1.1.1.1 -dip 2.2.2.2 -i 2


+--------------------------------------------------+
|          Removed ACL Flow_track                  |
+--------------------------------------------------+
| Commands used to remove ACL:                     |
| configure access-list delete Flow_track all      |
| delete access-list Flow_track                    |
+--------------------------------------------------+



     L3 ACL applied correctly
_____________________________________
|               ACL                 |
_____________________________________

entry Flow_track {
if match all {
    protocol icmp ;
    source-address 1.1.1.1/32 ;
    destination-address 2.2.2.2/32 ;
} then {
    permit  ;
    count Flow_track ;
} }




_____________________________________
|         ACL COUNTER               |
_____________________________________

 Vlan Name        Port   Direction
    Counter Name                   Packet Count         Byte Count
==================================================================
 *                2      ingress
    Flow_track                0



Commands used to apply ACL:
create access-list Flow_track "protocol icmp;source-address 1.1.1.1/32;destination-address 2.2.2.2/32" "permit;count Flow_track"
configure access-list add Flow_track first ports 2 ingress

```

Example 3:

```
X460G2-24p-G4.6 # run script flowtrack.py -dm 11-11-11-11-11-11 -sm 22:22:22:22:22:22 -i 2


+--------------------------------------------------+
|          Removed ACL Flow_track                  |
+--------------------------------------------------+
| Commands used to remove ACL:                     |
| configure access-list delete Flow_track all      |
| delete access-list Flow_track                    |
+--------------------------------------------------+



      L2 ACL applied correctly
_____________________________________
|               ACL                 |
_____________________________________

entry Flow_track {
if match all {
    ethernet-source-address 22:22:22:22:22:22 ;
    ethernet-destination-address 11:11:11:11:11:11 ;
} then {
    permit  ;
    count Flow_track ;
} }




_____________________________________
|         ACL COUNTER               |
_____________________________________

 Vlan Name        Port   Direction
    Counter Name                   Packet Count         Byte Count
==================================================================
 *                2      ingress
    Flow_track                0



Commands used to apply ACL:
create access-list Flow_track "ethernet-source-address 22:22:22:22:22:22;ethernet-destination-address 11:11:11:11:11:11" "permit;count Flow_track"
configure access-list add Flow_track first ports 2 ingress
```

License:
*******************************
Copyright (c) 2015, Extreme Networks
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

Support
******************************
The software is provided as is and Extreme has no obligation to provide
maintenance, support, updates, enhancements or modifications.
Any support provided by Extreme is at its sole discretion.
Issues and/or bug fixes may be reported in the Hub:

https://community.extremenetworks.com/extreme

Be Extreme,