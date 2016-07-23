#!/usr/bin/env python
'''
Wizard to wipe SNMP configuration
'''
##############################################################################
# Imports
##############################################################################
import argparse
import re
import sys
#############################################################################
# SNMP v3 Variable definitions
#############################################################################
config = exsh.clicmd('show config snmp',capture=True)
##############################################################################
# Main function
##############################################################################
def main():
    parser = argparse.ArgumentParser(prog='SNMPtogether.py', description = "This script can configure SNMPv3 and remove SNMPv3 configuration")
    parser.add_argument('-d', '--delete', help='removes SNMPv3 Configuration', action="store_true")
    parser.add_argument('-c', '--configure', help='configures SNMPv3 Configuration', action="store_true")
    args = parser.parse_args()
    d = args.delete
    c = args.configure
###############################################################################
# Delete SNMP configuration function
###############################################################################
    if args.delete:
	    print("Deleting SNMP configuration...")
	    exsh.clicmd('create log entry \"Deleting SNMP Configuration using configSNMP.py\"', capture=True)
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
	    exsh.clicmd('create log entry \"Deletion of SNMP configuration completed by configSNMP.py\"', capture=True)
	    print("Deletion of SNMP configuration completed successfully.")

####################################################################################
# Configure SNMPv3 function
####################################################################################
    if args.configure:
	    exsh.clicmd('create log entry \"Starting configuration of SNMPv3 using configSNMP.py\"', capture=True)
	    snmpuser = raw_input ("Please enter your SNMPv3 User name: ")
	    snmpuserpw = raw_input ("Please enter your SNMPv3 User password (7 to 49 char): ")
	    snmpprivacypw = raw_input ("Please enter your SNMPv3 privacy password (7 to 49 char): ")
	    snmpgroupname = raw_input ("Please enter your SNMPv3 Group name: ")
	    snmpaccessname = raw_input ("Please enter your SNMPv3 Access preferences: ")
	    yndisablev1v2access = raw_input("Would you like to disable SNMP v1v2c access?(yes or no): ")
	    yndisablev3user = raw_input ("Would you like to disable the default SNMPv3 user?(yes or no): ")
	    yndisablev3group = raw_input ("Would you like to disable the default SNMPv3 group? (yes or no): ")
	    exsh.clicmd('create log entry \"Starting SNMP Configuration\"', capture=True)
	    exsh.clicmd('configure snmpv3 add user %s authentication md5 %s privacy des %s' % (snmpuser,snmpuserpw,snmpprivacypw), capture=True)
	    exsh.clicmd('configure snmpv3 add group %s user %s sec-model usm' % (snmpgroupname,snmpuser), capture=True)
	    exsh.clicmd('configure snmpv3 add access %s sec-model usm sec-level priv read-view defaultAdminView write-view defaultAdminView notify-view defaultAdminView' % (snmpgroupname), capture=True)
	    exsh.clicmd('enable snmp access vr vr-default', capture=True)
	    if (re.match(yndisablev1v2access,"yes")):
		    exsh.clicmd('disable snmp access snmp-v1v2c')
	    if (re.match(yndisablev3user,"yes")):
		    exsh.clicmd("disable snmpv3 default-user")
	    if (re.match(yndisablev3group,"yes")):
		    exsh.clicmd("disable snmpv3 default-group")
	    print
	    exsh.clicmd('create log entry \"SNMPv3 has been configured successfully using configSNMP.py\"', capture=True)
	    print("SNMPv3 has been configured successfully")
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass		