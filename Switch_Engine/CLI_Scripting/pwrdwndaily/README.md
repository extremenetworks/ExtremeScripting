# PoE Power Down Daily

##Description
This profile turns power off at a specific time of day to a list of
Power-over-Ethernet enabled ports.

This Power Conservation Profile is designed to ease the set-up of power
conservation practices in your Extreme Networks edge switches. By using the
pre-defined power conservation profile and modifying it for use in your
environment, you'll have the opportunity to save energy and reduce energy
related network operating costs.

Networks that utilize Power over Ethernet enabled Voice over IP solutions,
wireless access points or other Power over Ethernet enabled devices are the
key beneficiaries of the module.

This profile turns off power at a specific time of day to a list of
Power-over-Ethernet enabled ports.  The profile is intended for deployment
with Extreme Networks EPICenter management platform Universal Port applet.


### Files
* [README.md](README.md) - This readme file
* [PowerDownDailyProfile.xsf](PowerDownDailyProfile.xsf)       - The script


### Requirements
* Firmware: ExtremeXOS(TM) 12.0 or greater with an Edge License
* Platform(s): EPICenter 6.0 SP1 or greater
* Extreme Networks ExtremeXOS-based advanced edge switches


### Example
In order to properly deploy this profile, the following actions must be
performed:

1.  Open the Power Down Daily profile
    a. Edit variables in profile to meet requirements of your
       network (ie., port numbers)

2.  Assign Power Down Daily profile to a Universal Port timer in EPICenter

3.  Configure Universal Port timer in EPICenter


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