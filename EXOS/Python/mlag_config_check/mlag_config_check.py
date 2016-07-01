# mlag_config_check.py
# This script will check a switch's MLAG config to ensure that there is only one port 
# in the ISC vlan, all vlans added to MLAG port also exist on the ISC port, and that
# all MLAG and ISC ports are active (and added to the aggregator if in a LAG).
#
# If a VLAN is not present on the ISC an option to auto-correct the configuration is provided
#
# The tool also now supports multi-peer MLAG
#
# This does not ensure that the tagging on vlans matches across MLAG peers.
# 
# Last updated: July 1, 2016
import json
from exsh import clicmd
from sys import exit

FMT_ERROR = 'ERROR: {0}'
FMT_CFG = '>> CONFIG ERROR: {0}'
FMT_H1 = '\n>> {0}...'
FMT_H2 = '{0}'


def get_mlag_peers():
    mlagpeerRslt = json.loads(clicmd('debug cfgmgr show next vsm.mLagPeer', True))
    mlag_peer = []
    dup = False
    for peerRow in mlagpeerRslt['data']:
        for peer in mlag_peer:
            if peer['peerName'] == peerRow['peerName']:
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
        port_data.append({'VlanName': str(vlanRow['vlanName']), 'VlanId': str(vlanRow['vlanId']), 'tag' : str(vlanRow['tagStatus'])})
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


def port_active(port):
    port_status = json.loads(clicmd('debug cfgmgr show one vlan.show_ports_info formatted portList={0}'.format(port), capture=True))
    port_status = port_status['data'][0]['linkState']
    if port_status == '1':
        return True
    else:
        return False


def legacy_mlag_check():
    # Find which vlan is the ISC vlan
    cli_output = clicmd('debug vsm show peer | inc "vrId      :"', True).split()
    isc_vlan = cli_output[5]
    peer_name = clicmd('debug vsm show peer | include "Name      : "', True).split()

    #Checkes to see if MLAG peer is not configured
    if cli_output[5] == 'Unknown':
        print ("Tool does not support this configuration")
        exit()
    else:
        print
        print ("****mlag_config_check.py running on MLAG Peer {0}****").format(peer_name[6])
        print
        # Check the number of ports added to the ISC vlan, and get the port number of the ISC link
        cli_output = clicmd('show vlan ' + isc_vlan, True).split()
        index = cli_output.index('Ports:')
        index = index + 1 # +1, since we found the item before the number of ports
        num_ports = cli_output[index]
        # Remove the trailing period from that output
        if num_ports.endswith('.'):
            num_ports = int(num_ports[:-1])
        #Check the number of ports added to the ISC vlan
        if num_ports > 1:
            print 'Multiple ports are added to the ISC vlan (' + isc_vlan + '). Please correct.'
            return
        elif num_ports == 0:
            print 'No ports are added to the ISC vlan (' + isc_vlan + '). Please correct.'
            return
        # At this point, we can assume that there is one port added to the ISC vlan,
        # and continue checking the MLAG configuration.
        # Determine what the port number of the ISC is
        if 'Tag:' in cli_output:
            index = cli_output.index('Tag:')
            index = index + 1
            isc_port = cli_output[index]
        elif 'Untag:' in cli_output:
            index = cli_output.index('Untag:')
            index = index + 1
            isc_port = cli_output[index]
        else:
            print FMT_ERROR.format('An error occurred. Unable to determine ISC port')
            return
        # Remove the flags around the port number
        if isc_port.endswith('g'):
            isc_port = isc_port[:-1]
        elif isc_port.endswith('G'):
            print ('The ISC port is also configured as an MLAG port. Please correct.')
            return
        if isc_port.startswith('*'):
            isc_port = isc_port[1:]
        elif isc_port.startswith('!'):
            isc_port = isc_port[1:]
            print 'The ISC port (' + isc_port + ') is disabled. Please correct.'
        # Create a list of the vlans that exist on the ISC port
        cli_output = clicmd('show port ' + isc_port + ' info detail', True).split()
        vlan_on_next_iteration = False
        isc_port_vlans = list()
        for i in cli_output:
            if vlan_on_next_iteration:
                #remove a trailing comma, if present
                if i.endswith(','):
                    vlan = i[:-1]
                else:
                    vlan = i
                isc_port_vlans.append(vlan)
            if i == 'Name:':
                vlan_on_next_iteration = True
            else :
                vlan_on_next_iteration = False
        # Now, isc_port_vlans contains all the vlans on the ISC port.
        # Now we can iterate through MLAG ports, and check if the vlans on them are
        # on the ISC port. If not, an error will be written to the CLI.
        cli_output = clicmd('show config vsm', True)
        lines = cli_output.split('\n')
        #remove an empty string that breaks the for loop below
        lines = lines[:-1]
        #create an empty list to be used in the loop
        mlag_ports = list()
        for l in lines:
            line = l.split()
            if line[0] == 'enable':
                mlag_ports.append(line[3])
        for p in mlag_ports:
            cli_output = clicmd('show port ' + p + ' info detail', True).split()
            vlan_on_next_iteration = False
            port_vlans = list()
            for i in cli_output:
                if vlan_on_next_iteration:
                    #remove a trailing comma, if present
                    if i.endswith(','):
                        vlan = i[:-1]
                    else:
                        vlan = i
                    if vlan not in isc_port_vlans:
                        print 'Vlan ' + vlan + ' is not added to the ISC port (' + isc_port + '), and is found on MLAG port ' + p + '. Please correct.'
                if i == 'Name:':
                    vlan_on_next_iteration = True
                else :
                    vlan_on_next_iteration = False
        ## Check local and remote checksums to determine if FDB and VLANs match
        for count in range(0,3):
            checksums = clicmd('debug fdb show globals | include LclCkhsum:', True)
            checksums = checksums.split()
            local = checksums[2]
            remote = checksums[4]
            #print local
            #print remote
            if local == remote:
                print ('Local and remote FDB checksums match.')
                break
        if local != remote:
            print 'Local and remote FDB checksums do not match. Please check config on the other MLAG peer.'
            print clicmd('debug fdb show globals', True)


def yes_no_input(request):
    input = raw_input(request)
    if input in ('y','Y'):
        return True
    elif input in ('n','N',''):
        return False
    print FMT_ERROR.format('Invalid input.  Please enter \'y\' or \'n\'')
    yes_no_input(request)


def main():
    print FMT_H1.format("Checking MLAG Configuration and Status")
    # Check to see if MLAG is configured
    vsm_config = len(clicmd('show configuration vsm', True).splitlines())
    if vsm_config <= 3:
        print FMT_ERROR.format('MLAG Not Configured')
        exit()

    # Check software version, 15.6 must run legacy MLAG check script
    pimage = True
    sh_switch = clicmd('show switch', True)
    ver = ''
    if 'Image Selected:   secondary' in sh_switch:
        pimage = False
    sh_switch = sh_switch.splitlines()
    for line in sh_switch:
        if (pimage and ('Primary ver:' in line)) or (not pimage and ('Secondary ver:' in line)):
            ver = line.split(':')
            ver = ver[1].strip()
    if ver == '':
        print FMT_ERROR.format('Problem detecting software version')
        exit()
    elif ver.startswith('15.6'):
        print('Switch running EXOS 15.6, executing legacy script, multi-peer not supported.')
        legacy_mlag_check()
    else:
        peer_info = get_mlag_peers()
        mports = get_mlag_ports()

        sharing = json.loads(clicmd('debug cfgmgr show next vlan.ls_ports_show', capture=True))
        sharing = sharing['data']
        lag_ports = []
        for port in sharing:
            lag_ports.append(port['port'])

        for index, peer in enumerate(peer_info):
            perror = False
            # Get Peer Name
            pname = peer['peerName']
            print FMT_H1.format('Checking MLAG Peer "{0}"'.format(pname))
            # Get ISC VLAN
            isc_vlan = peer['vlan']
            isc_port = ''
            # Check to see if MLAG peer is not configured
            if isc_vlan == 'None':
                print FMT_H2.format(FMT_CFG.format('Peer "{0}" is not properly configured, ISC VLAN configuration not found'.format(pname)))
                perror = True
                continue
            # Check the number of ports added to the ISC vlan, and get the port number of the ISC link
            port_check = get_vlan_ports(isc_vlan)
            plist = ['-', ',']
            # Catch 1 tagged and 1 untagged port added to ISC
            if port_check['untagged'] != 'None' and port_check['tagged'] != 'None':
                print FMT_H2.format(FMT_CFG.format('ISC vlan "{0}" for peer {1} has more than one port added, please resolve'.format(isc_vlan, pname)))
                perror = True
                continue
            # Check if NO ports are added to ISC
            elif port_check['untagged'] == 'None' and port_check['tagged'] == 'None':
                print FMT_H2.format(FMT_CFG.format('No port added to ISC vlan "{0}" for peer {1}, please resolve'.format(isc_vlan, pname)))
                perror = True
                continue
            # Check if untagged or tagged fields contain port list, meaning multiple ports are added
            elif any(s in port_check['untagged'] for s in plist) or any(s in port_check['tagged'] for s in plist):
                print FMT_H2.format(FMT_CFG.format('ISC vlan "{0}" for peer {1} has more than one port added, please resolve'.format(isc_vlan, pname)))
                perror = True
                continue
            elif port_check['untagged'] == 'None':
                isc_port = port_check['tagged']
            elif port_check['tagged'] == 'None':
                isc_port = port_check['untagged']
            if isc_port == '':
                FMT_ERROR.format('Problem detecting ISC port for peer {0}'.format(pname))
                perror = True
                continue

            # Create a list of the vlans that exist on the ISC port
            isc_vlans = get_port_vlan_list(isc_port)
            # Now we can iterate through MLAG ports, and check if the vlans on them are
            # on the ISC port. If not, an error will be written to the CLI.
            missing_vlans = []
            mlag_ports = []
            mport_vids = []

            # Create a list 'mlag_ports' that contains all MLAG ports for the peer
            for port in mports:
                if port['peerName'] == pname:
                    mlag_ports.append(port['port'])
            # Create a list of all VLANs on all MLAG ports for the peer
            for port in mlag_ports:
                vlan_list = get_port_vlan_list(port)
                for vid in vlan_list:
                    if vid not in mport_vids:
                        mport_vids.append(vid)

            # Check ISC and MLAG Port status
            # Check ISC
            if isc_port in lag_ports:
                for port in sharing:
                    if port['loadShareMaster'] == isc_port:
                        if port['linkState'] == '0':
                            print FMT_CFG.format(
                                'Port {0}, a LAG member of the ISC for peer {1}, is down.  Please resolve.'.format(
                                    port['port'], pname))
                            perror = True
                        elif port['agg_membership'] == '0' and port['linkState'] == '1':
                            print FMT_CFG.format(
                                'Port {0}, a LAG member of the ISC for peer {1} is not added to the aggregator.  Please resolve.'.format(
                                    port['port'], pname))
                            perror = True
            else:
                print FMT_CFG.format(
                    'ISC for {0} is not a LAG.  It is recommended that all ISC connections use link aggregation'.format(
                        pname))
                perror = True
                if not port_active(isc_port):
                    print FMT_CFG.format(
                        'ISC port {0} for Peer {1} not active. Please resolve.'.format(isc_port, pname))
                    perror = True
            # Check MLAG Ports
            for port in mlag_ports:
                if port in lag_ports:
                    for lag_port in sharing:
                        if lag_port['loadShareMaster'] == port:
                            if lag_port['linkState'] == '0':
                                print FMT_CFG.format(
                                    'MLAG port {0} for peer {1} is down.  Please resolve.'.format(
                                        lag_port['port'], pname))
                                perror = True
                            elif lag_port['agg_membership'] == '0' and lag_port['linkState'] == '1':
                                print FMT_CFG.format(
                                    'MLAG port {0} for peer {1} is not added to the aggregator.  Please resolve.'.format(
                                        lag_port['port'], pname))
                                perror = True
                else:
                    if not port_active(port):
                        print FMT_CFG.format(
                            'MLAG Port {0} for Peer {1} is not active. Please resolve.'.format(port, pname))
                        perror = True

            # Check to see if MLAG port VLANs are missing from ISC and add the missing vlans to a list
            for vid in mport_vids:
                if vid not in isc_vlans:
                    missing_vlans.append(vid)
                    print FMT_H2.format(FMT_CFG.format('VLAN {0} is found on an MLAG port but not added to ISC port {1}'.format
                                         (vid, isc_port)))
                    perror = True
            # If vlans are missing, ask the user if they woud like to resolve
            if missing_vlans != [] and yes_no_input(">> Would you like to add the missing vlans to the ISC? (y/n)"):
                for vlan in missing_vlans:
                    print('Adding missing VLANS..')
                    clicmd('configure vlan {0} add port {1} tagged'.format(vlan, isc_port))
            ## Check local and remote checksums to determine if FDB and VLANs match
            for count in range(0, 3):
                checksums = clicmd('debug fdb show globals | include LclCkhsum:', True)
                checksums = checksums.split()
                if index == 0:
                    local = checksums[2]
                    remote = checksums[4]
                elif index == 1:
                    local = checksums[7]
                    remote = checksums[9]
                else:
                    print FMT_ERROR.format('Checksum check failed.')
                    exit()
                    # print local
                    # print remote
                if local == remote:
                    # print FMT_H2.format('Local and remote FDB checksums match.')
                    break
                if local != remote:
                    print FMT_CFG.format('Local and remote FDB checksums do not match. Please check config on the other MLAG peer.')
                    print clicmd('debug fdb show globals', True)
                    perror = True


            if not perror:
                print FMT_H2.format('No problems found on peer "{0}"'.format(pname))

    print '\n>> MLAG config check completed.\n'

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass
