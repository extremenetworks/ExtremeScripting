# Non-Stacking Configuration Converter
This tool converts a non stacking "show configuration" output to a stacking configuration for slot 1.

### Description
This script will convert non stacking configurations to stacking configurations for slot 1.  Every situation possible has not been tested, but it worked on the configurations tested in the example.

**Please review the configuration before loading the configuration on a switch**

### Files
* [The Core Python Script - non_stacking_config_convert.py](non_stacking_config_convert.py)
* [README.md](README.md)
* [Example input configuration] (example.txt)
* [Example output stacking configuration] (stack_example.txt)

### Requirements
Firmware: ExtremeXOS(TM)
This script was tested on 16.1 and older.

### Features
* This Script can be run on EXOS or on a PC with python 2.7 installed. 
 

### How to use
* The script was made on python 2.7.  Make sure it's installed.
* Place the switch show configuration output into a file.
* place the configuration file in the same directory as the python script.
* The script will ask you for the configuration file name. (enter it)
* the script will create a new file with "stack_" in front of the original file name that has the new stacking configuration.
* Check over the new configuration file to make sure it's right.

## EXOS run example:
```
Switch.2 # save configuration as-script nonstack
Do you want to save configuration to script nonstack.xsf? (y/N) Yes
Saving configuration to script nonstack.xsf on master .... done!

Switch.3 # run script non_stacking_config_convert.py

Note: please only use the show configuration output for this script.
      Make sure the starting non stack configuration file is in the same folder as the python script

what is the non stacking configuration file name? nonstack.xsf

The new stacking configuration will be saved as /usr/local/cfg/stack_nonstack.xsf?

Switch.4# ls
-rw-r--r--    1 admin    admin        3716 Sep 21 11:12 non_stacking_config_convert.py
-rw-r--r--    1 admin    admin         869 Nov 10  2014 default.xsf
-rw-rw-rw-    1 root     root         5736 Sep 21 11:13 nonstack.xsf
-rw-rw-rw-    1 root     root       304838 Sep 20 19:13 primary.cfg
-rw-r--r--    1 admin    admin        5838 Sep 21 11:17 stack_nonstack.xsf
drwxr-xr-x    2 root     root            0 Sep  5 07:03 vmt
```

## Windows run example
```
C:\Users\xxxxx\xxxxx\stacking_change>python non_stacking_config_convert.py

Note: please only use the show configuration output for this script.
      Make sure the starting non stack configuration file is in the same folder as the python script

what is the non stacking configuration file name? config.txt

The new stacking configuration will be saved as stack_config.txt?

C:\Users\xxxxx\xxxxx\stacking_change>dir

 Directory of C:\Users\xxxxx\xxxxx\stacking_change

09/21/2015  11:22 AM    <DIR>          .
09/21/2015  11:22 AM    <DIR>          ..
09/21/2015  10:54 AM            27,595 config.txt
09/21/2015  11:12 AM             3,812 non_stacking_config_convert.py
09/21/2015  11:22 AM            28,549 stack_config.txt
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
