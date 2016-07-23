#!/usr/bin/env python
'''
Wizard to wipe SNMP configuration
'''

#############################################################################
# SNMP v3 Variable definitions
#############################################################################

#clierrormode = raw_input("If this script encounters errors, do you wish to abort or ignore?: ")
print("!!!WARNING!!! THIS SCRIPT WILL WIPE ALL SNMP CONFIGURATION ON THE SWITCH!!!")
ynsnmpconfig = raw_input ("Wipe SNMPv3 settings? (yes or no): ")
config = exsh.clicmd('show config snmp',capture=True)
if ynsnmpconfig.lower() == 'yes':

#############################################################################
# SNMP V3 Configuration
#############################################################################

#if (re.match(clierrormode,"ignore")):
#  configure cli mode scripting ignore-error
#  create log entry "CLI mode set for Ignore on Error"
#else
#  configure cli mode scripting abort-on-error
#  create log entry "CLI mode set for Abort on Error"
	import re
	print("Deleting SNMP configuration...")
	exsh.clicmd('create log entry \"Deleting SNMP Configuration\"', capture=True)
	print("Deleting trap receivers...")
	exsh.clicmd('configure snmp delete trapreceiver all')
	print("Deleting notification logs...")
	exsh.clicmd('configure snmp delete notification-log default')
	print("Deleting non-default SNMPv3 groups")
	print("Deleting non-default SNMPv3 access profiles...")
	exsh.clicmd('configure snmpv3 delete access all-non-defaults')
	print("Deleting non-default SNMPv3 communities...")
	exsh.clicmd('configure snmpv3 delete community all-non-defaults')
	print("Deleting filters...")
	exsh.clicmd('configure snmpv3 delete filter all')
	print("Deleting filter profiles...")
	exsh.clicmd('configure snmpv3 delete filter-profile all')
	print("Deleting non-default mib views...")
	exsh.clicmd('configure snmpv3 delete mib-view all-non-defaults')
	print("Deleting non-default notify configurations...")
	exsh.clicmd('configure snmpv3 delete notify all-non-defaults')
	print("Deleting notify target addresses...")
	exsh.clicmd('configure snmpv3 delete target-addr all')
	print("Deleting target parameters...")
	exsh.clicmd('configure snmpv3 delete target-params all')
	print("Deleting non-default SNMPv3 users...")
	exsh.clicmd('configure snmpv3 delete user all-non-defaults')
	print("Deleting non-default communities...")
	exsh.clicmd('configure snmp delete community readwrite all')
	print("Deleting SNMP readonly communities...")
	exsh.clicmd('configure snmp delete community readonly all')
	print("Deleting groups...")
	for line in config.splitlines():
		p = re.compile(ur'configure\ssnmpv3\sadd\sgroup\s\"(\S+)"')
		x = re.search(p, line)
		if x != None:
			exsh.clicmd('configure snmpv3 delete group '+x.group(1)+' user all-non-default', capture=True)
	print("Enabling SNMPv3 default group...")
	exsh.clicmd('enable snmpv3 default-group')
	print("Enabling SNMPv3 default user...")
	exsh.clicmd('enable snmpv3 default-user')
	print
	exsh.clicmd('create log entry \"Deletion of SNMP configuration completed.\"', capture=True)
	print("Deletion of SNMP configuration completed successfully.")
else:
	print("SNMP configuration was not erased")
	exsh.clicmd('create log entry \"SNMP configuration was not erased\"', capture=True)
	pass