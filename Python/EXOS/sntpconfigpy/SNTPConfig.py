#!/usr/bin/env python
'''
Wizard to configure SNTP
'''
import re
#############################################################################
# Variable definitions
#############################################################################

#clierrormode = raw_input("If this script encounters errors, do you wish to abort or ignore?": )
ynsntp = raw_input("Set a Time Server? (yes or no): ")
sntpserver = raw_input("SNTP server ipaddress (x.x.x.x): ")
tz = raw_input("Offset from GMT in minutes (Central Standard Time in example): ")
dst = raw_input("Configure Daylight Savings Time? (noautodst or autodst): ")
print ("Please refer to country customs regarding Daylight Savings Time")

#############################################################################
# Configure NTP client
#############################################################################

exsh.clicmd("create log entry \"Starting SNTP Configuration\"", True)
print("Starting SNTP Configuration")

#if (re.match(clierrormode,"ignore")):
#  configure cli mode scripting ignore-error
#  create log entry "CLI mode set for Ignore on Error"
#else:
#  configure cli mode scripting abort-on-error
#  create log entry "CLI mode set for Abort on Error"

if (re.match(ynsntp,"yes")):
	exsh.clicmd("configure sntp-client primary %s" % sntpserver, True)
	exsh.clicmd("configure timezone %s %s" % (tz,dst), True)
	exsh.clicmd("enable sntp-client", True)
	exsh.clicmd("create log entry \"SNTP Configured\"", True)
	print("SNTP Configured")
else:
	exsh.clicmd("create log entry \"SNTP NOT Configured\"", True)
	print("SNTP NOT Configured")
