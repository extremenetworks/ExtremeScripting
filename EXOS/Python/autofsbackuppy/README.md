# Automated FS Backup

## Description

Run automated back up on all scripts, including configuration, policy and scripts. 
Benefits include a simple rollback and configuration history.

### Files
* [DailyBackup.py](DailyBackup.py)
* [README.md](README.md)

### Requirements
* Firmware: ExtremeXOS(TM) 15.5.2 and Newer
* Platform(s): Any ExtremeXOS switch

## Examples
DailyBackup.py</br>
log entry of AAA.AuthPass triggers UPM</br>
UPM Runs and uploads current config as `c<serial>.cfg`</br>
UPM Recursively uploads all files

In the above example the x250e would upload all files on the switch and a second file 
in the root of the tftp for use with the Interactive Recovery script.

## Notes

The first time this script runs, it installs itself into UPM to be called once a day.
* This requires a TFTP Server with write privileges by the switch
* This requires a date structure in the TFTP directory
(e.g. `/tftpboot/<year>/<mo>/<day>` or `/tftpboot/2010/04/27`)

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
