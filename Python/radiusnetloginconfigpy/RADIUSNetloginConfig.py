#!/usr/bin/env python
'''
Wizard to configure RADIUS netlogin
'''
#############################################################################
# RADIUS and Netlogin Variable definitions
#############################################################################

#clierrormode = raw_input("If this script encounters errors, do you wish to abort or ignore?(abort or ignore): ")
ynradiusnetlogin = raw_input("Configure and enable RADIUS for Network Login? (yes or no): ")
ynradsecretnetlogin = raw_input("Is The RADIUS Server Shared Secret Encrypted (yes or no): ")
radservernetlogin = raw_input("RADIUS Server IP Address: ")
vrname = raw_input("RADIUS Client IP Address Virtual Router Name (vr-default): ")
radclientnetlogin = raw_input("RADIUS Client IP Address \nNote:  RADIUS Client IP Address must be configured in virtual router\n\"VR-Default\" for this script to execute properly: ")
radsecretnetlogin = raw_input("RADIUS Server Shared Secret Password: ")
netloginorder = raw_input("Network Login Authentication Order? (eg. dot1x mac): ")
netloginports = raw_input("Network Login Port List: ")
guestvlan = raw_input("Network Login GUEST VLAN: ")

#############################################################################
# RADIUS NetLogin
#############################################################################

if (re.match(ynradsecretnetlogin,"yes")):
	exsh.clicmd("configure radius netlogin primary shared-secret encrypted %s" % radsecretnetlogin, True)
	exsh.clicmd("create log entry \"Config RADIUS secret encrypted\"", True)
else:
	exsh.clicmd("configure radius netlogin primary shared-secret %s" % radsecretnetlogin, True)
	exsh.clicmd("create log entry \"Config RADIUS secret NOT encrypted\"", True)

if (re.match(ynradiusnetlogin,"yes")):
	exsh.clicmd("create log entry \"Starting Network Login Configuration\"", True)
	exsh.clicmd("create vlan %s" % guestvlan, True)
	exsh.clicmd("configure netlogin vlan %s" % guestvlan, True)
	exsh.clicmd("configure default delete port %s" % netloginports, True)
	exsh.clicmd("enable netlogin dot1x", True)
	exsh.clicmd("enable netlogin mac", True)
	exsh.clicmd("enable netlogin ports %s %s" % (netloginports,netloginorder), True)
	exsh.clicmd("configure netlogin ports %s mode mac-based-vlans" % netloginports, True)
	exsh.clicmd("configure radius netlogin primary server %s client-ip %s vr %s" % (radservernetlogin,radclientnetlogin,vrname), True)
	exsh.clicmd("enable radius netlogin", True)
	exsh.clicmd("create log entry \"RADIUS Network Login Configuration Complete\"", True)
else:
	exsh.clicmd("create log entry \"No RADIUS Netlogin\"", True)
