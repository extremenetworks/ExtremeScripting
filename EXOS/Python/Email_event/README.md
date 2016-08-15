# Email event script
This tool will send an email when a log event is logged. It runs on the switch.

### Description
This script works together with UPM. UPM will start the script once it reacts on an event log entry. That log entry can be any event.
Keep an eye on the amount of entries you want to email, in the end it is the CPU of the switch that will send mails and you dont want to overload the CPU with sending mails about log events you are not interested in.

**Please review the configuration before loading the configuration on a switch**

### Files
* [The Core Python Script - email.py](email.py)
* [README.md](README.md)


### Requirements
Firmware: ExtremeXOS(TM)
This script was tested on 16.1.

### Features
* This Script runs on EXOS.
 

### How to use
* Copy the script to the switch
* Adjust in the script the following lines:

    myVirtualRouter = 2  <- Number of your virtual-router to reach SMTP server

    FromDomain = "@email.com"

    to = 'Your@email.com'

    smtp = 'Your SMTP server IP/DNS'

* Setup UPM together with EMS to start the script for an event.
* Create a log filter that matches your event log events you want to email.
* In this example it acts on link Up/Down events

```
create log filter PortUpDown
configure log filter PortUpDown add events vlan.msgs.portLinkStateUp 
configure log filter PortUpDown add events vlan.msgs.portLinkStateDown 
```

* Create the UPM profile that launches the python script with correct arguments

```
create upm profile EmailProfile
enable cli scripting
run script email $EVENT.LOG_PARAM_0 $EVENT.LOG_PARAM_1
```

* Create the log target for UPM and bind it to the logfilter

```
create log target upm EmailProfile
enable log target upm EmailProfile
configure log target upm EmailProfile filter PortUpDown severity Info
```

* Enable DNS by adding a name server.

```
configure dns-client add name-server <DNS IP> vr <Correct VR to reach DNS server>
```

* After that the switch will mail you when a link status change happens.


## EXOS run example:
```
11/20/2015 10:15:30.15 <Noti:UPM.Msg.upmMsgExshLaunch> : Launched profile EmailProfile for the event log-message
11/20/2015 10:15:30.13 <Info:vlan.msgs.portLinkStateUp> : Port 9 link UP at speed 1 Gbps and full-duplex
11/20/2015 10:14:42.13 <Noti:UPM.Msg.upmMsgExshLaunch> : Launched profile EmailProfile for the event log-message
11/20/2015 10:14:42.12 <Info:vlan.msgs.portLinkStateDown> : Port 9 link down
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
