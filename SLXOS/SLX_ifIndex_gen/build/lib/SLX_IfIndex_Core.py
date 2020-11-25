#!/usr/bin/python3
import re
from SLX_BitMap import BitMap
from SLX_IntfTypeMap import IntfTypeMap
from SLX_TunnelTypeMap import TunnelTypeMap
from SLXRSpeedMap import SLXRSpeedMap
from SLXSSpeedMap import SLXSSpeedMap
from SLX_PortData import PortData
from SLX_PortMapping import PortMapping
from IfIndex import IfIndex


class Slx_IfIndex_Core(object):
    '''Slx_IfIndex_Core.
    Provides common functionality for all SLX device type, and is an inherited
    class for the device classes.
    Methods:
        common_data - Sets up the common data types needed for the device.

        validate_kwargs - Validates the arguments passed by the user, and maps
                          the needed ones into a data structure.

        expand_interface - Converts the human readable interface into the
                           various peices of information needed, and validates
                           them.

        bit_mapper - Maps an string or integer value into a binary string of
                     the requested length

        map_vars_to_bits - Maps all the information into the binary string
                           format, and stores it as an IfIndex obect in
                           self.if_index for later use.
    '''
    def common_data(self):
        self.valid_interface_types = ['ethernet', 'e', 'ethe',
                                      'lo', 'lb', 'loopback',
                                      'm', 'mgmt', 'management',
                                      'po', 'port-channel'
                                      'tun', 'tunnel',
                                      've']
        self.intf_type_map = IntfTypeMap()
        self.tunnel_type_map = TunnelTypeMap()
        self.valid_tunnel_types = ['vxlan', 'gre', 'nvgre', 'mpls']
        self.required_keys = ['interface']
        self.optional_keys = ['linecard', 'speed', 'tunnel_type']
        self.linecard = ''
        self.speed = ''
        self.tunnel_type = ''
        return

    def validate_kwargs(self):
        '''sets up the self.linecard, self.speed, self.tunnel_type
        and self.bridge_id if the correct keys are present in the kwards.'''
        data_key_set = set(self.data.keys())
        req_keys_checks = data_key_set.intersection(self.required_keys)
        if not list(req_keys_checks):
            raise ValueError('A required value is missing '
                             + '{}'.format(list(req_keys_checks)))
        optional_key_checks = data_key_set.intersection(self.optional_keys)
        if optional_key_checks:
            for key in optional_key_checks:
                if key:
                    if key == 'linecard':
                        self.linecard = self.data[key]
                    if key == 'speed':
                        self.speed = self.data[key]
                    if key == 'tunnel_type':
                        self.tunnel_type = self.data[key]
        return

    def expand_interface(self):
        '''set up self.type, self.slot, self.port, and self.sub_port.'''
        type = self.data['interface'].strip().split()[0].lower()
        intf_id = self.data['interface'].strip().split()[1].lower()
        if type not in self.valid_interface_types:
            raise ValueError('Interface is not a supported type of interface.')
        self.type = type
        self.slot = '0'
        self.port = intf_id
        self.sub_port = 0
        if type in ['ethernet', 'e', 'ethe']:
            self.max_port = self.mapping.get_max_interface()
            self.valid_speeds = []
            self.slot = intf_id.split('/')[0]
            self.port = intf_id.split('/')[1]
            port_data = self.mapping.get_interface(self.port)
            if port_data:
                self.valid_speeds = port_data.valid_speeds
            if ':' in intf_id:
                self.port = intf_id.split('/')[1].split(':')[0]
                sub_port = intf_id.split('/')[1].split(':')[1]
                port_data = self.mapping.get_interface(self.port)
                if port_data:
                    self.valid_speeds = port_data.breakout_speeds
                if int(sub_port) not in range(1, 5):
                    raise ValueError('Sub-interface is out of range (1-4).')
                if not port_data.breakout:
                    raise TypeError('Interface is not able to do breakout')
                self.sub_port = sub_port
            if not self.valid_speeds:
                raise ValueError('Interface does not have a valid speed, or '
                                 + 'is an invalid interface.')
            if self.data['speed'] not in self.valid_speeds:
                raise ValueError('Interface does not '
                                 + 'support the requested speed')
            if int(self.slot) not in range(self.min_slot, self.max_slot + 1):
                raise ValueError('Interface is not on a valid slot.')
            if int(self.port) not in range(1, int(self.max_port) + 1):
                raise ValueError('Interface is outside the valid port range.')
        if type in ['mgmt', 'm']:
            if int(self.port) not in self.mgmt_intfid_value:
                raise ValueError('Management interface id is out of range '
                                 + '(0-2).')
        if type in ['ve']:
            if int(self.port) not in range(1, self.max_ve_id + 1):
                raise ValueError('Ve interface id is out of range '
                                 + '(1-{}).'.format(self.max_ve_id))
        if type in ['lo', 'lb']:
            if int(self.port) not in range(1, self.max_lo_id + 1):
                raise ValueError('Loopback interface id is out of range '
                                 + '(1-{}).'.format(self.max_lo_id))
        if type in ['tun', 'tunnel', 'tnl']:
            if int(self.port) not in range(1, 1025):
                raise ValueError('tunnel interface id is out of range '
                                 + '(1-1024).')
            if self.tunnel_type:
                if self.tunnel_type not in self.valid_tunnel_types:
                    raise ValueError('Tunnel type is not a supported type')
        if type in ['po', 'port-channel']:
            if int(self.port) not in range(1, self.max_po_id + 1):
                raise ValueError('port-channel interface id is out of range'
                                 + '(1-{}).'.format(self.max_po_id))
        return

    @staticmethod
    def bit_mapper(value, bit_count):
        return format(int(value), '0{}b'.format(int(bit_count)))

    def map_vars_to_bits(self):
        self.bit_map = ''
        if self.type in ['ethernet', 'e', 'ethe']:
            chip_num = 0
            chip_port = 0
            port_data = self.mapping.get_interface(self.port)
            if port_data:
                chip_num = port_data.chip_num
                chip_port = port_data.chip_port
            # bits: 31..26
            self.bit_map += self.intf_type_map.map('phy_bc')
            # bits: 25..21
            self.bit_map += self.bit_mapper(self.slot, 5)
            # bits: 20..13
            self.bit_map += self.bit_mapper(self.port, 8)
            # bits: 12..9
            self.bit_map += self.bit_mapper(self.sub_port, 4)
            # bits: 8..6
            if self.speed_over_ride:
                max_speed = sorted([int(re.search(r'(\d+)', x).group(1)) for
                                    x in self.valid_speeds])[-1]
                self.data['speed'] = [x for x in self.valid_speeds
                                      if str(max_speed) in x][0]
            self.bit_map += self.speed_map.map(self.data['speed'])
            self.bit_map += self.bit_mapper(chip_num, 6)  # bits: 5..0
        elif self.type in ['po', 'port-channel']:
            self.bit_map += self.intf_type_map.map('lag')  # bits: 31..26
            self.bit_map += self.bit_mapper(0, 10)  # bits: 25..16 (reserved)
            self.bit_map += self.bit_mapper(self.port, 16)  # bits: 15..0
        elif self.type in ['ve']:
            self.bit_map += self.intf_type_map.map('ve')  # bits: 31..26
            # bits: 25..18
            # bridge_id portion has an issue as the valid range
            # of bridge_ids is 1 - 4096
            self.bit_map += self.bit_mapper(0, 8)
            self.bit_map += self.bit_mapper(self.port, 18)  # bits: 17..0
        elif self.type in ['tun', 'tunnel']:
            # bits: 31..26
            self.bit_map += self.intf_type_map.map('tunnel')
            # bits: 25..22
            self.bit_map += self.tunnel_type_map.map(self.data['tunnel_type'])
            # bits: 21..16 (reserved)
            self.bit_map += self.bit_mapper(0, 6)
            # bits: 15..0
            self.bit_map += self.bit_mapper(self.port, 16)
        elif self.type in ['lo', 'lb']:
            self.bit_map += self.intf_type_map.map('lb')  # bits: 31..26
            self.bit_map += self.bit_mapper(0, 10)  # bits: 25..16 (reserved)
            self.bit_map += self.bit_mapper(self.port, 16)  # bits: 15..0
        elif self.type in ['mgmt', 'm']:
            self.bit_map += self.intf_type_map.map('mgmt')  # bits: 31..26
            self.bit_map += self.bit_mapper(0, 10)  # bits: 25..16 (reserved)
            self.bit_map += self.bit_mapper(self.port, 16)  # bits: 15..0
        else:
            raise ValueError('Invalid interface type ' + intf_type)
        self.if_index = IfIndex(self.bit_map)
        return


def main():
    return


if __name__ == '__main__':
    main()
