#!/usr/bin/env python3

import ExtremeOpenAPI
import sys, logging, atexit, time, yaml

config    = None
session   = None
log       = None
callCount = 1
startTime = time.time()

########################################################################
def setupLogger():
    log = logging.getLogger('ExtremeOpenAPI') 
    log.setLevel(logging.INFO)         # DEBUG INFO WARNING ERROR CRITICAL
    atexit.register(_closeLogger,startTime)
    screen = logging.StreamHandler(stream=sys.stdout)
    screen.setLevel(logging.DEBUG)
    screen_formatter = logging.Formatter('%(asctime)s %(levelname)-7s [%(filename)s:%(lineno)d] %(message)s')
    screen.setFormatter(screen_formatter)
    log.addHandler(screen)
    return log

########################################################################
def _closeLogger(startTime):
    log.info("run time %0.3f seconds for %d calls" % (time.time() - startTime, callCount))
    logging.shutdown()

########################################################################
def readConfig(file='config.yaml'):
    with open(file, 'r') as f:
        config = yaml.safe_load(f)
    return config

########################################################################
def login(config):
    session = ExtremeOpenAPI.OpenAPI(config['host'],config['username'],config['password'])
    if session.error:
        log.error("login failed: '%s'" % session.message)
        exit(1)
    return session

########################################################################
def getAllVlanIds():
    vlans = session.call('GET','/v1/state/vlan')
    vlanId = list()
    if session.error:
        log.error("call failed: '%s'" % session.message)
    else:
        for vlan in vlans:
            vlanId.append(vlan['vlanId'])
        log.info("All %s VLANs" % len(vlans))
    return vlanId

########################################################################
def prepPort(port):
    '''disable auto-sense & enable flex-uni on port'''
    global callCount
    session.call(
        type = 'PATCH',
        subUri = '/v0/configuration/autosense/port/%s' % port,
        body = {
            "enable": False
        }
    )
    log.info("disabled auto-sense on port %s" % port)
    callCount += 1

    session.call(
        type = 'PUT',
        subUri = '/v0/configuration/ports/%s' % port,
        body = {
            "flexUni": True
        }
    )
    log.info("enabled flex-uni on port %s" % port)
    callCount += 1

########################################################################
def updateVlanConfig(vlanId, port):
    global callCount
    session.call(
        type = 'POST',
        subUri = '/v0/operation/vlan/%s/interfaces/:add' % vlanId,
        body = [
            {
                "interfaceType": "PORT",
                "interfaceName": port,
                "tagType": "TAG"
            }
        ]
    )
    if session.error:
        log.error("update VLAN failed: '%s'" % session.message)
        exit(3)
    else:
        log.info("update VLAN Test-%s [%s] to port %s in %0.3f seconds" % (vlanId,vlanId,port,session.elapsed))
        callCount += 1

########################################################################

log = setupLogger()

config = readConfig()

session = login(config['connection'])

vlanIds = getAllVlanIds()

prepPort(config['vlan']['port'])

for vlanId in range(config['vlan']['start'], config['vlan']['start'] + config['vlan']['range']):
    if vlanId in vlanIds:
        updateVlanConfig(vlanId, config['vlan']['port'])
    else:
        log.info("VLAN %s does not exist, skipping" % vlanId)
        continue
