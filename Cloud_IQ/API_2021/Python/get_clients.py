#!/usr/bin/env python

##############################################################
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            07. Mar. 2022
##############################################################

import XIQ
import logging
logging.basicConfig( level=logging.INFO, format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')

##############################################################
xiqUser   = 'xxxxxxxx'
xiqPasswd = 'xxxxxxxx'
log       = logging.getLogger()
session   = XIQ.API(xiqUser, xiqPasswd)

##############################################################

if session.error:
    log.error("login failed: %s" % session.message)
    exit(1)
else:
    log.debug("login passed")

##############################################################
clients = {}
if session.call('GET', 'clients/active'):
  for device in session.data['data']:
    print("  %s %s %s %-15s %s (%s)" % (
            device['online_time'],
            device['ssid'],
            device['mac_address'],
            device['ip_address'],
            device['hostname'],
            device['os_type'],
        )
    )
else:
    log.warning("unable to pull client list: %s" % session.message)

print()
