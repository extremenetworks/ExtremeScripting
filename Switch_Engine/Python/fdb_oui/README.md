# FDB OUI

## Description
This Python script scans the FDB table and reports the vendor of the device
connected based on known MAC OUI values

### Files
* [fdb_oui.py](fdb_oui.py)
* [README.md](README.md)

### Requirements
* Firmware: ExtremeXOS(TM) 15.6+
* Platform(s): Any ExtremeXOS switch

Example
```
# run script fdb_oui.py

Extreme Networks device with MAC address 00:01:30:10:3b:1c on port 1
Extreme Networks device with MAC address 00:04:96:1d:93:a4 on port 3
Unknown device with MAC address 00:09:9b:01:8d:75 on port 6
VMWare device with MAC address 00:0c:29:18:a9:43 on port 7
Unknown device with MAC address 00:10:18:d4:af:24 on port 8
Enterasys Networks device with MAC address 00:11:88:f1:a2:10 on port 11
Unknown device with MAC address 00:c0:dd:1b:60:5c on port 19
Unknown device with MAC address 78:2b:cb:46:55:dd on port 22
Dell device with MAC address 84:2b:2b:5f:e6:e1 on port 18
Dell device with MAC address 84:2b:2b:5f:e6:e9 on port 18
Dell device with MAC address 84:2b:2b:61:73:e0 on port 8

```

## Notes
The "known" OUI List is not intended to be comprehensive.

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
