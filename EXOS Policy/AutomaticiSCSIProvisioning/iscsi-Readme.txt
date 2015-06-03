*****************************
iSCSI Auto-provisioning
https://marketplace.extremenetworks.com/#details/iSCSI_Auto_provisioning
*****************************


Files:
*****************************
iscsi.pol 		-  The Example policy file
iscsi-Readme.txt	-  This Readme


Infrastructure Requirements
*******************************
Firmware: ExtremeXOS(TM) 11.6.x and Newer for iscsi.pol standard
Platform(s): Summit Series; BlackDiamond 8800, 8900-series, 8900-XL series,
             BlackDiamond BDX


Description:
*****************************
This simple script uses CLEAR-Flow to identify iSCSI traffic (port 3260),
assign it the right Quality of Service, and enable jumbo frames.
This pre-provisioned settings in a network allows iSCSI traffic to be
protected in a higher priority queue.


Example:
****************************
<X650 Running CLEAR-FLow policy> (Rule becomes true)
<X650 Running CLEAR-FLow policy> (CLEAR-Flow takes configured actions
                                  (e.g. QoS Provision))


In the above example the rule becomes true and CLEAR-Flow executes its actions
automatically.


Notes:
*******************************
- This requires a CLEAR-Flow enabled switch

1.0 - (1 April 2010) First Version of the script
1.1 - (17 April 2012) Version tested for xKit


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