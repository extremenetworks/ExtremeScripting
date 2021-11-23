#!/usr/bin/env python

##############################################################
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            1. Sep. 2020
##############################################################

import sys
import XMC_NBI

##############################################################
xmcServerIp = '192.168.162.50'
xmcClientID = 'DVDnjOaqMQ'
xmcSecret   = '8c12a0e1-87f8-4b18-a8d1-2e8c74d27c65'

##############################################################

session = XMC_NBI.XMC_NBI(xmcServerIp, xmcClientID, xmcSecret)
if session.error:
    print( "ERROR: '%s'" % session.message )
    sys.exit(1)

data = session.getDevices()
if session.error:
    print( "ERROR: get devices fialed '%s'" % session.message )
    sys.exit(1)
else:
    if data:
        print("INFO: found %s devices" % len(data))
        print( "\t%-16s %s" % ('IP-Address', 'nick-name') )
        for device in data:
            print( "\t%-16s %s" % (device['ip'], device['nickName']) )
    else:
        print('WARN: no device on XMC exists')
    print()