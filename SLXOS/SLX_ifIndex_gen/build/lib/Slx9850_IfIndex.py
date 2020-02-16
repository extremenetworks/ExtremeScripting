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


class Slx9850_IfIndex(Slx_IfIndex_Core):
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
        self.speed_over_ride = False
        self.valid_linecards = ['72x10G', '36x100G']
        self.dev_family = 'slx'
        self.max_slot = 8
        self.min_slot = 1
        self.max_ve_id = 4096
        self.max_lo_id = 255
        self.max_po_id = 512
        self.speed_map = SLXRSpeedMap()
        # self.max_port depends on lc type
        self.mgmt_intfid_value = [1, 2]
        self.validate_kwargs()
        # setup the self.mapping variables,
        # other devies will call self.init_mapping() here
        self.validate_linecard()
        # validate and parse the interface and data given by the user.
        self.expand_interface()
        self.map_vars_to_bits()
        return

    def init_72x10_mapping(self):
        self.mapping = PortMapping()
        self.mapping.add_interface('1', chip_port=1, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('2', chip_port=2, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('3', chip_port=21, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('4', chip_port=22, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('5', chip_port=3, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('6', chip_port=4, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('7', chip_port=5, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('8', chip_port=6, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('9', chip_port=23, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('10', chip_port=24, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('11', chip_port=7, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('12', chip_port=8, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('13', chip_port=1, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('14', chip_port=2, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('15', chip_port=21, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('16', chip_port=22, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('17', chip_port=3, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('18', chip_port=4, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('19', chip_port=5, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('20', chip_port=6, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('21', chip_port=23, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('22', chip_port=24, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('23', chip_port=7, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('24', chip_port=8, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('25', chip_port=25, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('26', chip_port=26, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('27', chip_port=27, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('28', chip_port=28, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('29', chip_port=9, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('30', chip_port=10, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('31', chip_port=11, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('32', chip_port=12, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('33', chip_port=29, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('34', chip_port=30, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('35', chip_port=13, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('36', chip_port=14, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('37', chip_port=25, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('38', chip_port=26, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('39', chip_port=27, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('40', chip_port=28, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('41', chip_port=9, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('42', chip_port=10, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('43', chip_port=11, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('44', chip_port=12, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('45', chip_port=29, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('46', chip_port=30, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('47', chip_port=13, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('48', chip_port=14, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('49', chip_port=31, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('50', chip_port=32, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('51', chip_port=33, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('52', chip_port=34, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('53', chip_port=15, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('54', chip_port=16, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('55', chip_port=17, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('56', chip_port=18, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('57', chip_port=35, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('58', chip_port=36, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('59', chip_port=19, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('60', chip_port=20, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('61', chip_port=31, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('62', chip_port=32, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('63', chip_port=33, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('64', chip_port=34, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('65', chip_port=15, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('66', chip_port=16, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('67', chip_port=17, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('68', chip_port=18, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('69', chip_port=35, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('70', chip_port=36, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('71', chip_port=19, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('72', chip_port=20, chip_num=1,
                                   breakout=False)
        self.mapping.add_interface('125', chip_port=125, chip_num=0,
                                   breakout=False)
        self.mapping.add_interface('126', chip_port=126, chip_num=1,
                                   breakout=False)
        return

    def init_36x100_mapping(self):
        '''
        <slot>/1           <slot>/1  ,2  ,3  ,4  ,5  ,6  ,7  ,26 ,27 ,28
        <slot>/2           <slot>/8  ,9  ,10 ,11 ,12 ,13 ,29 ,30 ,31 ,32
        <slot>/3           <slot>/15 ,16 ,17 ,18 ,19 ,20 ,14 ,33 ,34 ,35
        <slot>/4           <slot>/41 ,42 ,43 ,44 ,45 ,46 ,21 ,22 ,23 ,24
        <slot>/5           <slot>/48 ,49 ,50 ,51 ,52 ,53 ,25 ,36 ,47 ,54
        <slot>/6           <slot>/55 ,56 ,57 ,58 ,59 ,60 ,37 ,38 ,39 ,40
        * Only the first six ports in each group are 100g capable ports
        '''
        self.mapping = PortMapping()
        self.mapping.add_interface('1', chip_port=1, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('2', chip_port=5, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('3', chip_port=9, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('4', chip_port=21, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('5', chip_port=25, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('6', chip_port=29, chip_num=0,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('7', chip_port=13, chip_num=0,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('8', chip_port=1, chip_num=1,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('9', chip_port=5, chip_num=1,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('10', chip_port=9, chip_num=1,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('11', chip_port=21, chip_num=1,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('12', chip_port=25, chip_num=1,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('13', chip_port=29, chip_num=1,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('14', chip_port=1, chip_num=2,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('15', chip_port=5, chip_num=2,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('16', chip_port=9, chip_num=2,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('17', chip_port=13, chip_num=2,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('18', chip_port=21, chip_num=2,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('19', chip_port=25, chip_num=2,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('20', chip_port=29, chip_num=2,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('21', chip_port=1, chip_num=3,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('22', chip_port=5, chip_num=3,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('23', chip_port=21, chip_num=3,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('24', chip_port=25, chip_num=3,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('25', chip_port=1, chip_num=4,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('26', chip_port=17, chip_num=0,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('27', chip_port=33, chip_num=0,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('28', chip_port=37, chip_num=0,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('29', chip_port=13, chip_num=1,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('30', chip_port=17, chip_num=1,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('31', chip_port=33, chip_num=1,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('32', chip_port=37, chip_num=1,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('33', chip_port=17, chip_num=2,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('34', chip_port=33, chip_num=2,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('35', chip_port=37, chip_num=2,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('36', chip_port=5, chip_num=4,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('37', chip_port=1, chip_num=5,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('38', chip_port=5, chip_num=5,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('39', chip_port=21, chip_num=5,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('40', chip_port=25, chip_num=5,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('41', chip_port=9, chip_num=3,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('42', chip_port=13, chip_num=3,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('43', chip_port=17, chip_num=3,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('44', chip_port=29, chip_num=3,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('45', chip_port=33, chip_num=3,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('46', chip_port=37, chip_num=3,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('47', chip_port=21, chip_num=4,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('48', chip_port=9, chip_num=4,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('49', chip_port=13, chip_num=4,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('50', chip_port=17, chip_num=4,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('51', chip_port=25, chip_num=4,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('52', chip_port=29, chip_num=4,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('53', chip_port=33, chip_num=4,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('54', chip_port=37, chip_num=4,
                                   valid_speeds=['40g'], breakout=True,
                                   breakout_speeds=['10g'])
        self.mapping.add_interface('55', chip_port=9, chip_num=5,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('56', chip_port=13, chip_num=5,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('57', chip_port=17, chip_num=5,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('58', chip_port=29, chip_num=5,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('59', chip_port=33, chip_num=5,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('60', chip_port=37, chip_num=5,
                                   valid_speeds=['40g', '100g'], breakout=True,
                                   breakout_speeds=['10g', '25g'])
        self.mapping.add_interface('125', chip_port=125, chip_num=3,
                                   valid_speeds=['40g', '100g'])
        self.mapping.add_interface('126', chip_port=126, chip_num=4,
                                   valid_speeds=['40g', '100g'])
        return

    def validate_linecard(self):
        if self.linecard:
            if self.linecard not in self.valid_linecards:
                raise ValueError('Line card type is invalid: '
                                 + '{}'.format(self.linecard))
            self.init_72x10_mapping()
            if self.linecard == '36x100G':
                self.init_36x100_mapping()
        return


def main():
    return


if __name__ == '__main__':
    main()
