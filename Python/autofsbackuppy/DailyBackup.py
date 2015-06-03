#!/usr/bin/env python
'''
#############################################################################
#
# Script        	: Daily Automatic Backup Script
# Revision      	: 1.0
# EXOS Version(s)  	: 15.5.2 (EXOS supports Python)
# Last Updated  	: 15-Jan-2014
#
# Purpose:
# Run automated back up on all scripts, including configuration, policies, and scripts. Benefits
# include simple rollback and configuration history.
# The first time this script runs, it installs itself into UPM to be called once a day.
#
# MODIFY the user configurations below for your environment
#
'''

import time
import os

###############################################################################
# U S E R   C O N F I G U R A T I O N
###############################################################################
# Preconfigured TFTP Server. Please Set to your TFTP Server
tftp = '10.68.9.32'
# Preconfigured Virtual Router. Please Configure
vrtr  = 'vr-Mgmt'
# Time of day when backup occurs
backupTime = '22:00'


###############################################################################
serial = None
yeardirectory = None
modirectory = None
daydirectory = None
systemTime = None

def exosCmd(cmd):
    #print cmd
    result = exsh.clicmd(cmd, True)
    #print result
    return result


def uploadFiles(fileSuffix, uploadPrefix):
    serialSystem = serial + '_' +  systemTime + '_'
    for line in exosCmd('ls *' + fileSuffix).splitlines():
        line.strip()
        if line.endswith(fileSuffix):
            fileName = line.split()[-1]
            if len(fileName) > 32:
                exosCmd('create log entry "Length Error.File name for ' + fileName + ' exceeded 32 byte max length."')
                exosCmd('create log entry "' + fileName + ' truncated to ' +  fileName[:32] + '"')
                fileName = fileName[:32]
            destFileName = '{yyyy}-{mm}-{dd}_{prefix}{file}{sourceFile}'.format(yyyy=yeardirectory,
                    mm=modirectory,
                    dd=daydirectory,
                    prefix=uploadPrefix,
                    file=serialSystem,
                    sourceFile=fileName)
            cmd = 'tftp put {ipaddress} vr {virtualRouter} {sourceFile} {dest}'.format(ipaddress=tftp,
                    virtualRouter=vrtr,
                    sourceFile=fileName,
                    dest=destFileName)
            print exosCmd(cmd)
            exosCmd('create log entry "File ' + fileName + ' exported to ' + tftp  + ' Server as ' + destFileName + '"')

def upmConfig():
    result = None
    upmName='dailybackup'
    exosCmd('enable cli scripting permanent')
    for line in exosCmd('show upm profile').splitlines():
        if line.startswith(upmName):
            break
    else:
# Creating the Backup UPM
# because we cannot interact with the shell the way TCL can,
# we need to create a separate script that will create the upm profile
        xsfName = __file__.replace('.py','.xsf')
        xsf = open(xsfName,'w')
        xsf.write('create upm profile ' + upmName + '\n')
        xsf.write('load script ' + os.path.basename(__file__) + '\n')
        xsf.write('.\n\n')
        xsf.close()
        exosCmd('load script ' + os.path.basename(xsfName))
        os.remove(xsfName)
# Here we configure the UPM to have a liberal execution time.
        exosCmd('configure upm profile ' + upmName + ' maximum execution-time 1000')
        exosCmd('create log target upm ' + upmName)
        exosCmd('create log filter autologfilter')
        exosCmd('configure log target upm ' + upmName + ' filter autologfilter')
        exosCmd('enable log target upm ' + upmName)
        exosCmd('enable upm profile ' + upmName)
        exosCmd('create log entry "UPM ' + upmName + ' successfully created"')
        result = 1
# Check UPM timer exists
    for line in exosCmd('show upm timers').splitlines():
        if line.startswith(upmName):
            break
    else:
        exosCmd('create upm timer ' + upmName)
        exosCmd('config upm timer ' + upmName + ' profile ' + upmName)
        backupHourMin = backupTime.split(':')
        cmd = 'config upm timer {name} at {mm} {dd} {yy} {hh} {min} 0 every 86400'.format(name=upmName,
                mm=modirectory,
                dd=daydirectory,
                yy=yeardirectory,
                hh=backupHourMin[0],
                min=backupHourMin[1])
        exosCmd(cmd)
        result = 1
    return result


if upmConfig() == None:
    yeardirectory = time.strftime('%Y')
    modirectory = time.strftime('%m')
    daydirectory = time.strftime('%d')
    systemTime = time.strftime('%H%M%S')
    for line in exosCmd('show version').splitlines():
        if line.startswith('Switch'):
            tokens = line.split()
            serial = tokens[3]
            break
# upload policy files
    uploadFiles('.pol','p')
# upload TCL scripts
    uploadFiles('.xsf','s')
# upload Python scripts
    uploadFiles('.py','y')
# upload Config files
    uploadFiles('.cfg','c')

    exosCmd('create log entry "Automated Backup Ran"')

