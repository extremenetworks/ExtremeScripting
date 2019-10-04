# MLAG Config Compare

## Description
This script was made to assist in checking the MLAG configuration between two MLAG peers.  If you run this script on both mlag peers you can take the output of both scripts and run a compare/diff on the two outputs to make sure all vlan configuration is correct.

Note: This script does not support switches with two MLAG peers.

### Files
* [mlag_data_compare.py](mlag_data_compare.py)
* [README.md](README.md)

### Requirements
* Firmware: ExtremeXOS(TM) 15.6+
* Platform(s): Any ExtremeXOS switch

### Example

```
Switch# run script test_mlag.py
###############################
MLAG peer is Core
###############################

KEY:
VLAN Name : VLAN ID : Tag 0/1

----------------------------------
ISC port 1
----------------------------------
Vlan100 : 100 : 1
Vlan101 : 101 : 1
Data : 50 : 1

----------------------------------
ISC port 10
----------------------------------
Vlan100 : 100 : 1
Vlan101 : 101 : 1
Data : 50 : 1
```



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

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).

>Be Extreme
