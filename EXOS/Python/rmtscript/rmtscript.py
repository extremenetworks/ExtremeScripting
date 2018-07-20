#!/usr/bin/env python
# Python Scripts provided by Extreme Networks.

# This script is provided free of charge by Extreme.  We hope such scripts are
# helpful when used in conjunction with Extreme products and technology;
# however, scripts are provided simply as an accommodation and are not
# supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME ARE
# HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS
# THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.

#
# This script requires a python environment to run.
# In addition the requests module must also be installed
#
# This is an example of using the EXOS JSONRPC 'runscript' method.
# The command line expects a number of arguments
#usage: rmtscript [-h] -i IPADDRESS [-u USERNAME] [-p PASSWORD]
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -i IPADDRESS, --ipaddress IPADDRESS
#                        IP address of remote system
#  -u USERNAME, --username USERNAME
#                        Login username for the remote system
#  -p PASSWORD, --password PASSWORD
#                        Login password for the remote system
#  -d, --debug           Enable debug
#
# The -s option specifies the path of a script that would be run localy on the switch
# using the CLI command 'run script <pythonscript>.py'
#
# E.g.  The following is in a file sample.py on your local pc
#   exsh.clicmd('create vlan 10-20')
#   exsh.clicmd('config vlan 10-20 add ports all tagged')
#   print exsh.clicmd('show vlan',capture=True)
#
# To pass this to an EXOS switch using this script:
# on your server:
#
# python rmtscript.py -i 10.10.10.1 -u admin
#
# The rmtscript.py starts running and prompts:
#
# run script <file> [args]: sample.py -a -b def
#   sample.py is sent to the switch with the command line args -a -b def
#   It would be the same as transfering sample.py to a switch and running the following command
#       run script sample.py -a -b def
#   The sample.py stdout and stderr are captured and returned to the server
#
#

from __future__ import print_function
import argparse
import json
import requests
import getpass
try:
    import readline
except:
    pass

#
# This class contains the specifics of constructing a JSONRPC message and
# returning the results
class JsonRPC(object):

    def __init__(self, ipaddress, username=None, password=None, method='runscript'):
        self.ipaddress = ipaddress
        self.username = username
        self.password = password
        self.transaction = 0
        self.cookie = None
        # construct a URL template for the EXOS JSONRPC POST message
        self.url = 'http://{ip}/jsonrpc'.format(ip=self.ipaddress)
        self.json_request = {'method' : method,
                            'id' : self.transaction,
                            'jsonrpc' : '2.0',
                            'params' : None
                            }

    def send(self, params):
        # This method:
        #   fills out the JSONRPC POST data structures
        #   Sends the POST via HTTP to the EXOS switch
        #   gets the POST response
        #   returns the decoded JSON in native python structures


        # http headers
        headers = {'Content-Type': 'application/json'}

        # increment the JSONRPC transaction counter
        self.transaction += 1
        self.json_request['id'] = self.transaction

        # JSONRPC defines params as a list
        # EXOS expects the CLI command to be a string in a single list entry
        self.json_request['params'] = params

        # after the first authentication, EXOS returns a cookie we can use
        # in JSONRCP transactions to avoid re-authenticating for every transaction
        #
        # if we have a cookie from previsous authentication, use it
        # send the JSONRPC message to the EXOS switch
        if self.cookie:
            headers['Cookie'] = 'session={0}'.format(self.cookie)
            response = requests.post(self.url,
                headers=headers,
                json=self.json_request)
        else:
            response = requests.post(self.url,
                headers=headers,
                auth=(self.username, self.password),
                json=self.json_request)

        # interpret the response from the EXOS switch
        # first check the HTTP error code to see if HTTP was successful
        # delivering the message
        if response.status_code == requests.codes.ok:
            # if we have a cookie, store it so we can use it later
            self.cookie = response.cookies.get('session')
            try:
                # ensure the response is JSON encoded
                jsonrpc_response = response.json()

                # return the JSONRPC response to the caller
                return jsonrpc_response
            except Exception as e:
                raise e

        # raise http exception
        response.raise_for_status()

def get_params():
    # These are the command line options for rmtscript
    parser = argparse.ArgumentParser(prog = 'rmtscript')
    parser.add_argument('-i', '--ipaddress',
            help='IP address of remote system',
            default=None)
    parser.add_argument('-u', '--username',
            help='Login username for the remote system')
    parser.add_argument('-p', '--password',
            help='Login password for the remote system',
            default='')
    args = parser.parse_args()
    return args


def main():
    args = get_params()
    if args.ipaddress is None:
        # prompt for ip address of the remote system
        args.ipaddress = raw_input('Enter remote system IP address: ')

    if args.username is None:
        # prompt for username
        args.username = raw_input('Enter remote system username: ')
        # also get password
        args.password = getpass.getpass('Remote system password: ')

    # create a JSONRPC interface object
    jsonrpc = JsonRPC(args.ipaddress, username=args.username, password=args.password, method='runscript')

    while True:
        # prompt the user for an EXOS command
        cmd = input('run script <file> [args]: ')
        if cmd in ['q','quit','exit']:
            break

        # split the user input into parts
        script_args = cmd.split()

        # first token must be the local script file name
        script_name = script_args[0]

        # where there any additional command line args to pass to the script on the switch
        script_options = script_args[1:] if len(script_args) > 1 else []


        try:
            # open up the script name provided by the user
            with open(script_name, 'r') as fd:
                # read the entire script into the first params entry
                params = [fd.read()]
        except Exception as e:
            print(e)
            continue

        # add any additional parameters to the params list
        params += script_options

        # send the script and parameters to the switch for processing
        try:
            response = jsonrpc.send(params)
        except Exception as e:
            print(e)
            continue

        # extract the response stored in 2 variables 'stdout' and 'stderr'
        result = response.get('result')
        if result:
            if result.get('stdout'):
                print(result.get('stdout'))

            # if something was output to stderr, print that last
            if result.get('stderr'):
                print('STDERR\n',result.get('stderr'))
try:
    main()
except KeyboardInterrupt:
    pass
