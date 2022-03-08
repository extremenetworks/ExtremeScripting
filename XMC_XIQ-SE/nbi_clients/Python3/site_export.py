#!/usr/bin/env python

##############################################################
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            08 Mar 2022
##############################################################

import XMC_NBI

##############################################################
xmcServerIp = '192.168.162.50'
xmcClientID = 'DVDnjOaqMQ'
xmcSecret   = '8c12a0e1-87f8-4b18-a8d1-2e8c74d27c65'
file        = 'site.txt'
session     = None

##############################################################
def login():
    global session
    session = XMC_NBI.XMC_NBI(xmcServerIp, xmcClientID, xmcSecret)
    if session.error:
        print( "ERROR: '%s'" % session.message )
        exit(1)

##############################################################
def pullSites():
    data = session.getSites()
    if session.error:
        print( "ERROR: get sites fialed '%s'" % session.message )
    else:
        return data

##############################################################
def writeToFile(content):
    try:
        with open(file, 'w') as FILE_HANDLE:
            for line in content:
                FILE_HANDLE.write( line + "\n")
            
            FILE_HANDLE.close()

            print("INFO: write file '%s'" % file)
    except IOError:
        print("ERROR: write file '%s' failed" % file)

##############################################################

login()

sites = pullSites()

print("INFO: found %s sites" % len(sites) )
for site in sorted( sites ):
    print( "\t%s" % site )

writeToFile( sites )
