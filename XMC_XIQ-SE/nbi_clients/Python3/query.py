#!/usr/bin/env python

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
macAddress  = '11:22:33:44:55:66'
esGroup     = 'Printers'

##############################################################
session = XMC_NBI.XMC_NBI(xmcServerIp, xmcClientID, xmcSecret)
if session.error:
    print( "ERROR: '%s'" % session.message )
    exit(1)

query = '''
mutation {
  accessControl {
    addMACToEndSystemGroup(
        input: {
            group: "<GROUP>"
            value: "<MAC>"
            description: "just a test"
            custom1: "first"
            custom2: "second"
            custom3: "third"
            custom4: "four"
        }
    ) {
        status
        message
    }
  }
}
'''
query = query.replace("<MAC>", macAddress)
query = query.replace("<GROUP>", esGroup)
data  = session.query( query )
if not data['accessControl']['addMACToEndSystemGroup']['status'] == 'SUCCESS':
    print("ERROR: unable to add MAC address: %s" % data['accessControl']['addMACToEndSystemGroup']['message'])
else:
    print("INFO: add MAC address "+ macAddress)

queryInput = '''
{
  accessControl {
    endSystemInfoByMac(macAddress: "<MAC>") {
      endSystemInfo {
        custom1
        custom2
        custom3
        custom4
        groupDescr1
      }
    }
  }
}
'''
data = session.query( queryInput.replace("<MAC>", macAddress) )
for item in data['accessControl']['endSystemInfoByMac']['endSystemInfo']:
    print("INFO: MAC data: %s = %s" % (item, data['accessControl']['endSystemInfoByMac']['endSystemInfo'][item]) )

query = '''
mutation {
  accessControl {
    removeMACFromEndSystemGroup (input: {
      value: "<MAC>"
      group: "<GROUP>"
      reauthenticate: true
    }) {
      status
      message
    }
  }
}
'''
query = query.replace("<MAC>", macAddress)
query = query.replace("<GROUP>", esGroup)
data  = session.query( query )
if not data['accessControl']['removeMACFromEndSystemGroup']['status'] == 'SUCCESS':
    print("ERROR: unable to delete MAC address: %s" % data['accessControl']['removeMACFromEndSystemGroup']['message'])
else:
    print("INFO: delete MAC address "+ macAddress)
