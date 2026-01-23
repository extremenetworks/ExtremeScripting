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
def prepPort(port):
    '''disable auto-sense & enable flex-uni on port'''
    session.call(
        type = 'PATCH',
        subUri = '/v0/configuration/autosense/port/%s' % port,
        body = {
            "enable": False
        }
    )
    log.info("disabled auto-sense on port %s" % port)

    # flex uni control not jet integrated in 9.3.1 API, using CLI anternatively
    session.call(
        type = 'POST',
        subUri = '/v0/operation/system/cli',
        body = [
            "configure terminal",
            "interface gigabitEthernet %s" % port.replace(':','/'),
            "flex-uni enable"
        ]
    )
    log.info("enabled flex-uni on port %s" % port)

########################################################################
def updateL2vsn(isid,port):
    session.call(
        type = 'POST',
        subUri = '/v0/configuration/spbm/l2/isid/%s/suni' % isid,
        body = {
            "bpduEnabled": False,
            "cvid": isid - 2660000,
            "lagIds": [],
            "portIds": [
                port
            ]
        }
    )
    
    if session.error:
        log.error("update L2VSN port %s failed: '%s'" % (port, session.message))
        exit(3)
    else:
        log.info("update L2VSN Test-%s [%s] port %s in %0.3f seconds" % (isid,isid,port,session.elapsed))

########################################################################

log = setupLogger()

config = readConfig()

session = login()

l2vsns = getAllL2vsn()
callCount += 1

prepPort(config['isidPort'])

for id in range(config['isidStart'], config['isidStart'] + config['isidRange']):
    if id in l2vsns:
        updateL2vsn(id,config['isidPort'])
        callCount += 1
    else:
        log.info("L2VSN %s does not exist, skipping" % id)
        continue
