# SLX SNMP Ifindex generation script

This is script and supporting libraries to generate the SNMP ifIndex for a given
interface for Extreme SLX routers and switches.

## Description

This script will return the SNMP ifIndex value for the given interface provided
the following information:
* SLX model (such as 9850 or 9640),
* The interface string (such as 'e 1/1'),
* The speed of the interface (such as 40g, or 10G)
* The linecard model if applicable (such as '36x100G' or '48Y')
* The tunnel type if applicable (such as 'vxlan', or 'gre')


## Files
* [slx_ifindex_gen.py](build/bin/slx_ifindex_gen.py) - Human usable script to
determine the SNMP IfIndex of an SLX device.
* [SLX_Bitmap.py](build/lib/BitMap.py) - Provides a methods for use in mapping keys
to binary strings.
* [IfIndex.py](build/lib/IfIndex.py) - Stores and converts the binary string representing the SNMP IfIndex to various formats.
* [SLX_IntfTypeMap.py](build/lib/IntfTypeMap.py) - Instantiates a BitMap with various interface types.
* [SLX_PortData.py](build/lib/PortData.py) - Provides a data class to store physical
port information, such as the supported modes and speeds.
* [SLX_PortMapping.py](build/lib/PortMapping.py) - Provides a utility class holding
all the PortData objects for a SLX device.
* [SLX_IfIndex_Core.py](build/lib/SLX_IfIndex_Core.py) - Provides core functions
common to all SLX device classes.
* [Slx_IfIndex.py](build/lib/Slx_IfIndex.py) - Parent class for all SLX devices.
* [Slx9030_IfIndex.py](build/lib/Slx9030_IfIndex.py) - Provides the SLX9030 class
* [Slx9140_IfIndex.py](build/lib/Slx9140_IfIndex.py) - Provides the SLX9140 class
* [Slx9150_IfIndex.py](build/lib/Slx9150_IfIndex.py) - Provides the SLX9150 class
* [Slx9240_IfIndex.py](build/lib/Slx9240_IfIndex.py) - Provides the SLX9240 class
* [Slx9250_IfIndex.py](build/lib/Slx9250_IfIndex.py) - Provides the SLX9250 class
* [Slx9540_IfIndex.py](build/lib/Slx9540_IfIndex.py) - Provides the SLX9540 class
* [Slx9640_IfIndex.py](build/lib/Slx9640_IfIndex.py) - Provides the SLX9640 class
* [Slx9740_IfIndex.py](build/lib/Slx9740_IfIndex.py) - Provides the SLX9740 class
* [Slx9850_IfIndex.py](build/lib/Slx9850_IfIndex.py) - Provides the SLX9850 class
* [SLXRSpeedMap.py](build/lib/SLXRSpeedMap.py) - Instantiates a BitMap with various interface speeds.
* [SLXSSpeedMap.py](build/lib/SLXSSpeedMap.py) - Instantiates a BitMap with various interface speeds for the SLX 9140 and 9240.
* [SLX_TunnelTypeMap.py](build/lib/TunnelTypeMap.py) - Instantiates a BitMap with
the various tunnel types.
* [test](test/) - Unit tests for the various classes.



## Requirements

None, this script and libraries are intended for use on a standalone PC.
As such, you should have the following present on the PC:

* Python: python3 installation with setuptools module installed.


## Features
* slx_ifindex_gen.py - Human usable script to determine the SNMP IfIndex of an SLX device.
* Slx_IfIndex - module with the Slx_IfIndex class to allow for python scripts
to determine the SNMP IfIndex for an interface of an SLX.

## How to use

1. Clone or download the zip file for the ExtremeScripting repository, and extract
as needed.
2. Change directory to the ExtremeScripting/SLXOS/ifindex_gen folder.
3. Execute ```sudo python3 setup.py install```
4. Once installed execute slx_ifindex_gen.py -h and verify that the help for the
script is returned as shown below.

### Usage Examples:
#### slx_ifindex_gen.py
Shown below are examples of accessing the script help, and a example for the SLXOS
9250 and retrieving the ifIndex for interface e 0/1:1 when configured as a
4x10g breakout.
```
[user@linux ~]$  slx_ifindex_gen.py -h
usage: slx_ifindex_gen.py [-h] --interface INTERFACE --device DEVICE
                          [--linecard {72x10G,36x100G,48Y,48XT}]
                          [--speed SPEED]
                          [--tunnel_type {vxlan,gre,nvgre,mpls}]
                          [--output {dec,hex,bin,all}]

Script to generate ifIndex offline for SLX family of products.

optional arguments:
  -h, --help            show this help message and exit
  --interface INTERFACE, -i INTERFACE
                        The interface name in the format of <type>
                        <slot>/<port> or <type> <port>. Examples: e 1/1, e
                        2/1:1, tun 1, ve 20, po 1, m 1
  --device DEVICE, -d DEVICE
                        SLX device in the format of the 4 digit product
                        number. Examples: 9850, 9140
  --linecard {72x10G,36x100G,48Y,48XT}, -l {72x10G,36x100G,48Y,48XT}
                        LC type for 9850, or model for 9150/9740 for physical
                        ports
  --speed SPEED, -s SPEED
                        physical interface speed: [1g | 10g | 25g | 40g |
                        100g]
  --tunnel_type {vxlan,gre,nvgre,mpls}, -t {vxlan,gre,nvgre,mpls}
                        Tunnel types
  --output {dec,hex,bin,all}, -o {dec,hex,bin,all}
                        Output Display Mode: [bin | dec | hex | all](default:
                        dec)

[user@linux ~]$  slx_ifindex_gen.py -i 'e 0/1:1' -d 9250 -s '10g'
201335296
```

#### Slx_IfIndex module
Below is example code for use in other python scripts besides the included
slx_ifindex_gen.py
```
import re
import sys
from SLX_BitMap import BitMap
from SLX_IntfTypeMap import IntfTypeMap
from SLX_TunnelTypeMap import TunnelTypeMap
from SLXRSpeedMap import SLXRSpeedMap
from SLXSSpeedMap import SLXSSpeedMap
from SLX_PortData import PortData
from SLX_PortMapping import PortMapping
from IfIndex import IfIndex
from SLX_IfIndex_Core import Slx_IfIndex_Core
from Slx9850_IfIndex import Slx9850_IfIndex
from Slx9640_IfIndex import Slx9640_IfIndex
from Slx9540_IfIndex import Slx9540_IfIndex
from Slx9250_IfIndex import Slx9250_IfIndex
from Slx9240_IfIndex import Slx9240_IfIndex
from Slx9150_IfIndex import Slx9150_IfIndex
from Slx9140_IfIndex import Slx9140_IfIndex
from Slx9030_IfIndex import Slx9030_IfIndex
from Slx_IfIndex import Slx_IfIndex

def main():
  args_dict = {
    'device': 9850,
    'interface': 'e 1/1',
    'linecard': '36x100G'
    'speed': '100g'
  }
  example = Slx_IfIndex(**args_dict)
  print(example.get_if_index('decimal'))
  return

```

### Troubleshooting
The error message returned by the script will help indicate which of the passed
arguments is incorrect.
For example:
```
[user@Centos72-101-61 ~]$  slx_ifindex_gen.py -i 'e 0/1:1' -d 9150 -l 48Y -s 10G
ERROR: Failed to init the device level class to calculate the if_index due to the following:
TypeError: Interface is not able to do breakout
```
This error indicates that interface ethernet 0/1:1 on the SLX 9150-48Y is not able
to be configured as a breakout (0/49 and 0/56 are the only interfaces
supporting breakout on the 9150-48Y).

```
[user@Centos72-101-61 ~]$  slx_ifindex_gen.py -i 'e 0/1:1' -d 9250 -s 10G
ERROR: Failed to init the device level class to calculate the if_index due to the following:
ValueError: Interface does not support the requested speed
```
This error is directly related to using a uppercase 'g' in the speed setting.


# License
Copyright© 2020, Extreme Networks. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1.Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.


2.Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).
