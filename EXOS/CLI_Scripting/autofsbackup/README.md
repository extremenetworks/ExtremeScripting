# Automated FS Backup

## Description
Run automated back up on all scripts, including configuration, policy and
scripts. Benefits include a simple rollback and configuration history.

### Files

* [backup.xsf](backup.xsf) - Manual backup script
* [xbd.xsf](xbd.xsf) - The UPM triggered backup script
* [README.md](README.md) - This Readme


### Requirements
* Firmware: ExtremeXOS(TM) 12.3.x or higher
* Platform(s): Any ExtremeXOS switch.
* TFTP Server: IPv4 TFTP Server that allows switch to write files


### Example
In the below example the x250e would upload all files on the switch and a
second file in the root of the tftp for use with the Interactive Recovery script.
```
<x250e running script>	(log entry of AAA.AuthPass triggers UPM)
<x250e running script>	(UPM Runs and uploads current config as c<serial>.cfg)
<x250e running script>	(UPM Recursively uploads all files)
```


### Notes

* This requires a TFTP Server with write privileges by the switch
* This requires a date structure in the TFTP directory (This is currently not implemented!)

```   (e.g. /tftpboot/<year>/<mo>/<day> or /tftpboot/2010/04/27)```


### Updates
1.0 - ( Mar 2009) First Version of the script

1.1 - ( Apr 2010) Changes made to interact with other scripts

1.2 - ( Dec 2017) On backup.xsf: corrcetions to bad syntax, removal of redundant .cfg upload
                  addition of user prompts for tftp IP addr. and VR.


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
