# Legacy SNMPv1v2

### Description
This script provides an example of SNMP V1/V2 configuration for
an ExtremeXOS(TM) switch.

This script is a simple example of how one might go about configuring
SNMP V1/V2 on an ExtremeXOS switch.  The script can be used to enable
or disable SNMP V1/V2 access.  The script shows how to specify the
optional name, location and contact information.  The SNMP V1/V2 trap
receivers can optionally be created and configured.  Lastly, tailored
read-write and read-only community strings can be configured and the
default read-write and read-only community strings can be deleted from
the switch.

Specifically, this example performs the following functions:

1. Configures SNMP V1/V2 switch name, location and contact information

2. Optionally creates trap receivers

3. Optionally creates tailored read-write and read-only community strings

4. Optionally deletes read-write and read-only community strings

### Files

* [README.md](README.md)    - This readme file
[SNMPv1v2Config.xsf](SNMPv1v2Config.xsf)          - The script


### Requirements
* Firmware: ExtremeXOS(TM) 12.0
* Platform(s): Any ExtremeXOS switch.

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