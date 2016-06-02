# IOS to EXOS policy convertor script
This tool will take the access-list part of a cisco config and convert that to EXOS policy files.

### Description
Simply run this script from a PC with python and run it against the access-list portion of a cisco config.
It will save every accesslist to a seperate policy file.

**Please review the policy files before loading them on a switch**

### Files
* [The Core Python Script - IOStoPolicy.py](IOStoPolicy.py)
* [README.md](README.md)


### Requirements
* Python
* cisco extended ACL as in below example.
```
ip access-list extended test1
 permit tcp host 192.0.2.1  198.51.100.0 0.0.0.255 range 138 139
 deny tcp host 192.0.2.2  198.51.100.0 0.0.0.255 range 138 139
 permit tcp host 192.0.2.1  198.51.100.0 0.0.0.255 eq 23
 permit tcp 198.51.100.0 0.0.0.255 eq 23 host 192.0.2.1
 deny tcp any  198.51.100.0 0.0.0.255 eq 25
 deny ip any any
```

### Features
* This Script runs on any PC with python installed.
 

### How to use
* Copy the script
* run the script 
```
IOStoEXOS$ ./IOStoPolicy.py test1.acl 
ACL is saved to test1.pol

IOStoEXOS$ cat test1.pol 
entry test1_permit1 { if { protocol tcp; source-address 192.0.2.1/32; destination-address 198.51.100.0/24; destination-port 138 139;} then { permit;}}
entry test1_deny2 { if { protocol tcp; source-address 192.0.2.2/32; destination-address 198.51.100.0/24; destination-port 138 139;} then { deny;}}
entry test1_permit3 { if { protocol tcp; source-address 192.0.2.1/32; destination-address 198.51.100.0/24; destination-port 23;} then { permit;}}
entry test1_permit4 { if { protocol tcp; source-address 198.51.100.0/24; source-port 23; destination-address 192.0.2.1/32;} then { permit;}}
entry test1_deny5 { if { protocol tcp; source-address 0.0.0.0/0; destination-address 198.51.100.0/24; destination-port 25;} then { deny;}}
entry test1_deny6 { if { source-address 0.0.0.0/0; destination-address 0.0.0.0/0;} then { deny;}}
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
