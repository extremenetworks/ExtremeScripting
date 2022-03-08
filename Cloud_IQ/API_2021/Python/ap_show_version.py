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
cli_cmd   = 'show version'
log       = logging.getLogger()
session   = XIQ.API(xiqUser, xiqPasswd)

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
        if device['device_function'] == 'AP' and device['connected']:
            devices[ str(device['ip_address']) ] = device
else:
    log.warning("unable to pull device list: %s" % session.message)

for ip in devices:
    if session.call('POST', 'devices/'+ str(devices[ip]['id']) +'/:cli', [ cli_cmd ]):
        for dataSet in session.data['device_cli_outputs'][ str(devices[ip]['id']) ]:
            if dataSet['response_code'] == 'SUCCEED':
                print("%s  %s  '%s':\n%s" % (ip, devices[ip]['hostname'], dataSet['cli'], dataSet['output']) )
            else:
                print("%s  %s  '%s': %s" % (ip, devices[ip]['hostname'], dataSet['cli'], dataSet['response_code']) )
    else:
        log.warning("unable to call device CLI: %s" % (ip, session.message) )
print()
