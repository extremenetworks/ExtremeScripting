# VLAN Port Info

## Description
This script displays the VLAN assignment and tagging configuration for all or sellected ports on the switch.

### Files
* [vlanportinfo.py](vlanportinfo.py)
* [vlanportinfo_line_break.py](vlanportinfo_line_break.py)  Added line break after 25 lines.
* [README.md](README.md)

### Requirements
ExtremeXOS 15.6+

### Usage
run script vlanportinfo.py
run script vlanportinfo.py <port(s)>


### Example 1
# run script vlanportinfo.py 1-3,6
Port     untagged:tagged
1        untagged:1
2        untagged:1
3        untagged:1
6        none:

### Example 2
```
# run script vlanportinfo.py
Port     untagged:tagged
1        none:
2        tagged:30
3        tagged:10
4        tagged:1500
5        none:
6        none:
7        none:
8        none:
9        none:
10       none:
11       none:
12       none:
13       none:
14       none:
15       none:
16       none:
17       none:
18       tagged:2001
19       none:
20       none:
21       none:
22       none:
23       untagged:10
         tagged:30
24       tagged:2001
25       none:
26       none:
27       none:
28       none:
29       none:
30       none:
31       none:
32       none:
33       tagged:2001
34       none:
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
