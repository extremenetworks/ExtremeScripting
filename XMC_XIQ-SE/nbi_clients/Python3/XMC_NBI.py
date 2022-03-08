#!/usr/bin/env python

###########################################################################
#
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            created 01. Sep. 2020
#            updated 07. Mar. 2022
# 
#   tested against XMC 8.5.7 release
#   tested against XIQ-SE 21.11.11.37 release
#
# Note: this is class is not offical supported by Extreme Networks
#
###########################################################################

import sys, json, time, base64, logging
from datetime import datetime
import requests
import urllib3
urllib3.disable_warnings()                                              # supress SSL certificate  warning

logger = None
debug  = False
getframe_expr = 'sys._getframe({}).f_code.co_name'                      # is required to determinant the call of a routine

#####################################################################################################
class XMC_NBI():
    '''XMC NBI interface'''

    __version__ = "0.0.2"
    __author__  = "Markus Nikulski (mnikulski@extremenetworks.com)"

    #################################################################################################
    def __init__(self, host: str, clientId: str , secret: str , test: bool = False ):
        global logger

        if not logging.getLogger().hasHandlers():
            logging.basicConfig( level = logging.ERROR )
        logger = logging.getLogger()

        if debug:
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 1
            logger.setLevel( logging.DEBUG )

        logger.debug("XMC NBI version %s" % XMC_NBI.__version__)

        self.nbiUrl     = 'https://' + host + ':8443/nbi/graphql'       # API URL
        self.host       = host                                          # XMC IP address or FQDN
        self.port       = 8443                                          # TCP port
        self.clientId   = clientId                                      # API authentication
        self.secret     = secret                                        # API authentication
        self.timeout    = 10                                            # session timeout in seconds
        self.token      = None
        self.data       = None                                          # last query result
        self.test       = test                                          # test mode (boolean)
        self.error      = False                                         # error tracker (boolen)
        self.message    = ''                                            # error message
        self.expire     = 0                                             # time when the session will expire
        self.renewTime  = 90                                            # in procentage of the max expire time
        
        if self.test == False and debug:
            self.test = True
        
        self.session    = self._login()
        if not self.error:
            self._pull_schema()

    #################################################################################################
    def __repr__(self):
        return '%s' % self.__dict__
        
    #################################################################################################
    def __del__(self):
        if self:
            if self.session:
                self.session.close()

    #################################################################################################
    def _computeExpireTime(self, TimeStart, TimeEnd):
        '''internal use only'''
        timeDiff = TimeEnd - TimeStart
        unixtime = time.mktime( datetime.today().timetuple() )
        return     unixtime + ( timeDiff.total_seconds() / 100 * self.renewTime )

    #################################################################################################
    def _ifExpire(self):
        '''internal use only'''
        if self.expire > time.mktime( datetime.today().timetuple() ):
            return False
        else:
            return True

    #################################################################################################
    def _login(self):
        '''internal use only'''
        token_url = 'https://'+ self.host +':'+ str(self.port) +'/oauth/token/access-token?grant_type=client_credentials'
        headers   = {"Content-Type" : "application/x-www-form-urlencoded"}
        
        try:
            response = requests.post(token_url, auth=(self.clientId, self.secret), headers=headers, verify=False, timeout=5)
        except requests.Timeout as error:
            self.message = "timeout reached, host '%s' not responding" % self.host
            self.error = True
            return False
        except requests.TooManyRedirects as error:
            self.message = "too many redirects"
            self.error = True
            return False
        except requests.RequestException as error:
            self.message = "No connection could be made because the target machine actively refused it"
            self.error = True
            return False
        except requests.ConnectionError as error:
            self.message = "connection error '%s'" % error
            self.error = True
            return False
        
        if response.status_code == requests.codes.ok:                   # 200
            result = response.json()
            self.token  = result[u'access_token']

            xmcTokenElements = self.token.split('.')
            tokenData = json.loads( base64.b64decode(xmcTokenElements[1]+ "==") )
            self.expire = self._computeExpireTime( datetime.fromtimestamp( tokenData['iat'] ), datetime.fromtimestamp( tokenData['exp'] ) )

            logger.debug('            Issuer: %s' % tokenData['iss'] )
            logger.debug('           Subject: %s' % tokenData['sub'] )
            logger.debug('            JWT ID: %s' % tokenData['jti'] )
            logger.debug('         XMC-Roles: %s' % tokenData['roles'] )
            logger.debug('         Issued at: %s' % datetime.fromtimestamp( tokenData['iat'] ) )
            logger.debug('   Expiration Time: %s' % datetime.fromtimestamp( tokenData['exp'] ) )
            logger.debug('        Not Before: %s' % datetime.fromtimestamp( tokenData['nbf'] ) )

            session         = requests.Session()
            session.verify  = False
            session.timeout = self.timeout
            session.headers.update({'Accept':           'application/json',
                                    'Content-type':     'application/json',
                                    'Authorization':    'Bearer ' + self.token,
                                    'Cache-Control':    'no-cache',
                                    })

            return session
        
        elif response.status_code == requests.codes.unauthorized:       # 401
            self.message = "authentication failed"
            self.error = True
        elif response.status_code == requests.codes.not_found:          # 404
            self.message = "HTTP-ERROR: URL not found"
            self.error = True
        else:
            self.message = "HTTP-ERROR: " + response.status_code
            self.error = True
            return False

    #################################################################################################
    def _call(self, query: str):
        '''internal use only'''
        if self._ifExpire():
            logger.debug("XMC NBI session expired, force re-login")
            self.expire  = 0
            self.session = self._login()

        return self._decode_response( self.session.post( self.nbiUrl, json = {'query': query} ), eval(getframe_expr.format(2)) )
        
    #################################################################################################
    def _decode_response(self, response: str, caller: str):
        '''internal use only'''
        data_out   = None
        self.error = False
        
        if response.status_code != requests.codes.ok:
            self.message = 'HTTP-ERROR: ' + response.reason + ' (' + str(response.status_code) + ')'
            self.error   = True
        else:
            try:
                data_out = json.loads(response.text)
            except:
                self.message = "call '%s' no JSON data given" % caller
                self.error   = True

            if not self.error:
                if data_out['data'] == None:
                    self.message = data_out['errors'][0]['message']
                    self.error   = True
        
        if self.error:
            self.message = 'call execution error: "%s"' % self.message
            self.error  = True
            self.data   = None
            return False
        else:
            if self.test or debug:
                callTine = float("{0:0.1f}".format( response.elapsed.total_seconds() * 1000 ))
                logger.debug('call %s executed [%s ms]' % (caller, callTine) )
            self.data = data_out['data']
            return True

    #################################################################################################
    def _pull_schema(self):
        '''is just a API test call'''
        schema_nurl = 'https://'+ self.host +':'+ str(self.port) +'/nbi/graphql/schema.idl'
        
        response = self.session.get(schema_nurl)
        
        if response.status_code == requests.codes.ok:       # 200
            self.schema = response.text
        else:
            self.message = "pull NBI schema failed"
            self.error = True

    #################################################################################################
    def query(self, query: str):
        ''' provide NBI graphql code'''
        if self._call( query ):
            return self.data
        else:
            return False

    #################################################################################################
    def getSites(self):
        '''pull all sites'''
        query = '{ network { sites { mapPaths siteName } } }'
        
        if self._call( query ):

            return self.data['network']['sites'][0]['mapPaths']
        else:
            return False

    #################################################################################################
    def addSite(self, name: str):
        '''create a site'''
        query = '''
mutation {
  network {
    createSite(input: {siteLocation: "<NAME>"}) {
      status
      message
    }
  }
}
        '''
        
        if self._call( query.replace('<NAME>',  name) ):
            if self.data['network']['createSite']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['network']['createSite']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def deleteSite(self, name: str):
        '''delete a site'''
        query = '''
mutation {
  network {
    deleteSite(input: {siteLocation: "<NAME>"}) {
      status
      message
    }
  }
}
        '''
        
        if name == "/World":
            self.session.message = 'Site /World is not allowed to be deleted'
            self.error = True
            return False

        if self._call( query.replace('<NAME>',  name) ):
            if self.data['network']['deleteSite']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['network']['deleteSite']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def getDevices(self):
        '''pull all devices'''
        query = '{ network { devices { ip nickName } } }'
        
        if self._call( query ):
            return self.data['network']['devices']
        else:
            return False

    #################################################################################################
    def getDevice(self, ip: str):
        '''pull device details based on IP address'''
        query = '''
{ network { device(ip: "<IP>") {
      firmware
      sitePath
      status
      sysName
      sysContact
      sysLocation
      deviceData {
        serialNumber
        family
        subFamily
      }
      nosIdName
} } }
        '''
        
        if self._call( query.replace('<IP>', ip) ):
            returnData = {}
            if not self.data['network']['device'] == None:
                for key, value in self.data['network']['device'].items():
                    if key == 'deviceData':
                        for key2, value2 in value.items():
                            returnData[key2] = value2
                    elif key == 'status':
                        if value == 1:
                            returnData[key] = 'up'
                        else:
                            returnData[key] = 'down'
                    else:
                        returnData[key] = value
                return returnData
            else:
                return None
        else:
            return False

    #################################################################################################
    def getMacAddresses(self):
        '''pull all AMC addresses'''
        query = '''
{
  accessControl {
    allGroups {
      description
      typeStr
      name
      values
    }
  }
}
        '''
        
        if self._call( query ):
            returnData = {}
            for group in self.data['accessControl']['allGroups']:
                if group['typeStr'] == 'MAC':
                    for mac in group['values']:
                        returnData[mac] = group['name']
            return returnData
        else:
            return None

    #################################################################################################
    def getMacAddress(self, mac: str):
        '''pull MAC details based on MAC address'''
        query = '''
{ accessControl {
    endSystemInfoByMac(macAddress: "<MAC>") {
      endSystemInfo {
        custom1
        custom2
        custom3
        custom4
        memberOfGroups
        groupDescr1
      }
} } }
        '''
        
        if self._call( query.replace('<MAC>', mac) ):
            if not self.data['accessControl']['endSystemInfoByMac']['endSystemInfo'] == None:
                returnData = {}
                for key, value in self.data['accessControl']['endSystemInfoByMac']['endSystemInfo'].items():
                    if key == 'groupDescr1':
                        returnData['groupDescription'] = value
                    elif key == 'memberOfGroups':
                        returnData['groups'] = value
                    else:
                        returnData[key] = value
                return returnData
            else:
                return None
        else:
            return False

    #################################################################################################
    def addMacAddress(self, mac, group, description: str = '', custom1: str = ''):
        '''add MAC using MAC address, group'''
        query = '''
mutation {
  accessControl {
    addMACToEndSystemGroup(input: {
      group: "<GROUP>"
      value: "<MAC>"
      description: "<DESCRIPTION>"
      custom1: "<CUSTOM_1>"
      reauthenticate: true
    }) {
      status
      message
    }
  }
}
        '''
        query = query.replace('<MAC>',         mac)
        query = query.replace('<GROUP>',       group)
        query = query.replace('<DESCRIPTION>', description)
        query = query.replace('<CUSTOM_1>',    custom1)
        
        if self._call( query ):
            if self.data['accessControl']['addMACToEndSystemGroup']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['addMACToEndSystemGroup']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def delMacAddress(self, mac: str, group: str):
        '''delete MAC based on MAC address'''
        query = '''
mutation {
  accessControl {
    removeMACFromEndSystemGroup(input: {
        group: "<GROUP>",
        value: "<MAC>",
        reauthenticate: true
    }) {
      status
      message
    }
  }
}
        '''
        query = query.replace('<MAC>',  mac)
        query = query.replace('<GROUP>',  group)

        if self._call( query ):
            if self.data['accessControl']['removeMACFromEndSystemGroup']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['removeMACFromEndSystemGroup']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def reauthenticateMacAddresses(self, mac: str):
        '''force re-authentication if MAC address in End-System-Event'''
        query = '''
mutation {
  accessControl {
    reauthenticate(input: { macAddress: "<MAC>"  } )
    {
      status
      message
} } }
        '''
        
        if self._call( query.replace('<MAC>', mac) ):
            if self.data['accessControl']['reauthenticate']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['reauthenticate']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def getESGroups(self):
        '''pull all NAC groups'''
        query = '{ accessControl { endSystemCategoryGroupNames } }'
        
        if self._call( query ):
            return self.data['accessControl']['endSystemCategoryGroupNames']
        else:
            return False
    
    #################################################################################################
    def getESGroup(self, groupName: str):
        '''get details about a NAC group'''

        query = '''
{ accessControl {
    group(name: "<GROUP>") {
      description
      name
      typeStr
      values
      valueDescriptions
} } }
        '''
        
        if self._call( query.replace('<GROUP>', groupName) ):
            if not self.data['accessControl']['group'] == None:
                return self.data['accessControl']['group']
            else:
                return None
        else:
            return False

    #################################################################################################
    def createGroup(self, groupName: str, groupType: str, description: str = ''):
        '''create NAC group'''
        query = '''
mutation {
  accessControl {
    createGroup(input: {name: "<GROUP>", type: <TYPE>, description: "<DESC>"}) {
      status
      message
    }
  }
}
 '''
        
        query = query.replace('<GROUP>', groupName)
        query = query.replace('<TYPE>', groupType)
        query = query.replace('<DESC>', description)
        
        if self._call( query ):
            if self.data['accessControl']['createGroup']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['createGroup']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def deleteGroup(self, groupName: str):
        '''delete NAC group'''
        query = '''
mutation {
  accessControl {
    deleteGroup(input: {name: "<GROUP>"}) {
      status
      message
    }
  }
}

 '''
        
        if self._call( query.replace('<GROUP>', groupName) ):
            if self.data['accessControl']['deleteGroup']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['deleteGroup']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def createGroupRuleProfilePolicy(self, group_name: str, vlanId: int, vlanName: str, cfgDomain: str = 'Default'):
        '''create NAC group, rule, profile, policy'''
        query = '''
mutation {
  accessControl {
    createDCMVirtualAndPhysicalNetwork(input: {
      vlanName: "<VLAN-NAME>"
      primaryVlanId: <VLAN-ID>
      name: "<GROUP>"
      nacConfig: "<CONFIG-DOMAIN>"
    }) {
      status
      message
    }
  }
}
 '''
        
        query = query.replace('<GROUP>', group_name)
        query = query.replace('<VLAN-ID>', str(vlanId))
        query = query.replace('<VLAN-NAME>', vlanName)
        query = query.replace('<CONFIG-DOMAIN>', cfgDomain)

        if self._call( query ):
            if self.data['accessControl']['createDCMVirtualAndPhysicalNetwork']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['createDCMVirtualAndPhysicalNetwork']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def createSwitch(self, ip: str, attrToSend: str, pGateway: str, sGateway: str = 'null'):
        '''create switch in NAC'''
        query = '''
mutation {
  accessControl {
    createSwitch(input: {
      ipAddress: "<IP>"
      primaryGateway: "<P-GATEWAY>"
      secondaryGateway: <S-GATEWAY>
      authType: ALL
      attrsToSend: "<ATTR-TO-SEND>"
      radiusAccountingEnabled: true
      nacApplianceGroup: "Default"
    }) {
      status
      message
    }
  }
}
 '''
        
        query = query.replace('<IP>', ip)
        query = query.replace('<P-GATEWAY>', pGateway)
        query = query.replace('<S-GATEWAY>', sGateway)
        query = query.replace('<ATTR-TO-SEND>', attrToSend)
        
        if self._call( query ):
            if self.data['accessControl']['createSwitch']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['createSwitch']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def getSwitches(self):
        '''pull all NAC switches'''
        query = '''
{
  accessControl {
    allSwitches {
      key
      value {
        GetAuthType
        GetSwitchType
        attributesToSend
        authTypeStr
        nacApplianceGroup
        primaryGateway
        radiusAccountingEnabled
        secondaryGateway
        sharedSecret
        switchTypeStr
      }
    }
  }
}

 '''
        
        if self._call( query ):
            if not self.data['accessControl']['allSwitches'] == None:
                newData = {}
                for item in self.data['accessControl']['allSwitches']:
                    newData[ item['key'] ] = item['value']
                return newData
            else:
                return None
        else:
            return False

    #################################################################################################
    def deleteSwitch(self, ip: str):
        '''delete NAC switch'''
        query = '''
mutation {
  accessControl {
    deleteSwitch(input: {
      searchKey: "<IP>"
    }) {
      status
      message
    }
  }
}
 '''
        
        if self._call( query.replace('<IP>', ip) ):
            if self.data['accessControl']['deleteSwitch']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['accessControl']['deleteSwitch']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def enforceNacEnginesAll(self):
        '''enforce all NAC engines'''
        query = '''
mutation {
  accessControl {
    enforceAllAccessControlEnginesForceSwitchesAndPortal {
      status
      message
} } }
'''
        
        if self._call( query ):
            if self.data['accessControl']['enforceAllAccessControlEnginesForceSwitchesAndPortal']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['enforceAllAccessControlEnginesForceSwitchesAndPortal']['reauthenticate']['message']
                self.error = True
                return False
        else:
            return False

    #################################################################################################
    def enforceNacEngineDomain(self, name: str, ip: str = ''):
        '''enforce specific NAC engines'''
        query = '''
mutation {
  accessControl {
    enforceAccessControlEngines( input: {
      engineGroup: "<NAME>"<ENGINE_IP>
    }) {
      status
      message
    }
  }
}
'''
        query = query.replace('<NAME>', name)
        if ip == '':
            query = query.replace('<ENGINE_IP>', '')
        else:
            query = query.replace('<ENGINE_IP>', ',engineIps: "'+ ip +'"')
        
        if self._call( query ):
            if self.data['accessControl']['enforceAccessControlEngines']['status'] == 'SUCCESS':
                return True
            else:
                self.session.message = self.data['enforceAccessControlEngines']['reauthenticate']['message']
                self.error = True
                return False
        else:
            return False

#####################################################################################################
#######################################      self test      #########################################
#####################################################################################################
if __name__ == "__main__":
    print(XMC_NBI.getDevices.__doc__)
    print("##############################################################")
    print(" DOCUMENTATION: " + XMC_NBI.__doc__ )
    print("         CLASS: " + XMC_NBI.__name__ )
    print("       VERSION: " + str(XMC_NBI.__version__) )
    print("        AUTHOR: " + str(XMC_NBI.__author__) )
    print("#############################################################")
    print("##                        Self Test                        ##")
    print("#############################################################")
    debug   = True
    session = XMC_NBI('192.168.162.50', 'DVDnjOaqMQ', '8c12a0e1-87f8-4b18-a8d1-2e8c74d27c65', test=True)
    if session.error:
        print("ERROR: '%s'" % session.message)
        sys.exit(1)
    
    ######
    ip = "192.168.162.11"
    data = session.query('{network{device(ip: "'+ ip +'"){nickName}}}')
    if session.error:
        print("ERROR: NBI query failed '%s'" % session.message )
        sys.exit(1)
    else:
        if not data['network']['device'] == None:
            print("INFO: query result device '%s' is '%s'" % (ip,data['network']['device']['nickName']) )
        else:
            print("INFO query result: device '%s' not given" % ip )

    ####
    device_list = session.getDevices()
    
    if session.error:
        print("ERROR: get devices failed '%s'" % session.message )
        sys.exit(1)
    else:
        print("INFO: query result of %s devices" % len( device_list ) )
        for device in device_list:
            data = session.getDevice( device['ip'] )
            if session.error:
                print("ERROR: get devices failed '%s'" % session.message)
                sys.exit(1)
            else:
                if not data == None:
                    print("INFO: query result device '%s'" % device['ip'] )
                    for key, value in sorted( data.items() ):
                        print("%14s: %s" % (key, value) )
                else:
                    print("WARN: device %s not found" % ip)
            break
    
    ####
    mac_list = session.getMacAddresses()
    if session.error:
        print("ERROR: get MACs failed '%s'" % session.message )
        sys.exit(1)
    else:
        print("INFO: query result of %s MACs" % len( mac_list ) )
        if not mac_list == None:
            for mac, group in sorted( mac_list.items() ):
                mac_data = session.getMacAddress( mac )
                if session.error:
                    print("ERROR: get MAC '' failed '%s'" % (mac, session.message) )
                    sys.exit(1)
                else:
                    if not mac_data == None:
                        print("%18s: %s" % ('MAC', mac) )
                        for key, value in sorted( mac_data.items() ):
                            print("%18s: %s" % (key, value) )
                break
    
    ####
    mac   = '00:11:22:11:22:11'
    group = 'Printers'
    descr = 'is just a test'
    if session.addMacAddress(mac, group, descr ):
        print("INFO: add MAC address %s" % mac)
        mac_data = session.getMacAddress( mac )
        if session.error:
            print("ERROR: get MAC '' failed '%s'" % (mac, session.message) )
            sys.exit(1)
        else:
            if not mac_data == None:
                for key, value in sorted( mac_data.items() ):
                    print("%18s: %s" % (key, value) )
        
        if session.reauthenticateMacAddresses( mac ):
            print("INFO: re-authenticate MAC address %s" % mac )
        else:
            print("WARNING: re-authenticate MAC address %s failed: '%s'" % (mac, session.message) )

        if session.delMacAddress( mac, group ):
            print("INFO: delete MAC address %s" % mac)
        else:
            print("INFO: delete MAC address %s failed: '%s'" % (mac, session.message) )
    else:
        print("INFO: add MAC address %s failed: '%s'" % (mac, session.message) )

    ####
    group_list = session.getESGroups()
    if session.error:
        print("ERROR: get End System Groups failed '%s'" % session.message)
        sys.exit(1)
    else:
        print("INFO: query result of %s End System Groups" % len( group_list ) )
        for group_name in sorted( group_list ):
            group_data = session.getESGroup( group_name )
            if session.error:
                print("ERROR: get End System Groups failed '%s'" % session.message)
                sys.exit(1)
            else:
                print("INFO: query result of group '%s'" % group_name)
                if not group_data == None:
                    for key, value in sorted( group_data.items() ):
                        print("%18s: %s" % (key, value) )
            break
    
    ####
    session.enforceNacEnginesAll()
    if session.error:
        print("ERROR: enfoced all NAC engines failed '%s'" % session.message)
        sys.exit(1)
    else:
        print("INFO: enfoced all NAC engines")

    ####
    nac_domain = 'Default'
    session.enforceNacEngineDomain( nac_domain )
    if session.error:
        print("ERROR: enfoced %s NAC engine failed '%s'" % (nac_domain, session.message) )
        sys.exit(1)
    else:
        print("INFO: enfoced %s NAC engine" % nac_domain)

    sys.exit(0)
