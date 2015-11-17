# PoE fault disable via UPM

## Description
This script sets up two UPM profiles. The first monitors the log for a PoE port entering the faulted state. When this occurs, the UPM profile disables inline-power to this port.

The second UPM profile monitors the log for link down events. When one occurs, the UPM profile re-enables inline-power on the port.

###Files
* [README.md](README.md)
* [poe_upm.xsf](poe_upm.xsf)


### Requirements
* Firmware: ExtremeXOS(TM) 15.3 and newer
* Platform(s): ExtremeXOS(TM) based Extreme Networks switches with PoE support
* License: Edge or higher (for UPM support)


### Example

### Notes
This is intended for use when legacy inline-power is enabled. When this is enabled, non-PoE devices may have power delivered to them by the switch, leading to the port entering a fault state until PoE is reset on this port. This script will detect a device entering this state and disable PoE to that port. When the device connected is removed, the UPM script for link down will be triggered, re-enabling PoE to that port.

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
