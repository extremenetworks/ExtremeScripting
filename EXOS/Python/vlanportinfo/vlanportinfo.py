#!/usr/bin/env python
#Python Scripts provided by Extreme Networks.

#This script is provided free of charge by Extreme.  We hope such scripts are helpful when used in conjunction with Extreme products and technology; however, scripts are provided simply as an accommodation and are not supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME ARE HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.

import exsh
import json

FORMAT = '{prt:<8.8} {vlanType}:{tagged}'
print FORMAT.format(prt='Port', vlanType='untagged', tagged='tagged')
portRslt = exsh.clicmd(
    'debug cfgmgr show next vlan.show_ports_info format portList=* port=None', True)
portDict = json.loads(portRslt)
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
        print FORMAT.format(prt=port, vlanType='none', tagged='')
        continue
    if len(untaggedVlan):
        print FORMAT.format(prt=port, vlanType='untagged', tagged=', '.join(untaggedVlan))
        port = ''
    if len(taggedVlan):
        print FORMAT.format(prt=port, vlanType='tagged', tagged=', '.join(taggedVlan))
