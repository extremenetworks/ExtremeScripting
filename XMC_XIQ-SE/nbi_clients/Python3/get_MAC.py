#!/usr/bin/env python

##############################################################
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            08 Mar 2022
##############################################################

import XMC_NBI

##############################################################
xmcServerIp = '192.168.162.50'                              # 10.8.255.15
xmcClientID = 'DVDnjOaqMQ'                                  # Pj24I8ywuT
xmcSecret   = '8c12a0e1-87f8-4b18-a8d1-2e8c74d27c65'        # 519d93f9-5d7f-449d-bb30-1d616d8d54ef
session     = None

##############################################################
def login():
    global session
    session = XMC_NBI.XMC_NBI(xmcServerIp,xmcClientID,xmcSecret)
    if session.error:
        print( "ERROR: '%s'" % session.message )
        exit(1)

##############################################################

login()

mac_list = session.getMacAddresses()
if session.error:
    print( "ERROR: get MAC addresses failed '%s'" % session.message )
    exit(1)
else:
    print("INFO: found %s MACs" % len(mac_list))
    for mac, group in sorted( mac_list.items() ):
        print( "\t%s => %s" % (mac,group) )
