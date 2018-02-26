# portsum.py

## Description
This script provide a summary view of an EXOS switch port coounters.

This is a combined view of the EXOS commands:
* show ports statistics
* show ports rxerrors
* show ports txerrors
* show ports congestion
* show ports qosmonitor congestion

## Files
* [portsum.py](portsum.py?raw=true)
* [README.md](README.md)

## Requirements
ExtremeXOS 16.x and later

## Download
* Copy portsum.py to a tftp server. tftp the file to your switch using the EXOS tftp command
* Transfer the file to your PC, then use the Chalet switch web interface File Manager application to transfer the file to your switch.

### Usage
#### Help
```
run script portsum.py -h
```
```
usage: portsum [-h] [-v] [ports]

positional arguments:
  ports          Ports to display. Default is all ports

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  Display version
```

#### Example 1: All ports
```
run script portsum.py
```
```
Mon Feb 26 01:09:49 UTC 2018
In       Out      In       Out      In       Out      In       Out      In       Out      In       Out      In
Port        Octets   Octets   Ucasts   Ucasts   Mcasts   Mcasts   Bcasts   Bcasts Discards Discards   Errors   Errors Unknowns
--------  -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- --------
1:1              0        0        0        0        0        0        0        0        0        0        0        0        0
1:2              0        0        0        0        0        0        0        0        0        0        0        0        0
1:3              0        0        0        0        0        0        0        0        0        0        0        0        0
.
.
.
```
#### Example 2: Selected ports
```
run script portsum.py 1:1,1:3,1:20-25
```
```
Mon Feb 26 02:21:03 UTC 2018
            In       Out      In       Out      In       Out      In       Out      In       Out      In       Out      In
Port        Octets   Octets   Ucasts   Ucasts   Mcasts   Mcasts   Bcasts   Bcasts Discards Discards   Errors   Errors Unknowns
--------  -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- --------
1:1              0        0        0        0        0        0        0        0        0        0        0        0        0
1:3              0        0        0        0        0        0        0        0        0        0        0        0        0
1:20             0        0        0        0        0        0        0        0        0        0        0        0        0
1:21             0        0        0        0        0        0        0        0        0        0        0        0        0
1:22             0        0        0        0        0        0        0        0        0        0        0        0        0
1:23             0        0        0        0        0        0        0        0        0        0        0        0        0
1:24             0        0        0        0        0        0        0        0        0        0        0        0        0
1:25             0        0        0        0        0        0        0        0        0        0        0        0        0
```


## License
Copyright© 2018, Extreme Networks
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
