# Fabric Attach Zero Touch Client (FA-ZTC)
## Description
This script implements the ERS and VSP FA ZTC functionality on XOS.

### History
v1.0    02-May-2020
* initial posting

### Files
* [fa-ztc.py](fa-ztc.py)
* [README.md](README.md)

### Requirements
ExtremeXOS 22.4 and later

### Installation
Transfer the script to the XOS file system.

run script fa-ztc.py

Follow the dialogues for installation.

```
Slot-1 X460G2-STK.15 #% run script fa-ztc.py

Fabric-Attach Zero-Touch-Client (fa-ztc version 1.0)
====================================================
This Python script will do the following:
 - Anchor itself into the XOS switch Universal Port Manager (UPM)
   as an event handler responding to 'device-detect' and
   'device-undetect' events
 - Create an alias command 'fa-ztc' on the XOS switch to allow
   user to configure ZTC via command line

Ok to proceed (y/n) ?y

FA Zero-Touch_client script is now active
Please logout and log back in for alias 'fa-ztc' to be active
Then can use command 'fa-ztc' to configure ZTC bindings
To uninstall, use command 'run script fa-ztc.py uninstall'
Slot-1 X460G2-STK.16 #%
```


### Usage
fa-ztc add <client-type> <vlan-id> <i-sid>
fa-ztc remove <client-type>
fa-ztc ports <port-list|none|all>
fa-ztc show

```
Slot-1 X460G2-STK.17 #% fa-ztc
Fabric-Attach Zero-Touch-Client (fa-ztc version 1.0)
====================================================
Usage:
 fa-ztc ports <port-list|none|all>              : Set ports where to detect ztc clients
 fa-ztc add <client-type> <vlan-id> <i-sid>     : Add vlan/i-sid binding for client type
 fa-ztc remove <client-type>                    : Remove binding for client type
 fa-ztc show                                    : Show ztc configuration

 <client-type>        : wap-type1,wap-type2,switch,router,phone,camera,video
                        security-device,virtual-switch,srvr-endpt,ona-sdn,ona-spb-over-ip
Slot-1 X460G2-STK.18 #%
```


### Configuring ports
```
Slot-1 X460G2-STK.20 #% fa-ztc ports all
Slot-1 X460G2-STK.21 #% fa-ztc show

Fabric-Attach Zero-Touch-Client (ZTC) configuration
===================================================
FA ports (UPM): 1:1-2:54

Type  Client Name        VLAN       I-SID
-----------------------------------------

Slot-1 X460G2-STK.22 #%
```


### Configuring FA Clients
```
Slot-1 X460G2-STK.24 #% fa-ztc add virtual-switch 666 20666
Slot-1 X460G2-STK.25 #% fa-ztc show
Fabric-Attach Zero-Touch-Client (ZTC) configuration
===================================================
FA ports (UPM): 1:1-2:54

Type  Client Name        VLAN       I-SID
-----------------------------------------
 14   virtual-switch      666       20666

* Slot-1 X460G2-STK.26 #%
```


### Events recorded in log file
```
05/02/2020 17:34:16.15 <Noti:UPM.Msg.LLDPDevDetected> Slot-1: LLDP Device detected. Mac is 00:50:56:86:19:28, IP is 0.0.0.0, on port 2:9, device type is 4, max power is 0
05/02/2020 17:34:16.15 <Noti:UPM.Msg.upmMsgExshLaunch> Slot-1: Launched profile fa-ztc-detect for the event device-detect
05/02/2020 17:34:19.00 <Info:System.userComment> Slot-1: fa-ztc: detected FA client virtual-switch on port 2:9
05/02/2020 17:34:19.08 <Info:System.userComment> Slot-1: fa-ztc: applied vlan 666 i-sid 20666 on port 2:9

[...]

05/02/2020 17:38:31.17 <Noti:UPM.Msg.LLDPDevRemoved> Slot-1: LLDP Device Removed. Mac is 00:50:56:86:19:28, IP is 0.0.0.0, on port 2:9, device Type is 0
05/02/2020 17:38:31.17 <Noti:UPM.Msg.upmMsgExshLaunch> Slot-1: Launched profile fa-ztc-undetect for the event device-undetect
05/02/2020 17:38:34.03 <Info:System.userComment> Slot-1: fa-ztc: removed vlan 'ZTC_VLAN_0666'(666) i-sid ZTC_VLAN_0666 from port 2:9
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

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).

>Be Extreme
