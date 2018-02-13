# List Compressor

## Description
This script takes a string of numerical values and compresses them into a string of condensed numerical ranges

This script is actually a test/example container for the list_compress() function. EXOS outputs occasionally display
numerical ranges (i.e port numbers and VLAN IDs) inefficiently, consuming valuable screen space.
This list_compress() function will compress the list down to the most efficient string possible.  This allows a user (or script) 
to use the data more efficiently, particularly when inputing the data into a CLI command or parsing it for information within a script.

Notes:
- Slot/Chassis numbers are also supported.
- The underlying list_compress() function will accept both a string of numbers as well as a pythonic list of numbers

### Files
* [list_compress.py](list_compress.py)
* [README.md](README.md)

### Requirements
N/A

### Example

1. Execute a Command that presents a list of numbers that needs to be compressed
```
Slot-1 Switch.6 # show port 1:1 vid
         Untagged  
Port     /Tagged   VID(s)
-------- --------  ------------------------------------------------------------
1:1      Untagged  None
         Tagged    3019, 3020, 3021, 3022, 3023, 3025, 3026, 3027, 3029, 3030, 
                   3032, 3033, 3034, 3035, 3036, 3041, 3042, 3043, 3044, 3045, 
                   3046, 3047, 3048, 3050, 3051, 3052
```
                   
2. Input the list into the script
```
Slot-1 Switch.7 # run script list_compress.py "3019, 3020, 3021, 3022, 3023, 3025, 3026, 3027, 3029, 3030, 3032, 3033, 3034, 3035, 3036, 3041, 3042, 3043, 3044, 3045, 3046, 3047, 3048, 3050, 3051, 3052"
```
3. Output compressed list for easier use in the CLI
```
3019-3023, 3025-3027, 3029-3030, 3032-3036, 3041-3048, 3050-3052
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
