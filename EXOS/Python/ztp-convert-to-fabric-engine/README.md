# ZTP Convert to Fabric Engine (VOSS)
## Description
Boot universal hardware out of the box directly into VOSS as Fabric Engine

### History
v1.0 - 09-September-2022
* initial posting
v1.1 - 29-September-2022
* Modified to run with Python3 as well as Python2; EXOS32.2 introduces Python3 and drops Python2 support

### Files
* [ztp.py](ztp.py)
* [README.md](README.md)
* [Detailed Description](Universal-Hardware-USB-conversion-to-FabricEngine.pdf)


### Requirements
USB stick and Universal Hardware switch

### How to use
* Place Python script on USB key, naming it “ztp.py”
* Add desired VOSS images to same USB stick
* Insert USB stick into switch
* Power on the switch (or if switch was already booted into EXOS, execute “unconfigure switch”)




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
