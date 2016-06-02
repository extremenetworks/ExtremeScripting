# VLAN ELRP check

## Description
This Script will run ELRP on all VLANS on an EXOS switch.  If ELRP is disabled the script will enable it, run ELRP on all vlans and then disable it back.


### Files

* [vlan_elrp_check.py](vlan_elrp_check.py)
* [README.md](README.md)


### Requirements
* Firmware: ExtremeXOS(TM) 15.6
* This script was tested on 15.6 and older.

### Features
* This Scrip will run ELRP on all created vlans.
* If more than 20 vlans Have been created the script will check to make sure you want to run ELRP on all VLANS as it can take a while. 
* If elrp is disabled the script will temporaly enable ELRP during the test and disable it after the script is done.
 

### How to use
* Run the script on a switch with EXOS 15.6 and higher.

##### Switch script example
```
Switch# run script vlan_elrp_check.py


*************************************
* ELRP has been temporarily Enabled *
*************************************


Running ELRP on VLAN Default.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "Default" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



Running ELRP on VLAN ISC_MLAG.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "ISC_MLAG" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



Running ELRP on VLAN Mgmt.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "Mgmt" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



Running ELRP on VLAN V10_C0.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "V10_C0" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



Running ELRP on VLAN V11_C1.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "V11_C1" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



Running ELRP on VLAN V12_C2.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "V12_C2" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



Running ELRP on VLAN v13_C2_1.

Starting ELRP Poll . . .
# NO LOOP DETECTED # --- vlan "v13_C2_1" elrp statistics ---
3 packets transmitted, 0 received, ingress port (nil)



**************
*Cleaning up!*
**************
Ending status of ELRP is: Disabled
Switch# 
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
