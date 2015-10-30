#Chassis Hibernation

##Description
Administrators can use the chassis hibernation script to save energy by setting up a profile that defines when they would like the system to place specified blades into a standby state.  The administrator must specify when and which blades are enabled for this power saving.

###Files
* [chassishibernate.xsf](chassishibernate.xsf) 	-  The Core Script
* [README.md](README.md)		-  This Readme

### Requirements

* Firmware: ExtremeXOS(TM) 11.6.x and Newer for chassishibernation.xsf standard
* Platform(s): BD8806/8810 (Not blade dependent)


### Example
In the below example the UPM, based on configured time of day, will disable  and enable BD8806 Blades for power conservation.
```
<BD8806 Running UPM> (6AM Timer Triggers and Enables Blades)
<BD8806 Running UPM> (10PM Timer Triggers and Disables Blades)
```

### Notes
* Configuring time of day is required

### Updates
* 1.0 - (19 April 2010) First Version of the script

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