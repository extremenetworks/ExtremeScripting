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

# This is an example script to demostrate how to access and EXOS switch running
# 21.1.x or later using the JSONRPC cli method.
#
# the JSONRCP cli method processes an EXOS CLI command and returns:
#   the data structures that were used to contruct the CLI output
#   the actual CLI display output. This output is assigned to a variable
#
# The intent is to use published EXOS CLI 'show' commands but return the
# data structures used to create the display.
# This enables remote automation systems to programatically
# collect data from an EXOS switch without the need to 'screen scrape' the CLI
# display to get the desired information.
#
# This script runs on PC or server and accesses an Extreme EXOS switch via JSONRPC.
# It requires:
#   the IP address of the EXOS switch
#   the user name and password for the remote switch
#
# The script then prompts for an EXOS CLI command. Usually a 'show' command.
# The response are the data structures used to format a command along with a variable
# CLIoutput containing the formatted command response for reference.
#
#usage: jsoncli [-h] [-i IPADDRESS] [-u USERNAME] [-p PASSWORD] [-d]
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -i IPADDRESS, --ipaddress IPADDRESS
#                        IP address of remote system
#  -u USERNAME, --username USERNAME
#                        Login username for the remote system
#  -p PASSWORD, --password PASSWORD
#                        Login password for the remote system
#
#
#> jsoncli.py
#Enter remote system IP address: 10.68.65.81
#Enter remote system username: admin
#Remote system password:
#Enter EXOS cli: show port 1 statistics
#JSONRPC Response for: show port 1 statistics
#********************************************************************************
#{
#  "id": 1,
#  "jsonrpc": "2.0",
#  "result": [
#    {
#      "CLIoutput": "Port      Link       Tx Pkt     Tx Byte      Rx Pkt     Rx Byte      Rx Pkt      Rx Pkt      Tx Pkt      Tx Pkt\n          State       Count       Count       Count       Count       Bcast       Mcast       Bcast       Mcast\n========= ===== =========== =========== =========== =========== =========== =========== =========== ===========\nLongDisp> R               0           0           0           0           0           0           0           0\n========= ===== =========== =========== =========== =========== =========== =========== =========== ===========\n          > in Port indicates Port Display Name truncated past 8 characters\n          > in Count indicates value exceeds column width. Use 'wide' option or '0' to clear.\n          Link State: A-Active, R-Ready, NP-Port Not Present, L-Loopback\n"
#    },
#    {
#      "show_ports_stats": {
#        "displayString": "LongDisplayStrin",
#        "dot1dTpPortInDiscards": 0,
#        "dot1dTpPortInFrames": 0,
#        "dot1dTpPortMaxInfo": 1500,
#        "dot1dTpPortOutFrames": 0,
#        "linkState": 0,
#        "port": 1,
#        "portList": 1,
#        "portNoSnmp": 1,
#        "rxBcast": 0,
#        "rxByteCnt": 0,
#        "rxMcast": 0,
#        "rxPktCnt": 0,
#        "txBcast": 0,
#        "txByteCnt": 0,
#        "txMcast": 0,
#        "txPktCnt": 0
#      },
#      "status": "SUCCESS"
#    }
#  ]
#}
#
#Formatted CLIoutput Display
#********************************************************************************
#Port      Link       Tx Pkt     Tx Byte      Rx Pkt     Rx Byte      Rx Pkt      Rx Pkt      Tx Pkt      Tx Pkt
#          State       Count       Count       Count       Count       Bcast       Mcast       Bcast       Mcast
#========= ===== =========== =========== =========== =========== =========== =========== =========== ===========
#LongDisp> R               0           0           0           0           0           0           0           0
#========= ===== =========== =========== =========== =========== =========== =========== =========== ===========
#          > in Port indicates Port Display Name truncated past 8 characters
#          > in Count indicates value exceeds column width. Use 'wide' option or '0' to clear.
#          Link State: A-Active, R-Ready, NP-Port Not Present, L-Loopback
#
#********************************************************************************

import argparse
import json
import readline

#
# This class contains the specifics of constructing a JSONRPC message and
# returning the results
class JsonRPC(object):

    def __init__(self, ipaddress, username=None, password=None, method='cli'):
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

    def send(self, cmds):
        # This method:
        #   fills out the JSONRPC POST data structures
        #   Sends the POST via HTTP to the EXOS switch
        #   gets the POST response
        #   returns the decoded JSON in native python structures

        import requests

        # http headers
        headers = {'Content-Type': 'application/json'}

        # after the first authentication, EXOS returns a cookie we can use
        # in JSONRCP transactions to avoid re-authenticating for every transaction
        #
        # if we have a cookie from previsous authentication, use it
        if self.cookie is not None:
            headers['Cookie'] = 'session={0}'.format(self.cookie)

        # increment the JSONRPC transaction counter
        self.transaction += 1
        self.json_request['id'] = self.transaction

        # JSONRPC defines params as a list
        # EXOS expects the CLI command to be a string in a single list entry
        self.json_request['params'] = [cmds]

        # send the JSONRPC message to the EXOS switch
        response = requests.post(self.url,
            headers=headers,
            auth=(self.username, self.password),
            data=json.dumps(self.json_request))

        # interpret the response from the EXOS switch
        # first check the HTTP error code to see if HTTP was successful
        # delivering the message
        if response.status_code == requests.codes.ok:
            # if we have a cookie, store it so we can use it later
            self.cookie = response.cookies.get('session')
            try:
                # ensure the response is JSON encoded
                jsonrpc_response = json.loads(response.text)

                # return the JSONRPC response to the caller
                return jsonrpc_response
            except:
                return None

        # raise http exception

        response.raise_for_status()


def get_params():
    # These are the command line options for jsoncli
    parser = argparse.ArgumentParser(prog = 'jsoncli')
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
    import getpass
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
    jsonrpc = JsonRPC(args.ipaddress, username=args.username, password=args.password, method='cli')

    # start a CLI prompt loop for the user to enter EXOS commands
    while True:
        # prompt the user for an EXOS command
        cmd = raw_input('Enter EXOS cli: ')
        if cmd in ['q','quit','exit']:
            break

        try:
            # send the command to the EXOS switch over HTTP. the object will do the proper encoding
            response = jsonrpc.send(cmd)

            # print headers
            print 'JSONRPC Response for:', cmd
            print '*' * 80
            print json.dumps(response, indent=2, sort_keys=True)

            # dump the JSONRPC response to the user in a pretty format
            # first the data stuctures
            result = response.get('result')

            # now display any formatted CLI output, just for reference
            try:
                if result is not None:
                    cli_output = result[0].get('CLIoutput')
                    if cli_output is not None:
                        print '\nFormatted CLIoutput Display'
                        print '*' * 80
                        print cli_output
                        print '*' * 80
            except:
                pass
        except Exception as msg:
            print msg

try:
    main()
except KeyboardInterrupt:
    pass
