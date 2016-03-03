#!/usr/bin/env python
#Python Scripts provided by Extreme Networks.

#This script is provided free of charge by Extreme.  We hope such scripts are helpful when used in conjunction with Extreme products and technology; however, scripts are provided simply as an accommodation and are not supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME ARE HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.

import exsh
import json
import sys
ports = '*'
if(len(sys.argv) == 2):
	ports = sys.argv[1]
	
def port_check(port):
    try:
        ports_result = []
        cmd = 'debug cfgmgr show next vlan.show_ports_info portList={0} port=None'.format(port)
        result = json.loads(exsh.clicmd(cmd, capture=True))
        for status in result['data']:
            ports_result.append(status['status'])
        if 'ERROR' in ports_result:
            return False
        else:
            return True
    except RuntimeError as cmdMsg:
        print 'Error:', cmdMsg, ':', cmd
        exsh.clicmd('create log message "flow_mod.py: Error: cmd={0} : msg={1}"'.format(cmd, cmdMsg), capture=False)
        return False

if port_check(ports) == True:

    FORMAT = '{prt:<8.8} {vlanType}:{tagged}'
    print FORMAT.format(prt='Port', vlanType='untagged', tagged='tagged')
    cmd2 = 'debug cfgmgr show next vlan.show_ports_info portList={0} port=None'.format(ports)
    portRslt = exsh.clicmd(cmd2, capture=True)
    portDict = json.loads(portRslt)
    port_output = []
    for row in portDict['data']:
        port = row['port']
        vlanRslt = json.loads(exsh.clicmd(
            'debug cfgmgr show next vlan.show_ports_info_detail_vlans formatted port={0} vlanIfInstance=None'.format(port), True))
        taggedVlan = []
        untaggedVlan = []
        for vlanRow in vlanRslt['data']:
            vid = vlanRow.get('vlanId', None)
            if vid:
                if vlanRow['tagStatus'] == '1':
                    taggedVlan.append(vid)
                else:
                    untaggedVlan.append(vid)
        if len(untaggedVlan) == 0 and len(taggedVlan) == 0:
            cap1 = FORMAT.format(prt=port, vlanType='none', tagged='')
            port_output.append(cap1)
            continue
        if len(untaggedVlan):
            cap2 = FORMAT.format(prt=port, vlanType='untagged', tagged=', '.join(untaggedVlan))
            port_output.append(cap2)
            port = ''
        if len(taggedVlan):
            cap3 = FORMAT.format(prt=port, vlanType='tagged', tagged=', '.join(taggedVlan))
            port_output.append(cap3)
    num_lines=25
    index=0
    for x in port_output:
        index = (index + 1)
        if (index % num_lines) == 0:
            input=raw_input("Hit return key to continue press q then return to quit: ")
            if input.lower() == 'q':
                break
            else:
                print x
        else:
            print x
else:
    print ("Wrong port format or port not on Switch.  Use 1,2,3,4 or 1-5,6,8 or 1:1-5,2:3")