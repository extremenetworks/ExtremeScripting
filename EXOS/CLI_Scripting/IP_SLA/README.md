# IP SLA UPM example

## Description
This UPM script will run every 30 Seconds and mimic the function  of IP SLA.  The script checks the PreferredRoute and SecondaryRoute for connectivity and changed the default route based on connectivity.  If both routes are reachable it will program the default route of the PreferredRoute.

This script is meant to be an example of a possible scripting solution.  It has not been verified by Engineering. Performance can not be guaranteed. Customer use is at their own risk.

### Files
* [ip_sla.xsf](ip_sla.xsf) 	-  The Core Script
* [README.md](README.md)	-  This Readme

### Requirements
* Firmware: ExtremeXOS(TM) 12.3.x and Newer for ip_sla.xsf standard
* Platform(s): Any ExtremeXOS switch.
* TFTP Server

###Example
```
* X450G2-48t-10G4.5 # load script ip_sla.xsf
* X450G2-48t-10G4.7 # show upm timers 
Current Time: 2016-09-19 15:04:55
--------------------------------------------------------------------------------
UPM               Profile       Flags              Next Execution
Timer             Name                             time              
--------------------------------------------------------------------------------
IP_SLA_Timer     IP_SLA         ep            2016-09-19 15:05:13(Every 30 secs)
--------------------------------------------------------------------------------

Number of UPM Timers: 1
Flags: e - Profile is enabled, d: Profile is disabled
       o -Timer is non-periodic, p - Timer is periodic
* X450G2-48t-10G4.7 # show log
09/19/2016 15:04:43.28 <Noti:UPM.Msg.upmMsgExshLaunch> : Launched profile IP_SLA for the event UPM Timer IP_SLA_Timer
09/19/2016 15:00:43.19 <Noti:UPM.Msg.upmMsgExshLaunch> : Previous message repeated 8 additional times in the last 210 second(s)
09/19/2016 15:00:17.18 <Info:System.userComment> : 1st ping attempt failed for Preferred Route 192.168.22.1 .
09/19/2016 15:00:13.19 <Noti:UPM.Msg.upmMsgExshLaunch> : Launched profile IP_SLA for the event UPM Timer IP_SLA_Timer
09/19/2016 14:46:13.19 <Noti:UPM.Msg.upmMsgExshLaunch> : Previous message repeated 28 additional times in the last 810 second(s)
```


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
