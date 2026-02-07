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
                log.info("got %s %s [%s]" % (type, l2vsn['name'], l2vsn['isid']))
                l2vsnList.append(l2vsn['isid'])
        log.info("got all %s L2VSNs" % len(l2vsnList))
    return l2vsnList

########################################################################
def getL2VsnConfig(l2vsnId):
    l2vsn = session.call('GET','/v0/configuration/spbm/l2/isid/%s' % l2vsnId)
    if session.error:
        log.error("I-SID config failed: '%s'" % session.message)
        exit(3)
    else:
        log.info("got I-SID config %s [%s] in %0.3f seconds" % (l2vsn['name'],l2vsnId,session.elapsed))

########################################################################

log = setupLogger()

config = readConfig()

session = login(config['connection'])

l2vsns = getAllL2vsn()
callCount += 1

for l2vsn in l2vsns:
    getL2VsnConfig(l2vsn)
    callCount += 1
