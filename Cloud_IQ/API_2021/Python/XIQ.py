#!/usr/bin/env python

###########################################################################
#
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            7. Mar. 2022
# 
# Note: this is class is not offical supported by Extreme Networks
#
###########################################################################

import json, time, base64, logging
from datetime import datetime
import requests, urllib3
urllib3.disable_warnings()                                              # supress SSL certificate  warning

log     = None
debug   = False

#####################################################################################################
class API():
    '''XIQ API'''
    __version__ = "0.0.1"
    __author__  = "Markus Nikulski (mnikulski@extremenetworks.com)"

    #################################################################################################
    def __init__(self, userName: str , passwd: str):
        global log
        
        if not logging.getLogger().hasHandlers():
            logging.basicConfig( level=logging.ERROR )
        log = logging.getLogger()
        log.debug("XIQ API version %s" % API.__version__)

        if debug:
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 1
            log.setLevel( logging.DEBUG )

        self.url        = 'https://api.extremecloudiq.com/'             # API URL
        self.userName   = userName                                      # API authentication
        self.passwd     = passwd                                        # API authentication
        self.timeout    = 10                                            # session timeout in seconds
        self.token      = None                                          # authentiction token
        self.data       = None                                          # last query result
        self.error      = False                                         # error tracker (boolen)
        self.message    = ''                                            # error message
        self.expire     = 0                                             # time when the session will expire
        self.renewTime  = 90                                            # in procentage of the max expire time
        self.session    = self._login()

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
        try:
            response = requests.post(   self.url + 'login',
                                        headers = { 'Accept':       'application/json',
                                                    'Content-type': 'application/json'
                                                  },
                                        json    = { 'username': self.userName,
                                                    'password': self.passwd
                                                  },
                                        verify  = False,
                                        timeout = self.timeout
                                    )
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
        
        if response.status_code == requests.codes.ok:                           # 200
            result = response.json()
            self.token  = result[u'access_token']

            xmcTokenElements = self.token.split('.')
            tokenData        = json.loads( base64.b64decode(xmcTokenElements[1]+ "==") )
            self.expire      = self._computeExpireTime( datetime.fromtimestamp( tokenData['iat'] ), datetime.fromtimestamp( tokenData['exp'] ) )
            log.debug('            Issuer: %s' % tokenData['iss'] )
            log.debug('           Subject: %s' % tokenData['sub'] )
            log.debug('       Customer-ID: %s' % tokenData['customer_id'] )
            log.debug('               HIQ: %s' % tokenData['hiq_enabled'] )
            log.debug('         XIQ-Roles: %s' % tokenData['role'] )
            log.debug('       Data Center: %s' % tokenData['data_center'] )
            log.debug('            Region: %s' % tokenData['shard'] )
            log.debug('         Issued at: %s' % datetime.fromtimestamp( tokenData['iat'] ) )
            log.debug('   Expiration Time: %s' % datetime.fromtimestamp( tokenData['exp'] ) )

            session         = requests.Session()
            session.verify  = False
            session.timeout = self.timeout
            session.headers.update({'Accept':           'application/json',
                                    'Content-type':     'application/json',
                                    'Authorization':    'Bearer '+ self.token
                                    })

            return session
        
        elif response.status_code == requests.codes.unauthorized:               # 401
            self.message = "authentication failed"
        elif response.status_code == requests.codes.not_found:                  # 404
            self.message = "URL not found"
        elif response.status_code == requests.codes.method_not_allowed:         # 405
            self.message = "Method Not Allowed"
        elif response.status_code == requests.codes.internal_server_error:      # 500
            self.message = "Internal Server Error"
        else:
            self.message = "HTTP-ERROR: " + str(response.status_code)
        self.error = True
        
    #################################################################################################
    def call(self, type, subUrl, data=None):
        self.message = ''
        self.error   = False

        if self._ifExpire():
            log.debug("XIQ API session expired, force re-login")
            self.expire  = 0
            self.session = self._login()
        
        if data: log.debug("request body:\n%s" % data)

        if type == 'GET':
            return self._decode_response( self.session.get( self.url + subUrl ) )
        elif type == 'POST':
            return self._decode_response( self.session.post( self.url + subUrl, json = data ) )
        elif type == 'PUT':
            params = ''
            for item in data:
                params += "%s=%s&" % (item, data[item])
            return self._decode_response( self.session.put( self.url + subUrl +'?'+ params  ) )
        elif type == 'DELETE':
            return self._decode_response( self.session.delete( self.url + subUrl ) )
        else:
            self.message = "HTML call %s unknow" % type
            self.error = True
            return False
        
    #################################################################################################
    def _decode_response(self, response: str):
        '''internal use only'''
        data_out   = None
        self.error = True

        log.debug("response body:\n%s" % response.text)

        if response.status_code == requests.codes.ok:
            try:
                data_out   = json.loads( response.text )
                self.error = False
            except:
                self.message = "no JSON data given"
                return False
        elif response.status_code == requests.codes.unauthorized:               # 401
            self.message = "authentication failed"
        elif response.status_code == requests.codes.not_found:                  # 404
            self.message = "URL not found"
        elif response.status_code == requests.codes.method_not_allowed:         # 405
            self.message = "Method Not Allowed"
        elif response.status_code == requests.codes.internal_server_error:      # 500
            self.message = "Internal Server Error"
        else:
            self.message = 'HTTP-ERROR: ' + response.reason + ' (' + str(response.status_code) + ')'
        
        if self.error:
            self.message = self.message
            self.data   = None
            return False
        else:
            if debug:
                callTine = float("{0:0.1f}".format( response.elapsed.total_seconds() * 1000 ))
                log.debug('executed in %s ms' % callTine )
            self.data = data_out
            return True

    #################################################################################################
    def getDevices(self):
        '''pull all devices'''
        return self.call( 'GET', 'devices' )

#####################################################################################################
#######################################      self test      #########################################
#####################################################################################################

if __name__ == "__main__":
    print("###################################################################")
    print(" DOCUMENTATION: " + API.__doc__ )
    print("         CLASS: " + API.__name__ )
    print("       VERSION: " + str(API.__version__) )
    print("        AUTHOR: " + str(API.__author__) )
    print("###################################################################")
