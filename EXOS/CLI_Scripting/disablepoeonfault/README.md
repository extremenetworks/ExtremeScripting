# Disable PoE ports on fault

## Description
This script will set up two UPM profiles on an ExtremeXOS(TM) switch.

The first UPM profile will monitor the log for any ports entering a PoE fault state. When a port enters the fault state, PoE will be disabled on this port.

The second UPM profile will monitor the log for port link down events. When this occurs, the UPM profile will enable PoE on this port.

### Files
* [poe_upm.xsf](poe_upm.xsf)
* [README.md](README.md)

### Requirements
* Firmware: ExtremeXOS(TM) 15.3 or higher
* Platform(s): Any ExtremeXOS switch with PoE support
* License: Edge or higher

## Example

## Notes

The intended use for this script is when using legacy inline-power. When this is enabled, the switch may attempt to deliver power to non-PoE devices. When this occurs, the port will often fault, and remain faulted until PoE is reset on the port. By running this script, the port will automatically have PoE disabled when it enters the fault state, and will re-enable PoE when the device on that port is disconnected.

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
