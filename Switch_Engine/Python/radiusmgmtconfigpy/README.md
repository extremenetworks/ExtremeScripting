# RADIUS Mgmt Config

## Description

This script provides a wizard for configuring an ExtremeXOS(TM) switch with RADIUS management information.

Remote Authentication Dial IN User Service (RADIUS) is a mechanism
for authenticating and centrally administrating access to network
nodes.  The ExtremeXOS RADIUS client information allows authentication
for access to a switch.  In order for ExtremeXOS to provide this
access, RADIUS must be appropriately configured on the switch.  This
example shows how RADIUS management information is applied to an
ExtremeXOS switch.

Specifically, this example performs the following functions:
1. Configures the switch with RADIUS server and client IP addresses
2. Sets the RADIUS server password and encryption mechanism specification
3. Enables RADIUS server management access for the switch

### Files
* [RADIUSMgmtConfig.py](RADIUSMgmtConfig.py)
* [README.md](README.md)


### Requirements
* Firmware: ExtremeXOS(TM) 15.6+
* Platform(s): Any ExtremeXOS switch


## Example


## Notes

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
