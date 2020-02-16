#!/usr/bin/python3
"""."""
import sys
import re
import os
import datetime
import time
from CLI import CLI
import ipaddress


class Chunker(object):
    """
    Takes a output or config as string or list, and returns
    a list of lists with the relvent config sections.
    """
    def __init__(self):
        pass

    @staticmethod
    def chunker(data, key, regex=False, stop=False, stop_string='!'):

        list_data = data
        if isinstance(data, str):
            list_data = data.split('\n')
        list_data = [x.strip() for x in list_data]
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
                chunk_list.append(list_data[master_index:])
            else:
                chunk_list.append(list_data[master_index: next_index])
        return chunk_list


class PortStatusData(Chunker, object):
    """Displays the interface id, description, state, basic TX/RX stats,
    Rx optical power, and optic type.

    Parameters
    ----------
    type_flag : boolean
        True: Strip the interface type from the interface id.
        'e 0/1' becomes '0/1'
    tx_flag : boolean
        True: Offset the TX information column from the RX information column
    offset : integer
        The number of spaces to offset the TX information columns
    """
    def __init__(self, type_flag=False, tx_flag=False, offset=4):
        self.no_int_type_flag = type_flag
        self.offset_tx_flag = tx_flag
        self.offset_tx = offset
        self.data = {}
        self.interface_order = []
        self.cmds = {}
        self.cmds['status'] = 'show interface status'
        self.cmds['stats'] = ['show interface stats brief',
                              'show interface stats detail | '
                              + 'inc "Interface | Mbits"']
        self.cmds['media'] = 'show media | inc "Interface|RX Power .Agg.|PN"'
        self.gather_data()
        self.print()

    def gather_data(self):
        self.get_show_int_status()
        self.get_show_int_stats()
        self.get_show_media()

    def init_interface(self, id):
        self.data[id] = {}
        self.data[id]['Name'] = '--'
        self.data[id]['Link'] = ''
        self.data[id]['QSFP'] = '--'
        self.data[id]['Packets_RX'] = '0'
        self.data[id]['Packets_TX'] = '0'
        self.data[id]['Errors_RX'] = '0'
        self.data[id]['Errors_TX'] = '0'
        self.data[id]['Discards_RX'] = '0'
        self.data[id]['Discards_TX'] = '0'
        self.data[id]['CRC_RX'] = '0'
        self.data[id]['RX_Power'] = 'None'
        self.data[id]['mbits/sec_rx'] = '0'
        self.data[id]['mbits/sec_tx'] = '0'

    def get_show_int_status(self):
        chunks = self.chunker(CLI(self.cmds['status'], False).get_output(),
                              r'^Eth\s+\d+|^Po\s+\d+', regex=True)
        for chunk in chunks:
            for line in chunk:
                line_list = line.split()
                id = '{} {}'.format(line.lower()[0], line_list[1])
                self.init_interface(id)
                self.interface_order.append(id)
                self.data[id]['Link'] = line_list[2]
                name_index = 6
                if self.data[id]['Link'] == 'connected':
                    name_index = 7
                if len(line_list) - 1 >= name_index:
                    self.data[id]['Name'] = ' '.join(line_list[name_index:])

    def get_show_int_stats(self):
        chunks = self.chunker(CLI(self.cmds['stats'][0], False).get_output(),
                              r'^Eth\s+\d+|^Po\s+\d+', regex=True)
        for chunk in chunks:
            for line in chunk:
                line_list = line.split()
                id = '{} {}'.format(line.lower()[0], line_list[1])
                if id in self.data.keys():
                    self.data[id]['Packets_RX'] = line_list[2]
                    self.data[id]['Packets_TX'] = line_list[3]
                    self.data[id]['Errors_RX'] = line_list[4]
                    self.data[id]['Errors_TX'] = line_list[5]
                    self.data[id]['Discards_RX'] = line_list[6]
                    self.data[id]['Discards_TX'] = line_list[7]
                    self.data[id]['CRC_RX'] = line_list[8]
        chunks = self.chunker(CLI(self.cmds['stats'][1], False).get_output(),
                              r'^Interface', regex=True)
        for chunk in chunks:
            id = '{} {}'.format(chunk[0].split()[1].lower()[0],
                                chunk[0].split()[2])
            if id in self.data.keys():
                self.data[id]['mbits/sec_rx'] = chunk[1].split()[1]
                self.data[id]['mbits/sec_tx'] = chunk[1].split()[2]

    def get_show_media(self):
        chunks = self.chunker(CLI(self.cmds['media'], False).get_output(),
                              r'Interface', regex=True)
        for chunk in chunks:
            id = '{} {}'.format(chunk[0].split()[1].lower()[0],
                                chunk[0].split()[2])
            if id in self.data.keys():
                self.data[id]['QSFP'] = ' '.join(chunk[1].split()[3:]
                                                 ).strip('()')
                self.data[id]['RX_Power'] = chunk[2].split()[-2]

    def get_col_widths(self):
        self.widths = {}
        dummy_int = list(self.data.keys())[0]
        self.widths['int'] = max([len(int) for int in self.data.keys()])
        if self.no_int_type_flag:
            self.widths['int'] = max([len(int.strip('ep '))
                                      for int in self.data.keys()])
        for key in self.data[dummy_int].keys():
            self.widths[key] = max([len(self.data[int][key])
                                    for int in self.data.keys()])
        self.widths['Packets'] = max([self.widths['Packets_RX'],
                                     self.widths['Packets_TX'], 7])
        self.widths['Errors'] = max([self.widths['Errors_RX'],
                                    self.widths['Errors_TX'], 6])
        self.widths['Discards'] = max([self.widths['Discards_RX'],
                                      self.widths['Discards_TX'], 8])
        self.widths['tput'] = max([self.widths['mbits/sec_rx'],
                                  self.widths['mbits/sec_tx'], 17])
        self.widths['RX_Power'] = max([self.widths['RX_Power'], 8])
        self.widths['base_offset'] = (self.widths['int'] + self.widths['Name']
                                      + self.widths['Link'] + 2)
        self.widths['CRC'] = max([self.widths['CRC_RX'], 8])
        self.widths['tx_offset'] = self.widths['base_offset']
        if self.offset_tx_flag:
            self.widths['tx_offset'] += self.offset_tx

    def print(self):
        # print(self.data)
        self.get_col_widths()
        self.print_headers()
        self.print_data()

    def print_headers(self):
        print("\n" + "="*150)
        print("Int".ljust(self.widths['int']),
              "Name".ljust(self.widths['Name']),
              "Link".ljust(self.widths['Link']),
              "Packets".ljust(self.widths['Packets']),
              "Errors".ljust(self.widths['Errors']),
              "Discards".ljust(self.widths['Discards']),
              "CRC rx".ljust(self.widths['CRC']),
              "Throughput (Mbps)".ljust(self.widths['tput']),
              "RX Power".ljust(self.widths['RX_Power']),
              "QSFP")
        print("".ljust(self.widths['base_offset']),
              "RX".ljust(self.widths['Packets']),
              "RX".ljust(self.widths['Errors']),
              "RX".ljust(self.widths['Discards']),
              "".ljust(self.widths['CRC']),
              "RX".ljust(self.widths['tput']),
              "(dBm)")
        print("".ljust(self.widths['tx_offset']),
              "TX".ljust(self.widths['Packets']),
              "TX".ljust(self.widths['Errors']),
              "TX".ljust(self.widths['Discards']),
              "".ljust(self.widths['CRC']),
              "TX".ljust(self.widths['tput']))
        print("="*150)

    def print_data(self):
        for item in self.interface_order:
            interface = item
            if self.no_int_type_flag:
                interface = item.strip('ep ')
            print(interface.ljust(self.widths['int']),
                  self.data[item]['Name'].ljust(self.widths['Name']),
                  self.data[item]['Link'].ljust(self.widths['Link']),
                  self.data[item]['Packets_RX'].ljust(self.widths['Packets']),
                  self.data[item]['Errors_RX'].ljust(self.widths['Errors']),
                  self.data[item]['Discards_RX'].ljust(
                      self.widths['Discards']),
                  self.data[item]['CRC_RX'].ljust(self.widths['CRC']),
                  self.data[item]['mbits/sec_rx'].ljust(self.widths['tput']),
                  self.data[item]['RX_Power'].ljust(self.widths['RX_Power']),
                  self.data[item]['QSFP'])
            print("".ljust(self.widths['tx_offset']),
                  self.data[item]['Packets_TX'].ljust(self.widths['Packets']),
                  self.data[item]['Errors_TX'].ljust(self.widths['Errors']),
                  self.data[item]['Discards_TX'].ljust(
                      self.widths['Discards']),
                  "".ljust(self.widths['CRC']),
                  self.data[item]['mbits/sec_tx'])


def main():
    """Displays the interface id, description, state, basic TX/RX stats,
    Rx optical power, and optic type.

    Parameters
    ----------
    type_flag : boolean
        True: Strip the interface type from the interface id.
        'e 0/1' becomes '0/1'
    tx_flag : boolean
        True: Offset the TX information column from the RX information column
    offset : integer
        The number of spaces to offset the TX information columns
    """
    # data = PortStatusData()
    data = PortStatusData(False, True, 4)


if __name__ == '__main__':
    main()
