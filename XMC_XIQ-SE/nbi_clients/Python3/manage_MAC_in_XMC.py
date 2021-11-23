#!/usr/bin/env python

##############################################################
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            April 2020
##############################################################

import sys
import time
import XMC_NBI

##############################################################
xmcServerIp = '192.168.162.50'
xmcClientID = 'DVDnjOaqMQ'
xmcSecret   = '8c12a0e1-87f8-4b18-a8d1-2e8c74d27c65'
session     = None

##############################################################
def login():
    global session
    
    session = XMC_NBI.XMC_NBI(xmcServerIp,xmcClientID,xmcSecret)
    
    if session.error:
        print( "ERROR: '%s'" % session.message )
        sys.exit(1)

##############################################################
def getAllMACs():
    
    mac_list = session.getMacAddresses()
    
    if session.error:
        print( "ERROR: get MAC addresses failed '%s'" % session.message )
        sys.exit(1)
    else:
        print("INFO: found %s MACs" % len(mac_list))
        for mac, group in sorted( mac_list.items() ):
            print( "\t%s => %s" % (mac,group) )

##############################################################
def getMAC(mac):
    
    data = session.getMacAddress(mac)
    
    if session.error:
        print( "ERROR: get MAC address failed '%s'" % session.message )
    else:
        if data == None:
            print( "INFO: MAC %s not exists" % mac )
        else:
            print("INFO: MAC %s exists in group %s with description '%s'" % (mac,data['groups'],data['groupDescription']) )
    
##############################################################
def addMAC(mac):
    
    session.addMacAddress(mac, 'Printers', 'added by test script')
    
    if session.error:
        print( "ERROR: add MAC address failed '%s'" % session.message )
    else:
        print("INFO: add MAC %s" % mac)
    
##############################################################
def delMAC(mac):
    
    session.delMacAddress(mac)
    
    if session.error:
        print( "ERROR: delete MAC address failed '%s'" % session.message )
    else:
        print("INFO: delete MAC %s" % mac)
    
##############################################################

login()

#### first test ####
my_mac = '00:00:11:11:22:22'
addMAC( my_mac )
getMAC( my_mac )
delMAC( my_mac )
getMAC( my_mac )

time.sleep( 3 )

#### second test ####
for count in range(1,9):
    my_mac = '00:00:11:11:22:2' + str( count )
    addMAC( my_mac )

getAllMACs()

for count in range(1,9):
    my_mac = '00:00:11:11:22:2' + str( count )
    delMAC( my_mac )

getAllMACs()
