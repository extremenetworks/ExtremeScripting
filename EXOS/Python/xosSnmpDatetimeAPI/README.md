# EXOS snmp datetime Converter

## description

EXOS SNMP object extremeLastSaveConfigTime (1.3.6.1.4.1.1916.1.42.1.1.1.2) returns value as display string. Converting it to datetime format of python will be useful. So providing an API that can take display string formatted EXOS SNMP object extremeLastSaveConfigTime and return Python datetime format output.
**This script runs on client machine, NOT on EXOS switch**

## Files

 /snmpAPI
 - convertSnmpDate. py

This is the file that contains actual API. convertSnmpDate2Std(exos_formatted_datetime) returns python datetime object.

/supportFiles
   - getTime. py
   - readSnmp. py

readSnmp. py is using python SNMP library called 'easysnmp' to receive last configuration change time. community string and host IP needs to be changed for the example programs to work on the new environment. 
getTime. py takes uses readSnmp. py to display last configuration change time as it is from switch.

/Example 
 - xConfigCheck. py
 - xdisplayLastCon. py 
 - xNextConfChange. py

These are example python scripts that uses convertSnmpDate2Std API to convert received 'last configuration change time' to python datetime and process it. Example scripts uses readSnmp. py as well. So community string and host address needs to be updated to work it properly. Also setup needs 'easysnmp' python library.

## Requirements

There is no specific requirements to use this API. This Script can be run on a PC with python 2.7 installed.


## Example on Linux Machine

    root@aswanikumar-VirtualBox:/home/aswanikumar/sample# python getTime.py
    Thu Jul  5 04:51:42 2018
    
    root@aswanikumar-VirtualBox:/home/aswanikumar/sample# python xdisplayLastCon.py
    
    Last Config Update Time : 2018-07-05 04:51:42
    
    root@aswanikumar-VirtualBox:/home/aswanikumar/sample# python xConfigCheck.py
    
    Last Config Update Time : 2018-07-05 04:51:42
    Current time            : 2018-07-13 11:08:49.076661
    
    Configuration not Updated for last 8 days, 6:17:07.076661
    
    root@aswanikumar-VirtualBox:/home/aswanikumar/sample# python xNextConfChange.py
    
    Last Config Update Time : 2018-07-05 04:51:42
    
    Next Update after 60 days.
    
    Configuration will be Updated on : 2018-09-03 04:51:42
    
    root@aswanikumar-VirtualBox:/home/aswanikumar/sample#


##  License


Copyright© 2015, Extreme Networks All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    
2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support

The software is provided as is and Extreme Networks has no obligation to provide maintenance, support, updates, enhancements or modifications. Any support provided by Extreme Networks is at its sole discretion.

Issues and/or bug fixes may be reported on  [The Hub](https://community.extremenetworks.com/).
