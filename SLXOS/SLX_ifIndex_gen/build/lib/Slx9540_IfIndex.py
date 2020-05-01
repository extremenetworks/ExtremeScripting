#!/usr/bin/python3
from SLX_BitMap import BitMap
from SLX_IntfTypeMap import IntfTypeMap
from SLX_TunnelTypeMap import TunnelTypeMap
from SLXRSpeedMap import SLXRSpeedMap
from SLXSSpeedMap import SLXSSpeedMap
from SLX_PortData import PortData
from SLX_PortMapping import PortMapping
from IfIndex import IfIndex
from SLX_IfIndex_Core import Slx_IfIndex_Core


class Slx9540_IfIndex(Slx_IfIndex_Core):
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
        self.speed_over_ride = True
        self.valid_linecards = []
        self.dev_family = 'slx'
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
        self.init_mapping()
        # validate and parse the interface and data given by the user.
        self.expand_interface()
        if int(self.sub_port) != 0:
            self.speed_over_ride = False
        self.map_vars_to_bits()
        return

    def init_mapping(self):
        self.mapping = PortMapping()
        self.mapping.add_interface('1', chip_port=1, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('2', chip_port=2, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('3', chip_port=3, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('4', chip_port=4, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('5', chip_port=5, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('6', chip_port=6, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('7', chip_port=7, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('8', chip_port=8, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('9', chip_port=9, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('10', chip_port=10, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('11', chip_port=11, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('12', chip_port=12, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('13', chip_port=13, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('14', chip_port=14, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('15', chip_port=15, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('16', chip_port=16, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('17', chip_port=17, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('18', chip_port=18, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('19', chip_port=19, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('20', chip_port=20, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('21', chip_port=21, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('22', chip_port=22, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('23', chip_port=23, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('24', chip_port=24, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('25', chip_port=25, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('26', chip_port=26, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('27', chip_port=27, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('28', chip_port=28, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('29', chip_port=29, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('30', chip_port=30, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('31', chip_port=31, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('32', chip_port=32, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('33', chip_port=33, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('34', chip_port=34, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('35', chip_port=35, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('36', chip_port=36, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('37', chip_port=37, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('38', chip_port=38, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('39', chip_port=39, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('40', chip_port=40, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('41', chip_port=41, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('42', chip_port=42, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('43', chip_port=43, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('44', chip_port=44, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('45', chip_port=45, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('46', chip_port=46, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('47', chip_port=47, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('48', chip_port=48, chip_num=0,
                                   valid_speeds=['10g'], breakout=False)
        self.mapping.add_interface('49', chip_port=49, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('50', chip_port=53, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('51', chip_port=57, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('52', chip_port=61, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('53', chip_port=65, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('54', chip_port=69, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])


def main():
    return


if __name__ == '__main__':
    main()
