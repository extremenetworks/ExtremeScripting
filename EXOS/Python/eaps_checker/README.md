# check_eaps
This script runs from a server/PC with python installed and check the eaps config and status of one or more switches

### Description
This script will connect to every switch IP given in the file when used with -f or checks only 1 switch when used with -s.
It will check the eaps config if all vlans are added correctly to the ring ports and will also check if there are vlans added 
to the ring ports that are not protected by eaps that could possibly cause loops.
If the option --vpif is used it will check the vpif state for every Eaps master domain on the secondary port for domain vlans.

### Files
* [The Core Python Script - check_eaps.py](check_eaps.py)
* [README.md](README.md)


### Requirements
Firmware: ExtremeXOS(TM)
Following pyhton libraries are needed (most standard included in python):
  import telnetlib
  import re
  import argparse
  import sys
  import paramiko
  
  Paramiko is for SSH connection to the switch. This only works with the latest version of paramiko, please update this to the latest.
  Using PIP the command would be pip install --upgrade paramiko

### Features
* This Script runs from a remote server/PC, tested with python 2.7.

### How to use
* Copy the script to your server/PC 
* run the script with options -s <switch IP> or -f <file>. The file should contain an IP address per line.
* Other options:
 -u <username> 
 -p <password>
 --ssh (Use SSH)
 --vpif (Check vpif state on Eaps master secondary port)

## run example:
```
okoot@okoot-ubuntu:~/work/check_eaps$ ./check_eaps.py -h
usage: check_eaps.py [-h] [-s SWITCH] [-u USER] [-p PASSWORD] [-f FILE]
                     [--ssh] [--vpif]

Connect to switch and check Eaps config

optional arguments:
  -h, --help   show this help message and exit
  -s SWITCH    Switch IP
  -u USER      Username
  -p PASSWORD  Password, leave out for none
  -f FILE      File containing switch IP addresses
  --ssh        Use SSH to access switches
  --vpif  Check VPIF state on sec port master

someone@ubuntu:~/work/check_eaps$ ./check_eaps.py -f test --vpif
  
[Eaps checker version 1.02]


[+] Checking switch: 10.116.3.91 -SysName: X460-48t -HW Type: X460-48t
Checking config.. Eaps Check start.. Vlan check..

[+] No Eaps config problems detected
[+] Eaps status for all 1 domains OK

[+] Checking vpif state for eaps domain e1 blocked port 3
    This can take some time on large vlan/eaps configs.
 -  All vpif states are correct on port 3 for domain e1

[-] Closing connection

######################


[+] Checking switch: 10.116.3.194 -SysName: X460-48t -HW Type: X460-48t
Checking config.. Eaps Check start.. Vlan check..

[-] Eaps config problems found : 
 - Protected vlan v2 ports not added to EAPS e1 port 1
 - Protected vlan v2 ports not added to EAPS e1 port 3
 - Vlan Default added to ringports of eaps domain e1 but not protected by it.

[+] Eaps status for all 1 domains OK

[+] vpif check, no Master domains found, no vpif check needed.

[-] Closing connection

######################

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
