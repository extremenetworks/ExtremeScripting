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
addAllow    = True
deleteAllow = True
session     = None

##############################################################
def login():
    global session
    session = XMC_NBI.XMC_NBI(xmcServerIp, xmcClientID, xmcSecret)
    if session.error:
        print( "ERROR: '%s'" % session.message )
        exit(1)

##############################################################
def syncSitesToXmc( sites ):
    changes = False
    pending = False

    xmcSites = session.getSites()

    if session.error:
        print( "ERROR: get sites failed '%s'" % session.message )
        exit(1)
    else:
        for site in sorted(sites):
            if site in xmcSites:
                continue
            else:
                if addAllow:
                    session.addSite( site )
                    if session.error:
                        print( "ERROR: create site '%s' failed: '%s'" % (site,session.message) )
                    else:
                        print("INFO: create site '%s'" % site)
                        changes = True
                else:
                    print("INFO: site '%s' have to be added" % site)
                    pending = True

        for site in list( reversed(xmcSites) ):
            if site in sites:
                continue
            else:
                if deleteAllow:
                    if not site == "/World":
                        session.deleteSite( site )
                        if session.error:
                            print( "ERROR: delete site '%s' failed: '%s'" % (site,session.message) )
                        else:
                            print("INFO: delete site '%s'" % site)
                            changes = True
                else:
                    print("INFO: site '%s' have to be deleted" % site)
                    pending = True

    if pending:
        print("WARN: not all in sync")
    elif not changes:
        print("INFO: all in sync")

##############################################################
def readFromFile(file):
    data = []
    
    try:
        with open(file, 'r') as FILE_HANDLE:
            content = FILE_HANDLE.readlines()
            FILE_HANDLE.close()
            print("INFO: read file '%s'" % file)
    except IOError:
        print("ERROR: read file '%s' failed" % file)
        exit(1)

    for line in (line.rstrip('\n')  for line in content):
        data.append( line )

    #print("INFO: found %s sites in file" % len(sites) )
    #for site in sorted( sites ):
    #    print( "\t%s" % site )

    return data

##############################################################
def normalizeData(sites):
    siteList = []

    for site in sites:
        if site not in siteList:
            siteList.append( site )
        else:
            print("WRANING: site '%s' exist more than one time in the listing" % site)

    itemCounts = [2,3,4,5,6,7,8,9]
    siteToAdd = []
    for site in siteList:
        newSite = "/World"
        items = site.split('/')
        for count in itemCounts:
            if len( items ) > count:
                newSite = newSite + '/' + items[count]
                if not newSite in siteList and  not newSite in siteToAdd:
                    siteToAdd.append( newSite )

    for site in siteToAdd:
        siteList.append( site )
        print("INFO: for data normalisation add site '%s' to the list" % site)

    return siteList

##############################################################

sites = readFromFile( file )

sites = normalizeData( sites )

login()
 
syncSitesToXmc( sites )
