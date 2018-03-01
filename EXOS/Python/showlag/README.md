# showlag.py

## Description
This script provide a summary view of LAG ports on EXOS. It scans the individual LAG member ports and computes the composite value.

## Files
* [showlag.py](showlag.py?raw=true)
* [showlag_1.0.0.3.lst](showlag_1.0.0.3.lst?raw=true)
* [README.md](README.md)

## Requirements
ExtremeXOS 21.1 and later

## Download
If your switch has internet access, you can download showlag directoy to your switch with the download url command. Copy the link to the .lst file and paste it to switch command line following `download url`.

`download url` [showlag_1.0.0.3.lst](showlag_1.0.0.3.lst)

### Usage
```
Switch # run script showlag.py -h
usage: showlag [-h] [-d] [cmd [cmd ...]]

positional arguments:
  cmd          statistics, rxerrors, txerrors, utilization, all
               Use the same format as the "show port" EXOS commands

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Show debug information
```
The 'all' command displays the output for:
* statistics
* rxerrors
* txerrors
* utilization


Assume the switch has the following LAG configuraiton:
```
switch # show sharing
Load Sharing Monitor
Config    Current Agg     Min    Ld Share  Dist  Ld Share  Agg Link  Link Up
Master    Master  Control Active Algorithm Flags Group     Mbr State Transitions
================================================================================
     1            Static     1    L2        A     1         -     R       0
                                  L2              2         -     R       0
                                  L2              3         -     R       0
                                  L2              4         -     R       0
                                  L2              5         -     R       0
                                  L2              6         -     R       0
                                  L2              7         -     R       0
                                  L2              8         -     R       0
    10            Static     1    L2        A     10        -     R       0
                                  L2              11        -     R       0
                                  L2              12        -     R       0
                                  L2              13        -     R       0
                                  L2              14        -     R       0
                                  L2              15        -     R       0
                                  L2              16        -     R       0
                                  L2              17        -     R       0
                                  L2              18        -     R       0
    20            Static     1    L2        A     20        -     R       0
                                  L2              21        -     R       0
                                  L2              22        -     R       0
                                  L2              23        -     R       0
                                  L2              24        -     R       0
                                  L2              25        -     R       0
                                  L2              26        -     R       0
                                  L2              27        -     R       0
                                  L2              28        -     R       0
================================================================================
Link State: A-Active, D-Disabled, R-Ready, NP-Port not present, L-Loopback
Minimum Active: (<) Group is down. # active links less than configured minimum
Load Sharing Algorithm: (L2) Layer 2 address based, (L3) Layer 3 address based
                        (L3_L4) Layer 3 address and Layer 4 port based
                        (custom) User-selected address-based configuration
Custom Algorithm Configuration: ipv4 L3-and-L4, xor
Distribution Flags:
    A - All: Distribute to all members,
    L - Local Slot: Distribute to members local to ingress slot,
    P - Port Lists: Distribute to per-slot configurable subset of members,
    R - Resilient Hashing enabled.
Number of load sharing trunks: 3
```
### Example 1
```
switch # run script showlag.py statistics
```
```
    LAG  Tx Pkt Tx Byte  Rx Pkt Rx Byte  Rx Pkt  Rx Pkt  Tx Pkt  Tx Pkt
          Count   Count   Count   Count   Bcast   Mcast   Bcast   Mcast
------- ------- ------- ------- ------- ------- ------- ------- -------
   lag1       0       0       0       0       0       0       0       0
  lag10       0       0       0       0       0       0       0       0
  lag20       0       0       0       0       0       0       0       0
------- ------- ------- ------- ------- ------- ------- ------- -------
```
### Example 2
```
switch # run script showlag.py all
```
```
      LAG        Tx        Tx        Tx        Tx        Tx        Tx
               Coll Late coll  Deferred    Errors      Lost    Parity
--------- --------- --------- --------- --------- --------- ---------
     lag1         0         0         0         0         0         0
    lag10         0         0         0         0         0         0
    lag20         0         0         0         0         0         0
--------- --------- --------- --------- --------- --------- ---------


        LAG        Link          Rx     Peak Rx          Tx     Peak Tx
                  Speed % bandwidth % bandwidth % bandwidth % bandwidth
----------- ----------- ----------- ----------- ----------- -----------
       lag1        6000     0.00000     0.00000     0.00000     0.00000
      lag10        3000     0.00000     0.00000     0.00000     0.00000
      lag20        5000     0.00000     0.00000     0.00000     0.00000
----------- ----------- ----------- ----------- ----------- -----------


    LAG  Tx Pkt Tx Byte  Rx Pkt Rx Byte  Rx Pkt  Rx Pkt  Tx Pkt  Tx Pkt
          Count   Count   Count   Count   Bcast   Mcast   Bcast   Mcast
------- ------- ------- ------- ------- ------- ------- ------- -------
   lag1   10803 1458651    5239  762579       0    4253       0    9822
  lag10    3711  490243    2114  291031       0    1859       0    3460
  lag20    6866  900912    4967  660678       0    4560       0    6446
------- ------- ------- ------- ------- ------- ------- ------- -------


   LAG     Rx     Rx     Rx     Rx     Rx     Rx     Rx
          Crc   Over  Under   Frag Jabber  Align   Lost
------ ------ ------ ------ ------ ------ ------ ------
  lag1      0      0      0      0      0      0      0
 lag10      0      0      0      0      0      0      0
 lag20      0      0      0      0      0      0      0
------ ------ ------ ------ ------ ------ ------ ------
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
