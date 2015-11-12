# Firmware Version Check

## Description
Allows for automatic firmware version validation at bootup. When a switch boots,
this script matches the configured-firmware-version with the correct-firmware
setting.  If the configured-firmware setting is off, it is corrected with the
switch boot-up.

### Files
* [fwvc.xsf](fwvc.xsf) 	-  The Core Script
[README.md](README.md)	-  This Readme

### Requirements
* Firmware: ExtremeXOS(TM) 12.3.x and Newer for fwvc.xsf standard
* Platform(s): Any ExtremeXOS switch.
* TFTP Server

###Example
In the below example the x650 switch would check its firmware version against
a pre-set supported version. If the incorrect version was detected upon boot,
this would be corrected and switch (if selected) would reboot itself.
```
<x650 loaded with autoexec.xsf> (switch examines correct firmware)
<x650 loaded with autoexec.xsf> (If incorrect downloads correct image)
<x650 loaded with autoexec.xsf> (Option to reboot switch)
```



### Notes

* This requires a TFTP server
* This requires pre-setting correct firmware version in the script
* For automation the script should be copied into a default.xsf and or an autoexec.xsf

### Updates
* 1.0 - (7 Feb 2010) First Version of the script

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