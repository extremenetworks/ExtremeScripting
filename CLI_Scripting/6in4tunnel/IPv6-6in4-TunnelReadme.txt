*****************************
IPv6 in IPv4 Tunnel
https://marketplace.extremenetworks.com/#details/IPv6_in_IPv4_Tunnel
*****************************

Files:
*****************************
IPv6-6in4-TunnelReadme.txt  - This readme file
IPv6-6in4-Tunnel.xsf        - The script


Infrastructure Requirements
*******************************
Firmware: ExtremeXOS(TM) 12.0 and Newer for xbd.xsf standard
Platform(s): ExtremeXOS based Extreme Networks switches


Description:
*****************************
Configure an IPv6 6-in-4 tunnel between two IPv6 regions bridging
across an IPV4 region on an ExtremeXOS(TM) switch.


Example:
****************************
In this example, Router A is assumed to have an interface to an IPv4 region
with the address 192.168.1.1 (for this example we are using private IPv4
addresses, but to tunnel across the Internet, you would use a public address).
Router B is assumed to have an IPv4 interface of 10.2.0.1. The IPv4 interface
must be created before the tunnel is configured and cannot be deleted until
the tunnel is deleted.  This example has one subnet in each IPv6 region,
2001:db8:1::/64 for Router A and 2001:db8:2::/64 for Router B. Hosts A and B
are configured to use IPv6 addresses 2001:db8:1::101 and 2001:db8:2::101,
respectively.

For traffic to move from one region to the other, there must be a route.
In this example, a static route is created, but you could enable RIPng or
OSPFv3 on the tunnel interface.  In this example, we assume that the
IPv4 network can route from Router A to Router B (in other words, some
IPv4 routing protocol is running on the public-ipv4 interfaces). For
platforms on which hardware based tunneling is supported, IPv4 forwarding
needs to be enabled on the tunnel source VLAN. However, in platforms on
which IPv6-in-IPv4 tunnels are supported in software only, you do not need
to enable IPv4 forwarding on the public interfaces in this example unless
you are also routing IPv4 traffic on them (in this example, it is assumed
you are running no IPv4 traffic inside your respective IPv6 networks,
although you could).  When Host A needs to send a packet to 2001:db8:2::101
(Host B), it forwards it to Router A. Router A receives an IPv6 packet from
the IPv6 source address 2001:db8:1::101 to the destination 2001:db8:2::101.
Router A has the static route, for the route 2001:db8:2::/64 with next hop
2001:db8:a::2 (Router B) through the tunnel interface. So Router A
encapsulates the IPv6 packet inside an IPv4 header with the source address
192.168.1.1 and destination address 10.2.0.1. The encapsulated IPv6 packet
passes through the IPv4 network and reaches the other end of the tunnel -
Router B. Router B decapsulates the packet and removes the IPv4 header.
Router B then forwards the IPv6 packet to the destination host - Host B.

The following functions are performed in this example:

1. IPv4 VLAN creation and configuration

2. 6in4 tunnel creation, configuration and enabling

3. IPV6 VLAN creation, configuration and enabling

4. IPV6 address configuration and enabling


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