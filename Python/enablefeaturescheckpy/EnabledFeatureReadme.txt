
*****************************
List Enabled Features
https://marketplace.extremenetworks.com/#details/List_Enabled_Features_Py
*****************************

Files:
*****************************
EnabledFeatures.py          -  The Core Script
EnabledFeaturesReadme.txt	-  This Readme


Infrastructure Requirements
*******************************
Firmware: ExtremeXOS(TM) 12.1 and Newer
Platform(s): Any ExtremeXOS switch.


Description:
*****************************
This Python script identifies the features enabled on a switch.  The list
of features is discovered by a series of if/then else statements and includes
most of the common features that may be enabled by a switch.  This list does
not include all possible features of a switch and may be modified to
include the unique features running on your network.


Example:
****************************
EnabledFeatures.py

Example output looks like:
RADIUS                : disabled
TACACS                : disabled
Access List(s)        : None Configured
BGP                   : disabled
Configuration logging : disabled
CLI scripting         : enabled
EAPS                  : disabled
EDP                   : disabled
ELRP                  : disabled
ELSM                  : disabled
Debug Mode            : disabled
ESRP                  : disabled
IPARP                 : enabled
IGMP Snooping         : enabled
MLD                   : disabled
MVR                   : disabled
MSDP                  : disabled
NetLogin              : disabled
OSPF                  : disabled
OSPFv3                : disabled
PIM                   : disabled
RIP                   : disabled
RIPNG                 : disabled
IP route sharing      : enabled
SNMP                  : enabled
Spanning Tree         : disabled
Telnet                : enabled
Web mode HTTP         : enabled
Web mode HTTPS        : disabled
VLAN(s)               : created
VMAN(s)               : created

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
