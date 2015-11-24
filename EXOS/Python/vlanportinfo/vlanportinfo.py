#!/usr/bin/env python

# vlanportinfo.py
# This script displays the VLAN assignment and tagging configuration for all ports on the switch.
# 
# Usage: run script vlanportinfo.py
#
# Last updated: November 23, 2015

import exsh
import json

FORMAT = '{prt:<8.8} {vlanType}:{tagged}'
print FORMAT.format(prt='Port', vlanType='untagged',tagged='tagged')
portRslt = exsh.clicmd('debug cfgmgr show next vlan.show_ports_info format portList=* port=None', True)
portDict = json.loads(portRslt)
for row in portDict['data']:
    port = row['port']
    vlanRslt = json.loads(exsh.clicmd('debug cfgmgr show next vlan.show_ports_info_detail_vlans formatted port={0} vlanIfInstance=None'.format(port), True))
    taggedVlan = []
    untaggedVlan = []
    for vlanRow in vlanRslt['data']:
        vid = vlanRow.get('vlanId',None)
        if vlanRow['tagStatus'] == '1':
            if vid:
                taggedVlan.append(vid)
        else:
            if vid:
                untaggedVlan.append(vid)
    if len(untaggedVlan) == 0 and len(taggedVlan) == 0:
        print FORMAT.format(prt=port, vlanType='none', tagged='')
    if len(untaggedVlan):
        print FORMAT.format(prt=port, vlanType='untagged', tagged=', '.join(untaggedVlan))
        port=''
    if len(taggedVlan):
        print FORMAT.format(prt=port, vlanType='tagged', tagged=', '.join(taggedVlan))
