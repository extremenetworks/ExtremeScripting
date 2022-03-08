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
runCLI    = True

##############################################################

if session.error:
    log.error("login failed: %s" % session.message)
    exit(1)
else:
    log.debug("login passed")

##############################################################
devices = {}
if session.call('GET', 'devices'):
    for device in session.data['data']:
        print("  %5s %s  %s  %-15s %s (%s)  %s" % (
                device['connected'],
                device['device_admin_state'],
                device['serial_number'],
                device['ip_address'],
                device['hostname'],
                device['device_function'],
                device['network_policy_name'],
            )
        )
else:
    log.warning("unable to pull device list: %s" % session.message)
print()
