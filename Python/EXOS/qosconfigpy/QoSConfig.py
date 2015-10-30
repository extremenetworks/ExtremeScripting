#!/usr/bin/env python
'''
Wizard to aid in creating QoS profiles
'''
import re
##############################################################################
# Variable definitions
##############################################################################

print "Set QoS Profile (QP1 to QP8)"
qosprofile = raw_input("Please enter QP you wish to create (e.g. QP3): ")
print "Change QoS scheduling method (yes or no)"
ynqosmethod = raw_input("Enter yes or no: ")
print "QoS scheduling method (strict-priority or weighted-round-robin)"
qosmethod = raw_input("Enter strict-priority or weighted-round-robin: ")
print "QoS maximum buffer percentage (1 to 100)"
maxbuf = raw_input("Enter 1 to 100: ")
print "QoS weight value for weighted round-robind scheduling (1 to 16)"
weight = raw_input("Please enter 1 to 16 :")
print "QoS minimum bandwidth percentage (0 to 100)"
minbw = raw_input("Please enter 0 to 100: ")
print "QoS maximum bandwidth percentage (0 to 100)"
maxbw = raw_input("Please Enter 0 to 100: ")
print "QoS port list"
portlist = raw_input("Please enter port list (e.g. 3-8 or 1:1-1:12): ")
print "Enable QoS dot1p (yes or no)"
ynenabledot1p = raw_input("Please enter yes or no: ")
print "Enable QoS dot1p replacement (yes or no)"
ynrepldot1p = raw_input("Please enter yes or no: ")
print "Enable QoS diffserv (yes or no)"
ynenablediffserv = raw_input("Please enter yes or no: ")
print "Enable QoS diffserv replacement (yes or no)"
ynrepldiffserv = raw_input("Please enter yes or no: ")
##############################################################################
# Create QoS Profile
##############################################################################
exsh.clicmd("create qosprofile %s" % qosprofile, True)

##############################################################################
# Configure QoS Schedule (Switch Level)
##############################################################################

if (re.match(ynqosmethod,"yes")):
	exsh.clicmd("configure qosscheduler %s" % qosmethod, True)

##############################################################################
# Configure QoS Profile
##############################################################################
exsh.clicmd("configure qosprofile %s maxbuffer %s weight %s" % (qosprofile,maxbuf,weight), True)
exsh.clicmd("configure qosprofile %s minbw %s maxbw %s ports %s" % (qosprofile,minbw,maxbw,portlist), True)

##############################################################################
# Enable QoS Dot1p
##############################################################################

if (re.match(ynenabledot1p,"yes")):
	exsh.clicmd("enable dot1p examination ports %s" % portlist, True)
	if (re.match(ynrepldot1p,"yes")):
		exsh.clicmd("enable dot1p replacement ports %s" % portlist, True)

##############################################################################
# Enable QoS Diffserv
##############################################################################

if (re.match(ynenablediffserv,"yes")):
	exsh.clicmd("enable diffserv examination ports %s" % portlist, True)
	if (re.match(ynrepldiffserv,"yes")):
		exsh.clicmd("enable diffserv replacement ports %s" % portlist, True)

print "QoS Configuration Complete"
