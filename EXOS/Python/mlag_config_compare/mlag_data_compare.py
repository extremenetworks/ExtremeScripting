import json
from exsh import clicmd
from sys import exit

def get_mlag_peers():
    mlagpeerRslt = json.loads(clicmd('debug cfgmgr show next vsm.mLagPeer', True))
    mlag_peer = []
    dup = False
    for peerRow in mlagpeerRslt['data']:
        for peer in mlag_peer:
            if peer['peerName'] == peerRow['peerName'] or peerRow['peerName'] == None:
                dup = True
        if dup is True:
            pass
        else:
            mlag_peer.append({'peerName': str(peerRow['peerName']),
                              'peerIpAddr': str(peerRow['peerIpAddr']),
                              'localIpAddr': str(peerRow['localIpAddr']),
                              'vlan': str(peerRow['vlan'])})
    return mlag_peer


def get_mlag_ports():
    mlagportRslt = json.loads(clicmd('debug cfgmgr show next vsm.mLagPort', True))
    mlag_ports = []
    dup = False
    for mportRow in mlagportRslt['data']:
        for peer in mlag_ports:
            if mportRow['peerName'] == None:
                dup = True
            if peer['peerName'] == mportRow['peerName'] and peer['idx'] == mportRow['idx']:
                dup = True
        if dup is True:
            pass
        else:
            mlag_ports.append({'peerName': str(mportRow['peerName']),
                              'idx': str(mportRow['idx']),
                              'port': str(mportRow['port']),
                              'localportstate': str(mportRow['lclLinkState']),
                              'remoteportstate': str(mportRow['rmtLinkState'])})
    return mlag_ports


def get_port_vlans(port):
    vlanRslt = json.loads(clicmd('debug cfgmgr show next vlan.show_ports_info_detail_vlans port={0} vlanIfInstance=None'.format(port), True))
    port_data = []
    for vlanRow in vlanRslt['data']:
        port_data.append({'VlanName': str(vlanRow['vlanName']).lower(), 'VlanId': str(vlanRow['vlanId']), 'tag' : str(vlanRow['tagStatus'])})
    return port_data


def get_port_vlan_list(port):
    vlanRslt = json.loads(clicmd('debug cfgmgr show next vlan.show_ports_info_detail_vlans port={0} vlanIfInstance=None'.format(port), True))
    port_data = []
    for vlanRow in vlanRslt['data']:
        port_data.append(str(vlanRow['vlanName']))
    return port_data


def get_vlan_ports(vlan):
    vlanportsRslt = json.loads(clicmd('debug cfgmgr show one vlan.vlanPort vlanName={0}'.format(vlan), True))

    return  ({'untagged' : str(vlanportsRslt['data'][0]['untaggedPorts']), 'tagged' : str(vlanportsRslt['data'][0]['taggedPorts'])})

peer_info = get_mlag_peers()

def main():
    peer_info = get_mlag_peers()
    mports = get_mlag_ports()
    data = []
    if len(peer_info) == 1:
        peer_info = peer_info[0]
        port_check = get_vlan_ports(peer_info['vlan'])
    
        if port_check['untagged'] == 'None':
            isc_port = port_check['tagged']
        if port_check['tagged'] == 'None':
            isc_port = port_check['untagged']
    print ("###############################")
    print ("MLAG peer is {0}").format(peer_info['peerName'])
    print ("###############################")
    print ("")
    print ("KEY:")
    print ("VLAN Name : VLAN ID : Tag 0/1")
    print ("")
    print ("------------------------------------")
    print ("ISC port {0}").format(isc_port)
    print ("------------------------------------")
    for isc_vlans in get_port_vlans(isc_port):
        print ("{0} : {1} : {2}").format(isc_vlans['VlanName'],isc_vlans['VlanId'],isc_vlans['tag'])
    print ("")
    
    for port in mports:
        print ("------------------------------------")
        print ("MLAG Port {0}, ID: {1}, Rpeer : {2}").format(port['port'], port['idx'], port['remoteportstate'])
        print ("------------------------------------")
        for mvlan in get_port_vlans(port['port']):
            print ("{0} : {1} : {2}").format(mvlan['VlanName'],mvlan['VlanId'],mvlan['tag'])
        print ("")

if len(peer_info) > 1:
    print ("This script does not support two MLAG peers.")
else:
    main()
