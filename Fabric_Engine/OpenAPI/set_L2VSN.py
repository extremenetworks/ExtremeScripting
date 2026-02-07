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
def getAllL2vsn():
    l2vsns = session.call(
        type = 'GET',
        subUri = '/v0/configuration/spbm/l2/isid',
)
    l2vsnList = list()
    if session.error:
        log.error("call failed: '%s'" % session.message)
    else:
        for type in ['cvlan','suni','tuni']:
            for l2vsn in l2vsns[type]:
                l2vsnList.append(l2vsn['isid'])
        log.info("got all %s L2VSNs" % len(l2vsnList))
    return l2vsnList

########################################################################
def setL2vsn(isid):
    global callCount
    session.call(
        type = 'POST',
        subUri = '/v0/configuration/spbm/l2/isid',
        body = {
            "isidType": "SUNI",
            "isid": isid,
            "name": "API-Test-%s" % isid,
        }
    )
    
    if session.error:
        log.error("set L2VSN failed: '%s'" % session.message)
        exit(3)
    else:
        log.info("set L2VSN Test-%s [%s] in %0.3f seconds" % (isid,isid,session.elapsed))
        callCount += 1

########################################################################

log = setupLogger()

config = readConfig()

session = login(config['connection'])

l2vsns = getAllL2vsn()

for isidId in range(config['isid']['start'], config['isid']['start'] + config['isid']['range']):
    if not isidId in l2vsns:
        setL2vsn(isidId)
    else:
        log.info("L2VSN %s already exists, skipping" % isidId)
        continue
