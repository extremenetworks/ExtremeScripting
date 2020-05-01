# SLX event-handler template

This is a template script for writing SLX event-handler scripts.

## Description

This script will register itself as an event-handler for the SLX. On the specified event, the SLX will pass the log message information to the script, and the script will do the requested actions.  

Please review the scripts actions prior to usage.

## Files

* [event_handler_template.py](event_handler_template.py) - This is a template file for the event handler script.

* [po_member.py](po_member.py) - This is an example based off the template that enables or disables the port-channel members based on the port-channel state change log message.

## Requirements

Firmware: Extreme SLX OS 17r.1.00 or later, or Extreme SLX OS 17s.1.00 or later.
VDX may work, but has not been tested.

## Features

This script must be run on a Extreme SLX platform.

## How to use

1. Modify the template script for the desired action  it should do, and log message and information it should trigger on.
2. Copy the script to the SLX device.
3. Execute 'python <filename_of_script.py> --register'
4. Verify that the script has registered as an event-handler by using 'show run event-handler'.
5. Wait for the script to be activated.

### Usage Example:

```
slx8-1# copy scp://user:extreme@10.25.101.102//home/user//EventHandler/event_handler_template.py flash://event_handler.py

slx8-1# python event_handler.py -r                                                                                       

slx8-1# show run event-handler
 event-handler event_handler
 description test
 trigger 1 raslog LOG-1001
trigger 2 raslog LOG-1002
action python-script event_handler.py
!
event-handler activate event_handler
```



## License

Copyright� 2018, Extreme Networks All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).


Be Extreme
