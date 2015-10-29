*****************************
IPv6 Unicast Config
https://marketplace.extremenetworks.com/#details/IPv6_Unicast_Config
*****************************

Files:
*****************************
IPv6UnicaseConfigReadme.txt
IPv6UnicaseConfig.xsf - Script file


Infrastructure Requirements
*******************************
ExtremeXOS(TM) 12.1 or greater
ExtremeXOS based Extreme Networks switches


Description:
*****************************
This script provides an example of IPv6 unicast routing in
ExtremeXOS(TM).


Example:
****************************
In this example, assume there are three VLANS to be configured on
a BlackDiamond(TM) switch - a protocol-sensitive VLAN using IPv6
addressing ("vlan1"), a protocol-sensistive VLAN using IPv6 addressing
("vlan2"), and a port-based VLAN handling all other traffic ("vlan3").

The first IPv6 VLAN, "vlan1", is to be assigned all ports on slots 1 and
3 with the IP address of "2001:db8:35::1/48", while the other IPv6 VLAN,
"vlan2", is to be assigned all ports on slots 2 and 4 with the IP address
of "2001:db8:36::1/48".  Finally, the third VLAN, "vlan3", is assigned to
slots 1 through 4 on this BlackDiamond switch.

The devices connected to the network generate a combination of IPv6
traffic and other forms of traffic (e.g., NetBIOS).  The IPv6 traffic is
filtered by the protocol-sensitive VLANs, while all other traffic is
directed to VLAN "vlan3".

Thus, in this configuration, all IPv6 traffic from devices connected to
slots 1 and 3 have access to the router by way of VLAN "vlan1".  Ports on
slots 2 and 4 reach the router by way of VLAN "vlan2". All other traffic
(NetBIOS) is part of the VLAN "vlan3".

The following functions are performed in this example:

1. Create three VLANS - "vlan1", "vlan2", and "vlan3"

2. Configure "vlan1" and "vlan2" for IPv6

3. Provide the port congiuration for all the VLANs

4. Configure the IP addresses for "vlan1" and "vlan2"

5. Configure ripng for "vlan1" and "vlan2"

6. Enable IPv6 forwarding

7. Enable ripng


Notes:
*******************************


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