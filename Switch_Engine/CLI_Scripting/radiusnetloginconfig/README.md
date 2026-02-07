# RADIUS Netlogin Config

## Description
This script provides an example for configuring an
ExtremeXOS(TM) switch for RADIUS netlogin.

Remote Authentication Dial IN User Service (RADIUS) is a mechanism
for authenticating and centrally administrating access to network
nodes.  The ExtremeXOS RADIUS client information allows authentication
for access to a switch.  In order for ExtremeXOS to provide this
access, RADIUS must be appropriately configured on the switch.  This
example shows how RADIUS netlogin information is applied to an
ExtremeXOS switch.

Specifically, this example performs the following functions:

1. Configures the switch with RADIUS netlogin information

2. Creates and configures a guest VLAN for the RADIUS server

3. Enables RADIUS netlogin for the switch

### Files
[README.md](README.md)  - This readme file
[RADIUSNetloginConfig.xsf](RADIUSNetloginConfig.xsf)        - The script


### Requirements
* Firmware: ExtremeXOS(TM) 12.0
* Platform(s): Any ExtremeXOS switch.

### Notes
The RADIUS Client IP address must be configured in specified virtual router
name (vr-default) for this script to execute properly.

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

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).

>Be Extreme