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
from SLX_IfIndex_Core import Slx_IfIndex_Core


class Slx9150_IfIndex(Slx_IfIndex_Core):
    '''Device specific classes validate against the device specific
    information.'''
    def __init__(self, interface, linecard='', speed='',
                 tunnel_type='', *args, **kwargs):
        self.data = kwargs
        if not self.data:
            self.data['interface'] = interface
            self.data['linecard'] = linecard
            self.data['speed'] = speed
            self.data['tunnel_type'] = tunnel_type
        self.common_data()
        self.valid_linecards = ['48Y', '48XT']
        self.dev_family = 'slx'
        self.speed_over_ride = True
        self.max_slot = 0
        self.min_slot = 0
        self.max_ve_id = 8192
        self.max_lo_id = 255
        self.max_po_id = 256
        self.speed_map = SLXRSpeedMap()
        # self.max_port depends on lc type
        self.mgmt_intfid_value = [0]
        self.validate_kwargs()
        # setup the self.mapping variables,
        # other devies will call self.init_mapping() here
        self.validate_linecard()
        # validate and parse the interface and data given by the user.
        self.expand_interface()
        if int(self.sub_port) != 0:
            self.speed_over_ride = False
        self.map_vars_to_bits()
        return

    def init_48Y_mapping(self):
        self.mapping = PortMapping()
        for interface in range(1, 49):
            self.mapping.add_interface(str(interface), chip_port=0, chip_num=0,
                                       valid_speeds=['10g', '25g'],
                                       breakout=False)
        self.mapping.add_interface('49', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('50', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('51', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('52', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('53', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('54', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('55', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('56', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        return

    def init_48XT_mapping(self):
        self.mapping = PortMapping()
        for interface in range(1, 49):
            self.mapping.add_interface(str(interface), chip_port=0, chip_num=0,
                                       valid_speeds=['10g'],
                                       breakout=False)
        self.mapping.add_interface('49', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('50', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('51', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('52', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('53', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'],
                                   breakout=False)
        self.mapping.add_interface('54', chip_port=0, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])

        return

    def validate_linecard(self):
        if not self.linecard:
            raise ValueError('Linecard must be 48Y or 48XT')
        if self.linecard:
            if self.linecard not in self.valid_linecards:
                raise ValueError('Line card type is invalid: '
                                 + '{}'.format(self.linecard))
            self.init_48Y_mapping()
            if self.linecard == '48XT':
                self.init_48XT_mapping()
        return


def main():
    return


if __name__ == '__main__':
    main()
