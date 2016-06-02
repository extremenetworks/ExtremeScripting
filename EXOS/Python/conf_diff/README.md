# Unsaved Config Diff

### Description
This script will compare the currently running config with the saved config, and show the changes.

**This script will clear the CLI dirty bit. The config is not saved.**

### Files
* [conf_diff.py](conf_diff.py)
* [README.md](README.md)


### Requirements
Firmware: ExtremeXOS(TM)
 

### How to use
* ` run script conf_diff.py`
* Lines that start with '-' are lines that are present in the saved config, and have been deleted from the running config.
* Lines that start with '+' are lines that are not present in the saved config, and have been added to the running config.

## EXOS run example:
```
 * X450G2-48p-10G4.11 # run script conf_diff.py
Comparing configurations, please wait...

If line starts with '+', the command has been added since last save.
If line starts with '-', the command was present in the last save, and has been deleted.

Config changes:
+ disable port 1
Note that this script has cleared the CLI dirty bit. The configuration has not been saved.
```

## License
Copyright© 2016, Extreme Networks
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
