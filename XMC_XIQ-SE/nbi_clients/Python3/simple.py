#!/usr/bin/env python

##############################################################
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            08 Mar 2022
##############################################################

import XMC_NBI

##############################################################
xmcServerIp = '192.168.162.50'
xmcClientID = 'DVDnjOaqMQ'
xmcSecret   = '8c12a0e1-87f8-4b18-a8d1-2e8c74d27c65'
macAddress  = '00:11:22:33:44:55'
esGroup     = 'Printers'

##############################################################

session = XMC_NBI.XMC_NBI(xmcServerIp, xmcClientID, xmcSecret)

session.addMacAddress(macAddress, esGroup, 'added by test script')

data = session.getESGroup(esGroup)
for item in data:
    print("  %s = %s" % (item, data[item]))
