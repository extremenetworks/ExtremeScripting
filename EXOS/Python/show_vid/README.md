# Show vlanID
## Description
This script is a substitute to the "show vlan" command for users that like to see vlans in VID order.

### History
26-Sep-2016 - fixed VLAN flags display to always report flags with correct VLAN name

### Files
* [showvid.py](showvid.py)
* [README.md](README.md)

### Requirements
ExtremeXOS 15.6.2 and later

### Usage
run script showvid.py

optional arguments:
  -h, --help            show this help message and exit
  -v VLAN, --vlan VLAN  VLAN ID range 1,2 or 1-5


### Example 1
```
SWITCH.5 # load sc showvid.py
Collecting information. This may take a moment
-----------------------------------------------------------------------------------------------
 VID Description     Protocol Addr       Flags                         Proto  Ports  Virtual
     /VLAN Name                                                               Active Router
                                                                              /Total
---- --------------- ------------------  ----------------------------  ------ ------ ----------
   1 Default         ------------------  ------------T----------------  ANY    0/1    VR-Default
  10 test10          ------------------  -----------------------------  ANY    0/2    VR-Default
  11 test11          ------------------  -----------------------------  ANY    0/2    VR-Default
  12 test12          ------------------  -----------------------------  ANY    0/2    VR-Default
 666 ISC_MLAG        1.1.1.1/30          ------I----------------------  ANY    0/1    VR-Default
2001 xxx             ------------------                                ANY    0/2    VR-Default
4095 Management VLAN 12.12.12.12/24      -----------------------------  ANY    1/1    VR-Mgmt
-----------------------------------------------------------------------------------------------
Flags : (B) BFD Enabled, (c) 802.1ad customer VLAN, (C) EAPS Control VLAN,
        (d) Dynamically created VLAN, (D) VLAN Admin Disabled,
        (e) CES Configured, (E) ESRP Enabled, (f) IP Forwarding Enabled,
        (F) Learning Disabled, (h) TRILL Enabled, (i) ISIS Enabled,
        (I) Inter-Switch Connection VLAN for MLAG, (k) PTP Configured,
        (l) MPLS Enabled, (L) Loopback Enabled, (m) IPmc Forwarding Enabled,
        (M) Translation Member VLAN or Subscriber VLAN, (n) IP Multinetting Enabled,
        (N) Network Login VLAN, (o) OSPF Enabled, (O) Flooding Disabled,
        (p) PIM Enabled, (P) EAPS protected VLAN, (r) RIP Enabled,
        (R) Sub-VLAN IP Range Configured, (s) Sub-VLAN, (S) Super-VLAN,
        (t) Translation VLAN or Network VLAN, (T) Member of STP Domain,
        (v) VRRP Enabled, (V) VPLS Enabled, (W) VPWS Enabled, (Z) OpenFlow Enabled

```
### Example 2
```
SWITCH.6 # load sc showvid.py -v 1
Collecting information. This may take a moment
-----------------------------------------------------------------------------------------------
 VID Description     Protocol Addr       Flags                         Proto  Ports  Virtual
     /VLAN Name                                                               Active Router
                                                                              /Total
---- --------------- ------------------  ----------------------------  ------ ------ ----------
   1 Default         ------------------  ------------T----------------  ANY    0/1    VR-Default
-----------------------------------------------------------------------------------------------
Flags : (B) BFD Enabled, (c) 802.1ad customer VLAN, (C) EAPS Control VLAN,
        (d) Dynamically created VLAN, (D) VLAN Admin Disabled,
        (e) CES Configured, (E) ESRP Enabled, (f) IP Forwarding Enabled,
        (F) Learning Disabled, (h) TRILL Enabled, (i) ISIS Enabled,
        (I) Inter-Switch Connection VLAN for MLAG, (k) PTP Configured,
        (l) MPLS Enabled, (L) Loopback Enabled, (m) IPmc Forwarding Enabled,
        (M) Translation Member VLAN or Subscriber VLAN, (n) IP Multinetting Enabled,
        (N) Network Login VLAN, (o) OSPF Enabled, (O) Flooding Disabled,
        (p) PIM Enabled, (P) EAPS protected VLAN, (r) RIP Enabled,
        (R) Sub-VLAN IP Range Configured, (s) Sub-VLAN, (S) Super-VLAN,
        (t) Translation VLAN or Network VLAN, (T) Member of STP Domain,
        (v) VRRP Enabled, (V) VPLS Enabled, (W) VPWS Enabled, (Z) OpenFlow Enabled
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
