# SLX Portstatus

This is a script that returns an customized data format for the physical and
port-channel interfaces from various commands on the SLX. This information comes
from various show commands on the SLX. The information is processed and returned as
a table to the CLI for the user to process.

## Description

This script returns a customized view point of the physical and port-channel interfaces.
Among the information returned is is the link state, RX and TX stats, RX optical
power, and optical media type.

## Files

* [SLX_Portstatus.py](SLX_Portstatus.py) - This is the script that returns the
cusomized data format.

## Requirements

Firmware: Extreme SLX OS 17r.1.00 or later, or Extreme SLX OS 17s.1.00 or later.
VDX may work, but has not been tested.

## Features

This script must be run on a Extreme SLX platform.

## How to use

1. Copy the script to the SLX device.
2. Execute 'python <filename_of_script.py>'. Script should return a data table
similar to the one shown below.


### Usage Example:

```
SLX9250-1# python SLX_Portstatus.py                                                           

======================================================================================================================================================
Int     Name Link         Packets Errors Discards CRC rx   Throughput (Mbps) RX Power QSFP
                        RX      RX     RX                RX                (dBm)
                            TX      TX     TX                TX               
======================================================================================================================================================
e 0/1:1 -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/1:2 -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/1:3 -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/1:4 -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/2   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/3   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/4   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/5   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/6   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/7   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/8   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/9   -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/10  -- adminDown    0       0      0        0        0.000000          -inf     40GE QSFP+ SR4
                            0       0      0                 0.000000
e 0/11  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/12  -- adminDown    0       0      0        0        0.000000          -inf     40GE QSFP+ SR4 INT
                            0       0      0                 0.000000
e 0/13  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/14  -- adminDown    0       0      0        0        0.000000          -inf     40GE QSFP+ SR4
                            0       0      0                 0.000000
e 0/15  -- adminDown    0       0      0        0        0.000000          -inf     40GE QSFP+ SR4
                            0       0      0                 0.000000
e 0/16  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/17  -- adminDown    0       0      0        0        0.000000          -inf     40GE QSFP+ SR4 INT
                            0       0      0                 0.000000
e 0/18  -- adminDown    0       0      0        0        0.000000          -inf     40GE QSFP+ SR4 INT
                            0       0      0                 0.000000
e 0/19  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/20  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/21  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/22  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/23  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/24  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/25  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/26  -- adminDown    0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
e 0/27  -- connected    35010   0      0        0        0.000000          3.397    40GE QSFP+ SR4
                            35033   0      0                 0.000000
e 0/28  -- connected    144078  0      0        0        0.000367          3.885    40GE QSFP+ SR4
                            144599  0      0                 0.000000
e 0/29  -- connected    88773   0      0        0        0.000398          5.963    40GE QSFP+ SR4
                            34987   0      0                 0.000000
e 0/30  -- connected    90281   0      0        0        0.000000          3.350    40GE QSFP+ SR4
                            146786  0      0                 0.000000
e 0/31  -- notconnected 0       0      0        0        0.000000          -inf     40GE QSFP+ SR4
                            0       0      0                 0.000000
e 0/32  -- notconnected 0       0      0        0        0.000000          -inf     40GE QSFP+ SR4
                            0       0      0                 0.000000
p 1     -- connected    179088  0      0        0        0.000367          None     --
                            179632  0      0                 0.000000
p 2     -- connected    179054  0      0        0        0.000398          None     --
                            181773  0      0                 0.000000
p 3     -- notconnected 0       0      0        0        0.000000          None     --
                            0       0      0                 0.000000
SLX9250-1#
```



## License

Copyright� 2020, Extreme Networks All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).


Be Extreme
