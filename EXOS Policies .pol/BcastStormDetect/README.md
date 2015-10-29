# Broadcast Storm Detect

## Description
This policy provides a CLEAR-Flow monitoring example that 
inspects received broadcast message packets to detect potential
broadcast storm attacks.  Both TCP and UDP broadcast packets are
counted and should the sum of these broadcast messages exceed 
100,000 in one second.  In this case, an SNMP trap is issued 
along with a syslog message to provide notification of a 
potential broadcast storm attack.

### Files

* [BcastStormDetect.pol](BcastStormDetect.pol)	-  The Example policy file
* [README.md](README.md)	-  This Readme

### Requirements
* Firmware: ExtremeXOS(TM) 11.6.x and Newer for BcastStormDetect.pol standard
* Platform(s): Summit X450a, X480, X650; BlackDiamond 8800 c-series, 8900-series, 8900-XL series, BlackDiamond 10K, 12K 


### Example
In the below example the rule becomes true and CLEAR-Flow executes its
actions automatically.
```
<X650 Running CLEAR-FLow policy> (Rule becomes true)
<X650 Running CLEAR-FLow policy> (CLEAR-Flow takes configured actions
                                  (e.g. QoS BCast Traffic))
```


### Notes
* This requires a CLEAR-Flow enabled switch

### Versions
1.0 - (1 April 2010) First Version of the script


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
