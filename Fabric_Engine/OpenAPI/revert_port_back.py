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
def revertPort(port):
    '''disable flex-uni on port & enable auto-sense'''
    # flex uni control not jet integrated in 9.3.1 API, using CLI anternatively
    session.call(
        type = 'POST',
        subUri = '/v0/operation/system/cli',
        body = [
            "configure terminal",
            "interface gigabitEthernet %s" % port.replace(':','/'),
            "no flex-uni enable"
        ]
    )
    log.info("disabled flex-uni on port %s" % port)

    session.call(
        type = 'PATCH',
        subUri = '/v0/configuration/autosense/port/%s' % port,
        body = {
            "enable": True
        }
    )
    log.info("enabled auto-sense on port %s" % port)



########################################################################

log = setupLogger()

config = readConfig()

session = login()

revertPort(config['isidPort'])

revertPort(config['vlanPort'])
