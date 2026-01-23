#!/usr/bin/env python3

###########################################################################
#
# written by Markus Nikulski
#            mnikulski@extremenetworks.com
#            created 17. Jul. 2025
#            updated 21. Jan. 2026
# 
# Note: this is class is not offical supported by Extreme Networks
#
###########################################################################

import json
import time, logging, requests, urllib3
from datetime import datetime
urllib3.disable_warnings()

log = logging.getLogger('ExtremeOpenAPI')
debug  = False

#####################################################################################################
class OpenAPI():
    '''OpenAPI interface for Fabric Engine'''

    __version__ = "0.0.1"
    __author__  = "Markus Nikulski (mnikulski@extremenetworks.com)"

    #################################################################################################
    def __init__(self, host: str, username: str, password: str):
        '''Create Extreme OpenAPI session object'''
        if debug:
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 1
            log.setLevel( logging.DEBUG )

        log.debug("Extreme OpenAPI version %s" % OpenAPI.__version__)

        self.host       = host                                          # Fabric Engine (aka VSP) IP address or FQDN
        self.port       = str(9443)                                     # TCP port
        self.nbiUrl     = 'https://'+host+':'+self.port+'/rest/openapi' # API URL
        self.username   = username                                      # API authentication
        self.password   = password                                      # API authentication
        self.timeout    = 60                                            # session timeout in seconds
        self.token      = None                                          # session authentication token
        self.data       = None                                          # last query result
        self.error      = False                                         # error tracker (boolen)
        self.message    = ''                                            # error message
        self.expire     = 0                                             # time when the session will expire
        self.elapsed    = 0                                             # time taken to execute last call
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
            log.debug("Extreme OpenAPI session expired, force re-login")
            self.expire  = 0
            self.session = self._login()
            return True

    #################################################################################################
    def _login(self):
        '''internal use only'''
        token_url = 'https://'+ self.host +':'+ str(self.port) +'/auth/token'
        headers   = {"Content-Type": "application/json", "Accept'":  "application/json"}
        body      = {'username': self.username,'password': self.password}
        try:
            response = requests.post(token_url, auth=(self.username, self.password), headers=headers, json=body, verify=False, timeout=5)
            log.debug("login passed in %0.3f seconds" % response.elapsed.total_seconds())
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
            self.token  = result[u'token']
            self.expire = result[u'ttl'] + time.mktime( datetime.today().timetuple() )
            session         = requests.Session()
            session.verify  = False
            session.timeout = self.timeout
            session.headers.update({'Accept':        'application/json',
                                    'Content-type':  'application/json',
                                    'X-Auth-Token':  self.token,
                                    'Cache-Control': 'no-cache',
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
    def call(self,type: str, subUri: str, body: str = None):
        '''internal use only'''
        self.error = False
        self.message = ""
        self.elapsed = 0
        self._ifExpire()
        log.debug("Call %s URI: %s BODY: '%s'" % (type,subUri,body))
        if type == 'GET':
            response = self.session.get(self.nbiUrl + subUri)
        elif type == 'POST':
            response = self.session.post(self.nbiUrl + subUri,json=body)
        elif type == 'PUT':
            response = self.session.put(self.nbiUrl + subUri,json=body)
        elif type == 'PATCH':
            response = self.session.patch(self.nbiUrl + subUri,json=body)
        elif type == 'DELETE':
            response = self.session.delete(self.nbiUrl + subUri)
        else:
            self.message = "unsupported HTTP method '%s'" % type
            self.error = True
            return False
        
        self.elapsed = response.elapsed.total_seconds()
        return self._checkResponse(type,response)

    #################################################################################################
    def _checkResponse(self,type: str, response: object):
        if response.status_code >= 200 and response.status_code < 300:      # 2xx
            if response.status_code == requests.codes.no_content:           # 204
                #log.debug("call %s passed in %0.3f seconds, no body given" % (type, response.elapsed.total_seconds()))
                return True
            else:
                log.debug("call %s passed in %0.3f seconds, body:\n%s" % (type, response.elapsed.total_seconds(), json.dumps(response.json(), indent=2, sort_keys=True)))
                return response.json()
        else:
            try:
                result = response.json()
                self.message = result['errorMessage']
            except:
                self.message = "HTTP error %s" % response.status_code
            self.error = True
            return False
    
#####################################################################################################
#######################################      self test      #########################################
#####################################################################################################
if __name__ == "__main__":
    print(OpenAPI._login.__doc__)
    print("##############################################################")
    print(" DOCUMENTATION: " + OpenAPI.__doc__ )
    print("         CLASS: " + OpenAPI.__name__ )
    print("       VERSION: " + str(OpenAPI.__version__) )
    print("        AUTHOR: " + str(OpenAPI.__author__) )
    print("#############################################################")
    print("##                        Self Test                        ##")
    print("#############################################################")
 