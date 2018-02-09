#!/usr/bin/env python
'''
Wizard to configure SNMP
'''

#############################################################################
# SNMP v1/v2 Variable definitions
#############################################################################

#clierrormode = raw_input("If this script encounters errors, do you wish to abort or ignore?: ")

ynsnmpconfig = raw_input("Congifigure SNMP v1/v2 access? (yes or no): ")
ynsnmpdisable = raw_input("Disable SNMP v1/v2 access? (yes or no): ")
ynsnmpcommadd = raw_input("Add SNMP v1/v2 communities? (yes or no): ")
snmprwname = raw_input("Read/Write SNMP Community Name?: ")
snmproname = raw_input("Read-Only SNMP Community Name?: ")
ynsnmpcommrem = raw_input("Remove default SNMP Communities? (yes or no): ")
snmpname = raw_input("SNMP Switch Name?: ")
snmplocation = raw_input("SNMP Location?: ")
snmpcontact = raw_input("SNMP Contact?: ")
snmptrapcount = raw_input("Number of SNMP Trap Receivers (Script supports: 1-3): ")
snmptrap1 = raw_input("SNMP Trap Receiver #1: ")
snmptrap2 = raw_input("SNMP Trap Receiver #2: ")
snmptrap3 = raw_input("SNMP Trap Receiver #3: ")

#############################################################################
# SNMP V1/V2 Configuration
#############################################################################

#if (re.match(clierrormode,"ignore")):
#  configure cli mode scripting ignore-error
#  create log message "CLI mode set for Ignore on Error"
#else
#  configure cli mode scripting abort-on-error
#  create log message "CLI mode set for Abort on Error"


if (re.match(ynsnmpconfig,"yes")):
	exsh.clicmd("create log message \"Starting SNMP Configuration\"", True)
	print("Starting SNMP Configuration")
	exsh.clicmd("configure snmp sysName %s" % snmpname, True)
	exsh.clicmd("configure snmp sysLocation %s" % snmplocation, True)
	exsh.clicmd("configure snmp sysContact %s" % snmpcontact, True)
	if (snmptrapcount >= 1):
		exsh.clicmd("configure snmp add trapreceiver %s community %s" % (snmptrap1,snmproname), True)
	if (snmptrapcount >= 2):
		exsh.clicmd("configure snmp add trapreceiver %s community %s" % (snmptrap2,snmproname), True)
	if (snmptrapcount >= 3):
		exsh.clicmd("configure snmp add trapreceiver %s community %s" % (snmptrap3,snmproname), True)
	if (re.match(ynsnmpcommadd,"yes")):
		exsh.clicmd("configure snmp add community readwrite %s" % snmprwname, True)
		exsh.clicmd("configure snmp add community readonly %s" % snmproname, True)
		exsh.clicmd("create log message \"New SNMP Communities Created\"", True)
		print("New SNMP Communities Created")
	if (re.match(ynsnmpcommrem,"yes")):
		exsh.clicmd("configure snmp delete community readwrite private", True)
		exsh.clicmd("configure snmp delete community readonly public", True)
		exsh.clicmd("create log message \"Default SNMP Communities Removed\"", True)
		print("Default SNMP Communities Removed")
	else:
		exsh.clicmd("create log message \"Default SNMP Communities NOT Removed\"", True)
		print("Default SNMP Communities NOT Removed")
else:
	if (re.match(ynsnmpdisable,"yes")):
		exsh.clicmd("create log message \"Disabling SNMP access\"", True)
		print("Disabling SNMP access")
		exsh.clicmd("disable snmp access snmp-v1v2", True)
	else:
		exsh.clicmd("create log message \"SNMP Not Configured\"", True)
		print("SNMP Not Configured")


