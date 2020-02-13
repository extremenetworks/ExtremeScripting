#!/usr/bin/python3
import re
import os
import collections
import difflib
import subprocess
import argparse
import ipaddress
import sys

#comment below line for debugging purpose.
sys.tracebacklimit=0

def render_conf_diff(buf):
    cnt = 0
    flag = False
    output = []
    lst = buf[:]
    for ele in lst[-2::-1]:
        if ele.startswith('@'):
            continue
        if not (len(ele.strip())):
            continue
        if (ele[0] == '+' or ele[0] == '-'):
            if '!' in ele:
                output.append(ele)
                continue
            if re.search('[^ ]', ele[1:]) is not None:
                cnt = re.search('[^ ]', ele[1:]).start()
                output.append(ele)
                if cnt:
                    cnt -= 1
                    flag = True
                else:
                    flag = False
        else:
            tcnt = re.search('[^ ]', ele[1:]).start()
            if tcnt == 0 and flag:
                output.append(ele)
                flag = False
            elif tcnt == cnt and flag:
                output.append(ele)
                cnt -= 1
                flag = True
            else:
                flag = False
    return '\n'.join(output[-3::-1])


class cmd_struct():
    def __init__(self, cmd=None, cmd_ctx=None, cmd_idx=None, cmd_act_idx=None):
        self.cmd = cmd
        self.cmd_ctx = cmd_ctx
        self.cmd_idx = cmd_idx
        self.cmd_act_idx = cmd_act_idx


class Chunker(object):
    """Chunker class for locating chunks of configuration."""
    def __init__(self):
        pass

    @staticmethod
    def chunker(data, key, regex=False, stop=False, stop_string='!',
                line_clean=True, no_strip=False):
        """
        Takes a Cisco/MLX/SLX router config as string or list, and returns
        a list of lists with the relvent config sections.
        """
        list_data = data
        if isinstance(data, str):
            list_data = data.split('\n')
        if line_clean:
            list_data = [x.strip() for x in list_data if x != '']
        else:
            list_data = [x for x in list_data if x != '']
        index_list = [index for index, value in enumerate(list_data)
                      if key in value]
        if regex:
            index_list = [index for index, value in enumerate(list_data)
                          if re.search(key, value)]
        if stop:
            stop_index = [index for index, value in enumerate(list_data)
                          if stop_string == value.strip()]
        chunk_list = []
        for index, master_index in enumerate(index_list):
            if master_index == index_list[-1]:
                next_master_index = len(data)-1
                next_stop_index = next_master_index
                if stop:
                    next_stop_index = [value for value in stop_index
                                       if value >= master_index][0]
            else:
                next_master_index = index_list[index + 1]
                next_stop_index = next_master_index
                if stop:
                    next_stop_index = [value for value in stop_index
                                       if value >= master_index][0]
            next_index = sorted([next_master_index, next_stop_index])[0]
            if next_index == master_index:
                if no_strip:
                    chunk_list.append([x.rstrip() for x in
                                       list_data[master_index:] if x != ''])
                else:
                    chunk_list.append([x.strip() for x in
                                       list_data[master_index:] if x != ''])
            else:
                if no_strip:
                    chunk_list.append([x.rstrip() for x in
                                       list_data[master_index: next_index]
                                       if x != ''])
                else:
                    chunk_list.append([x.strip() for x in
                                       list_data[master_index: next_index]
                                       if x != ''])
        return chunk_list


class parse_file():
    def __init__(self, peer_ip=None, peer_int=None, source_ip=None,
                 input_file=None, output_file=None, patch_file=None):
        # Validation and initialization part
        self.load_input_file(input_file)
        self.output_filename = output_file
        self.patch_filename = patch_file
        self.valid_peer_ip(peer_ip)
        self.valid_peer_int(peer_int)
        self.valid_source_ip(source_ip)
        self.check_for_new_cluster_conf()
        self.cluster_commands = []
        self.cluster_completed = False
        self.extract_cluster_info()
        self.extract_interface_info()
        self.extract_vlans_ve_info()
        self.extract_evpn_info()
        self.initialize_new_cluster_config()
        self.finalize_source_ip()
        self.generate_new_config_file()
        if self.patch_filename is not None:
            self.show_diff()

    @staticmethod
    def cstrip(x):
        return ' '.join(x.strip().split()[1:])

    def valid_peer_ip(self, p_ip=None):
        """Validates that peer_ip is a string formated IP address.
        If valid, sets peer_ip"""
        if p_ip is None:
            raise ValueError('ERROR: Peer_ip was not declared')
        if isinstance(p_ip, (list, dict, int)):
            raise TypeError('ERROR: Peer_ip is not a string')
        try:
            self.peer_ip = ipaddress.ip_address(p_ip)
        except Exception as err:
            raise err
        return

    def valid_peer_int(self, p_int=None):
        """validates that the peer interface was correctly passed.
        if valid sets peer_int. Inits new_peer_int_exists to False"""
        self.new_peer_int_exists = False
        if p_int is None:
            raise ValueError('ERROR: Peer_int was not declared')
        if isinstance(p_int, (list, dict, int)):
            raise TypeError('ERROR: Peer_int is not a string')
        pattern = re.compile(r'^([\w-]+)\s+([\d/]+)')
        match = pattern.search(p_int)
        if match:
            if (match.group(1).lower() not in
                    ['e', 'eth', 'po', 'ethernet', 'port-channel']):
                raise ValueError('ERROR peer_int is not a valid interface '
                                 + 'type.')
            if match.group(1).lower() in ['e', 'eth', 'po']:
                p_int = 'Port-channel {}'.format(match.group(2))
                if match.group(1).lower() in ['e', 'eth']:
                    p_int = 'Ethernet {}'.format(match.group(2))
            self.peer_int = p_int.lower()
        else:
            raise ValueError('ERROR peer interface is not a valid format.')
        return

    def valid_source_ip(self, s_ip=None):
        """Validates the source_ip against the peer ip and data types.
        Should be an Ip address in CIDR format, or None.
        If valid, sets source_ip"""
        if s_ip is not None:
            if len(s_ip.split('/')) != 2:
                raise ValueError('ERROR: Source ip has to be in CIDR format. '
                                 + 'Please give subnet also')
            peer = ipaddress.ip_address(self.peer_ip)
            try:
                source = ipaddress.ip_network(s_ip, False)
            except Exception as err:
                raise err
            if peer not in source:
                raise ValueError('ERROR: Source_ip and peer_ip must be in the '
                                 + 'same subnet to be reachable ')
        self.source_ip = s_ip
        return

    def check_for_new_cluster_conf(self):
        """Checks that the configuration loaded has not been upgraded to the
        new MCT configuration format."""
        for chunk in [x for x in self.chunks if x[0].startswith('interface ')
                      or x[0].startswith('cluster ')]:
            if (chunk[0].startswith('interface ')
                    and chunk[0].lower() == 'interface '
                    + self.peer_int.lower()):
                self.new_peer_int_exists = True
            if (chunk[0].startswith('cluster ') and
                    len(chunk[0].split(' ')) == 2):
                raise TypeError('ERROR: Configuration pass has already'
                                + ' been converted to the new format.')
        if self.new_peer_int_exists is False:
            raise ValueError('ERROR: The user passed a new peer interface '
                             + '{}'.format(self.peer_int)
                             + ' and it doesnt exist. Aborting the '
                             + 'conversion')
            exit()
        return

    def extract_cluster_info(self):
        """Extracs the cluster configuration from the chunks variable.
        Initializes cluster_client, old_peer, old_peer_int, and cluster_name"""
        self.cluster_client = collections.OrderedDict()
        self.old_peer = None
        self.old_peer_int = None
        self.cluster_name = None
        self.shut_clients = None
        for chunk in [x for x in self.chunks if x[0].startswith('cluster ')]:
            c_name = ' '.join(chunk[0].split(' ')[:-1])[:]
            client_chunks = Chunker.chunker(chunk, r'\s+client\s+', True,
                                            line_clean=False, no_strip=True)
            o_peer = [self.cstrip(x) for x in chunk if
                      x.strip().startswith('peer ')]
            o_peer_int = [self.cstrip(x) for x in chunk if
                          x.strip().startswith('peer-interface ')]
            shut_clients = [x.strip() for x in chunk if
                          x.strip().startswith('client-interfaces')]
            if c_name:
                self.cluster_name = c_name
            if o_peer:
                self.old_peer = o_peer[0].split()[0]
            if o_peer_int:
                self.old_peer_int = o_peer_int[0]
            if shut_clients:
                self.shut_clients = ' shutdown clients'
            if [x for x in chunk if x.strip().startswith('client-pw')
                    or x.strip().startswith('describe')]:
                t_cmds = [x+'\n' for x in chunk
                          if x.strip().startswith('client-pw')
                          or x.strip().startswith('describe')]
                self.cluster_commands = t_cmds
            for client in client_chunks:
                client_name = self.cstrip(client[0])
                client_interface = [self.cstrip(x) for x in client if
                                    x.strip().startswith('client-interface')]
                self.cluster_client[client_name] = client_interface
        return

    def extract_interface_info(self):
        """Extracts the ipv4 address and vlan membership from the interface
        chunks. Initializes int_ip and int_vlan as dictionarys"""
        self.int_ip = {}
        self.int_vlan = {}
        for chunk in [x for x in self.chunks if x[0].startswith('interface ')]:
            interface = self.cstrip(chunk[0])
            # should this be a list for interface with multi IP address
            # assigned?
            ip_address = [x.split()[-1] for x in chunk
                          if x.strip().startswith('ip address ')]
            vlans = [x.split()[-1] for x in chunk
                     if x.strip().startswith('switchport trunk '
                                             + 'allowed vlan add')]
            if ip_address:
                self.int_ip[interface] = ip_address[0]
            if vlans:
                self.int_vlan[interface] = vlans[0]
        return

    def extract_vlans_ve_info(self):
        """Extracts the vlans that have ve interfaces present in the vlan
        chunks. Initializes vlan_ve as a dictionary"""
        self.vlan_ve = {}
        for chunk in [x for x in self.chunks if re.search(r'^vlan \d+', x[0])
                      and [y for y in x if
                      y.strip().startswith('router-interface')]]:
            vlan_id = self.cstrip(chunk[0])
            ve_id = [self.cstrip(x) for x in chunk
                     if x.strip().startswith('router-interface ')][0]
            self.vlan_ve[vlan_id] = ve_id
        return

    def extract_evpn_info(self):
        """Extracts the evpn bridge-domain, and evpn vlans. Initializes
        evpn_bridge_domain and evpn_vlan."""
        self.evpn_bridge_domain = None
        self.evpn_vlan = None
        for chunk in [x for x in self.chunks if x[0].startswith('evpn ')]:
            bridge_domain = [x.split()[-1] for x in chunk if
                             x.strip().startswith('bridge-domain ')]
            vlan = [x.split()[-1] for x in chunk if
                    x.strip().startswith('vlan add ')]
            if vlan:
                self.evpn_vlan = vlan[0]
            if bridge_domain:
                self.evpn_bridge_domain = bridge_domain[0]
        return

    def initialize_new_cluster_config(self):
        """Uses the extracted configurationinforation to generate the new
        cluster configuration.
        """
        if self.evpn_vlan is not None:
            self.cluster_commands.insert(0, '')
            cmd = ' member vlan add {}\n'.format(self.evpn_vlan)
            self.cluster_commands.insert(0, cmd)
        if self.shut_clients:
            self.cluster_commands.insert(0, self.shut_clients +'\n')
        if self.evpn_bridge_domain is not None:
            cmd = (' member bridge-domain add '
                   + '{}\n'.format(self.evpn_bridge_domain))
            self.cluster_commands.insert(0, cmd)
        self.cluster_commands.insert(0, '  auto'+'\n')
        self.cluster_commands.insert(0, ' peer-keepalive'+'\n')
        self.cluster_commands.insert(0, ' peer {}\n'.format(self.peer_ip))
        self.cluster_commands.insert(0, ' peer-interface '
                                     + '{}\n'.format(self.peer_int[:]))
        if self.cluster_name is not None:
            self.cluster_commands.insert(0, self.cluster_name+'\n')
        else:
            raise RuntimeError('There are no cluster confings in the existing '
                               + 'configuration. Aborting conversion.')
        return

    def finalize_source_ip(self):
        """Uses the extracted cluster configuration to determine the source_ip
        if it was not provided by the user, and is present in
        the configuration.
        """
        if self.source_ip is None:
            if self.old_peer_int is not None:
                if self.old_peer_int in self.int_ip:
                    self.source_ip = self.int_ip[self.old_peer_int]
                else:
                    raise RuntimeError('There is no way to derive source-ip '
                                       + 'to be used as user did not pass it '
                                       + 'as input and old MCT configs dont '
                                       + 'have peer-interface configuration '
                                       + 'in cluster. Aborting the '
                                       + 'conversion.')
            else:
                raise RuntimeError('There is no way to derive source-ip to be '
                                   + 'used as user did not pass it as input '
                                   + 'and old MCT configs dont have '
                                   + 'peer-interface configuration in cluster.'
                                   + ' Aborting the conversion.')
        return

    def generate_new_config_file(self):
        skipIndex = '0'
        parent_interface_cmd = None
        cluster_cmd_index = [x for x in self.idx_file.keys()
                             if self.idx_file[x].cmd.startswith('cluster ')][0]
        bgp_cmd_index = [x for x in self.idx_file.keys()
                         if self.idx_file[x].cmd.startswith('router bgp')]
        if not bgp_cmd_index == []:
            bgp_cmd_index_evpn = [x for x in self.idx_file.keys()
                                  if self.idx_file[x].cmd.startswith(
                                  ' address-family l2vpn evpn')
                                  and x.startswith(bgp_cmd_index[0])]
        else:
            bgp_cmd_index_evpn = []
        try:
            with open(self.output_filename, 'w') as output:
                for i_index in self.idx_file:
                    if (parent_interface_cmd is not None
                            and len(i_index.split('.')) == 1):
                        parent_interface_cmd = None
                    cmd = self.idx_file[i_index].cmd
                    pre_count = count = len(i_index.split('.'))-1
                    if (i_index == cluster_cmd_index
                            or i_index.startswith(cluster_cmd_index)):
                        continue
                    if i_index.startswith(skipIndex+'.') and cmd.startswith(' switchport'):
                        continue
                    if cmd.startswith('interface '):
                        parent_interface_cmd = cmd
                        if not self.cluster_completed:
                            for item in self.cluster_commands:
                                if not item.startswith(' '):
                                    output.write("!\n")
                                output.write(item)
                            output.write('!\n')
                            self.cluster_completed = True
                        if cmd[0] != ' ':
                            output.write("!\n")
                        output.write(cmd)
                        output.write('\n')
                        if self.cstrip(cmd).lower() == self.peer_int.lower():
                            tmp_cmd = ' ip address {}\n'.format(self.source_ip)
                            output.write(tmp_cmd)
                            skipIndex = i_index
                        interface_config = self.cstrip(cmd)
                        for key in self.cluster_client:
                            if interface_config in self.cluster_client[key]:
                                value = self.cstrip(key)
                                tmp_cmd = ' cluster-client {}\n'.format(value)
                                output.write(tmp_cmd)
                    elif (not bgp_cmd_index_evpn == []
                          and i_index.startswith(bgp_cmd_index_evpn[0])):
                        if self.old_peer is not None and self.old_peer in cmd:
                            continue
                        else:
                            output.write(cmd)
                            output.write('\n')
                    elif (parent_interface_cmd is not None and
                          ((self.old_peer_int is None) or
                          (parent_interface_cmd ==
                           'interface ' + self.old_peer_int))
                          and cmd.startswith(' ip address ')
                          and cmd.split(' ')[-1] == self.source_ip):
                        continue
                    elif (parent_interface_cmd is not None
                          and cmd.startswith(' ip address ')
                          and cmd.split(' ')[-1] == self.source_ip):
                        raise RuntimeError('The source ip passed by user is '
                                           + 'configured in another interface'
                                           + ' which is other than old '
                                           + 'peer-interface.'
                                           + 'Aborting the conversion.')
                    else:
                        if cmd[0] != ' ' and int(i_index.split('.')[0]) > 1:
                            output.write('!\n')
                        output.write(cmd)
                        output.write('\n')
                output.write('!\n')
        except Exception as err:
            raise err
        return

    def show_diff(self):
        """if the patch_file is not a null string, writes the differences
        between the old configuriation and new configuration out as a diff
        file."""
        if self.patch_filename:
            try:
                with open(self.patch_filename, 'w') as patch_file:
                    run_file = [line for line in self.lines
                                if not line.strip(' ').startswith('!')]
                    with open(self.output_filename, 'r') as output_file:
                        self.out_lines = output_file.readlines()
                    mod_file = [line for line in self.out_lines
                                if not line.strip(' ').startswith('!')]
                    buf = [ele.rstrip() for ele in
                           list(difflib.unified_diff(run_file, mod_file,
                                                     n=1000))]
                    patch_file.write(render_conf_diff(buf))
            except Exception as err:
                raise err

    def load_input_file(self, file):
        """Reads in the input file and processes it to the variables
        idx_file, lines, chunks, and input_filename if the file is valid and
        can be read."""
        try:
            with open(file, 'r') as input_file:
                self.lines = input_file.readlines()
        except Exception as err:
            raise err
        self.input_filename = input_file
        self.chunks = Chunker.chunker(self.lines, r'^\w+', True,
                                      line_clean=False, no_strip=True)
        self.idx_file = collections.OrderedDict()
        index = [0]
        pre_cnt = 0
        for line_index, line in enumerate(self.lines):
            if line.strip() == '!':
                continue
            cnt = re.search('[^ ]', line).start()
            if not cnt:
                index = [index[0]+1]
            else:
                if pre_cnt < cnt:
                    index.append(0)
                else:
                    index = index[:cnt+1]
                index[-1] += 1
            pre_cnt = cnt
            idx = '.'.join(list(map(str, index)))
            self.idx_file[idx] = cmd_struct(cmd=line.strip('\n'), cmd_ctx=idx,
                                            cmd_act_idx=line_index + 1)
        return


def main():
    """python ./mct_config_convert.py -h
    usage: mct_config_convert.py [-h] --peer_ip PEER_IP --peer_int PEER_INT
                                 [--source_ip SOURCE_IP]
                                 [--input_file INPUT_FILE]
                                 [--output_file OUTPUT_FILE]
                                 [--diff_file DIFF_FILE]

    Script to convert old MCT Configs to new configs.

    optional arguments:
      -h, --help            show this help message and exit
      --peer_ip PEER_IP     Peer Ip in new MCT cluster configs.
      --peer_int PEER_INT   Peer Interface in new MCT cluster configs.
      --source_ip SOURCE_IP
                            Source IP in new MCT cluster configs.
      --input_file INPUT_FILE, -i INPUT_FILE
                            Input file to proccess. DO NOT USE THIS OPTION IF
                            EXECUTING ON THE SLX.
      --output_file OUTPUT_FILE, -o OUTPUT_FILE
                            Where the modified configuration is stored. DO NOT
                             USE THIS OPTION IF EXECUTING ON THE SLX, as the
                            default location will be used by the upgrade
                            framework for configuration replay after upgrade.
      --diff_file DIFF_FILE, -d DIFF_FILE
                            This will show the diff with the INPUT and OUTPUT
                            file. DO NOT USE THIS OPTION IF EXECUTING ON THE
                            SLX.
        """
    parser = argparse.ArgumentParser(description='Script to convert old MCT'
                                     + ' Configs to new configs.')
    parser.add_argument('--peer_ip', type=str, required=True,
                        help='Peer Ip in new MCT cluster configs.')
    parser.add_argument('--peer_int', type=str, required=True,
                        help='Peer Interface in new MCT cluster configs.'
                        + ' Format is one of the following notations:'
                        + ' po 1, Port-channel 1, e 0/1, ethe 0/1 or '
                        + ' Ethernet 0/1')
    parser.add_argument('--source_ip', type=str,
                        help='Source IP in new MCT cluster configs.')
    parser.add_argument('--input_file', '-i', type=str, action='store',
                        default='/var/config/vcs/scripts/startup-config',
                        help='Input file to proccess. DO NOT USE THIS OPTION'
                        + ' IF EXECUTING ON THE SLX.')
    parser.add_argument('--output_file', '-o', type=str, action='store',
                        default='/fabos/users/admin/scripts/'
                        + 'startup-config-new',
                        help='Where the modified configuration is stored. '
                        + 'DO NOT USE THIS OPTION IF EXECUTING ON THE SLX, '
                        + 'as the default location will be used by the '
                        + 'upgrade framework for configuration replay after '
                        + 'upgrade.')
    parser.add_argument('--diff_file', '-d', type=str, action='store',
                        default='/fabos/users/admin/scripts/unified-diff.txt',
                        help='This will show the diff with the INPUT and '
                        + 'OUTPUT file. DO NOT USE THIS OPTION IF EXECUTING '
                        + 'ON THE SLX.')

    args = parser.parse_args()
    try:
        parse_file(args.peer_ip, args.peer_int, args.source_ip,
                   args.input_file, args.output_file, args.diff_file)
    except Exception as err:
        print(err)
        exit(1)
    return


if __name__ == '__main__':
    main()
