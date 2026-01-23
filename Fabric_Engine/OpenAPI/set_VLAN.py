#!/usr/bin/env python3

import ExtremeOpenAPI
import sys, logging, atexit, time, yaml

config    = None
session   = None
log       = None
callCount = 0
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
def login():
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
def setVlanConfig(vlanId):
    session.call(
        type = 'POST',
        subUri = '/v0/configuration/vrf/GlobalRouter/vlan',
        body = {
            "id": vlanId,
            "name": "Test-%s" % vlanId,
            "stpName": "0",
            "vlanType": "PORT_MSTP_RSTP"
        }
    )
    if session.error:
        log.error("set VLAN failed: '%s'" % session.message)
        exit(3)
    else:
        log.info("set VLAN Test-%s [%s] in %0.3f seconds" % (vlanId,vlanId,session.elapsed))

########################################################################

log = setupLogger()

config = readConfig()

session = login()

vlanIds = getAllVlanIds()
callCount += 1

for id in range(config['vlanStart'], config['vlanStart'] + config['vlanRange']):
    if not id in vlanIds:
        setVlanConfig(id)
        callCount += 1
    else:
        log.info("VLAN %s already exists, skipping" % id)
        continue
