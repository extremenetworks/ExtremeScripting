*****************************
Auto-VLAN Provision EDP
https://marketplace.extremenetworks.com/#details/Auto_VLAN_Provision_EDP
*****************************

Files:
*****************************
avp.xsf         - The Core Script
avp-Readme.txt	- This Readme
avpdefault.xsf	- Auto-VLAN Provision Deployed as a default.xsf script and
                  using UPM from a Script

Infrastructure Requirements
*******************************
Firmware: ExtremeXOS(TM) 12.3.x and Newer for avp.xsf standard
Firmware: ExtremeXOS 12.4.x and Newer for avpdefault.xsf expanded
Platform(s): Any ExtremeXOS switch. 

Description: 
*****************************
This script will auto-configure an edge switch based on the ports seen on the
uplink port. The script will initially show EDP to find the VLAN, VLAN ID and
port that will be connected to the uplink.  The script will then create a VLAN,
configure it with VLAN ID and add the port tagged or untagged as necessary.

Example: 
****************************
<x250e running script>	 (sends edp query) ----> <x450a with VLAN: EDP_TEST TAG 2010>
<x450a with VLAN: EDP_TEST TAG 2010> (replies with EDP PDU) ---> <x250e running script>
<x250e running script> (Parses EDP output and configures switch)

In the above example the x250e running the applet would automatically configure
its upliknk with VLAN: EDP_TEST with a tag of 2010.


Notes:
*******************************
 - This requires a unique VLAN on the EDP uplink port that a switch running
   this script can see.
 - This version will only provision the first VLAN. Multiple VLANs are ignored.
 - The avpdefault.xsf will need to be renamed to default.xsf for ExtremeXOS
   to to use it when a configuration file is not selected. For more information
   please see the ExtremeXOS Concepts guide.

1.0 - (19 April 2010) First Version of the script

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