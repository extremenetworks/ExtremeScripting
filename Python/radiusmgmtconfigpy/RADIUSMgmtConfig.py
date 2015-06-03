#!/usr/bin/env python
'''
Wizard to aid in configuring RADIUS
'''
import re
###############################################################################
# RADIUS Variable definitions
###############################################################################

ynradiusmgmt = raw_input("Configure And Enable RADIUS For Switch Management? (yes or no): ")
ynradsecretmgmt = raw_input("Is The RADIUS Server Shared Secret Encrypted (yes or no): ")
radservermgmt = raw_input("RADIUS Server IP Address: ")
vrname = raw_input("RADIUS Client IP Address Virtual Router Name (vr-default): ")
print("Note:  RADIUS Client IP Address must be configured in virtual router\n\"VR-Default\" for this script to execute properly")
radclientmgmt = raw_input("RADIUS Client IP Address: ")
radsecretmgmt = raw_input("RADIUS Server Shared Secret Password: ")

###############################################################################
# RADIUS MGMT ACCESS
###############################################################################

if (re.match(ynradiusmgmt,"yes")):
	exsh.clicmd("create log entry \"Configuring RADIUS Switch Management\"", True)
	print("Configuring RADIUS Switch Management")
	exsh.clicmd("configure radius mgmt-access primary server %s client-ip %s vr %s" % (radservermgmt,radclientmgmt,vrname), True)
	if (re.match(ynradsecretmgmt,"yes")):
		exsh.clicmd("configure radius mgmt-access primary shared-secret encrypted %s" % radsecretmgmt, True)
		exsh.clicmd("create log entry \"RADIUS management secret encryted\"", True)
		print("RADIUS management secret encryted")
	else:
		exsh.clicmd("configure radius mgmt-access primary shared-secret %s" % radsecretmgmt, True)
		exsh.clicmd("create log entry \"RADIUS managment secret not encrypted\"", True)
		print("RADIUS management secret not encryted")
	exsh.clicmd("enable radius mgmt-access", True)
	exsh.clicmd("create log entry \"RADIUS Switch Management Configuration Complete and Enabled\"", True)
	print("RADIUS Switch Management Configuration Complete and Enabled")
else:
	exsh.clicmd("create log entry \"RADIUS Switch Managment Not Configured\"", True)
	print("RADIUS Switch Managment Not Configured")
