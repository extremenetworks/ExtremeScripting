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
def login(config):
    session = ExtremeOpenAPI.OpenAPI(config['host'],config['username'],config['password'])
    if session.error:
        log.error("login failed: '%s'" % session.message)
        exit(1)
    return session

########################################################################
def getAllVlans():
    vlans = session.call('GET','/v1/state/vlan')
    if session.error:
        log.error("call failed: '%s'" % session.message)
    else:
        msg = ''
        for vlan in vlans:
            #log.debug(json.dumps(vlan,indent=2,sort_keys=True))
            msg += "\t%5s %s\n" % (vlan['vlanId'],vlan['name'])
        log.info("All %s VLANs:\n%s" % (len(vlans), msg))
    return vlans

########################################################################
def getVlanConfig(vlanId):
    vlan = session.call('GET','/v0/configuration/vlan/%s' % vlanId)
    if session.error:
        log.error("VLAN config failed: '%s'" % session.message)
        exit(3)
    else:
        log.info("got VLAN config %s [%s] in %0.3f seconds" % (vlan['name'],vlanId,session.elapsed))
        #log.debug(json.dumps(vlan,indent=2,sort_keys=True))

########################################################################

log = setupLogger()

config = readConfig()

session = login(config['connection'])

vlans = getAllVlans()
callCount += 1

for vlan in vlans:
    getVlanConfig(vlan['vlanId'])
    callCount += 1
