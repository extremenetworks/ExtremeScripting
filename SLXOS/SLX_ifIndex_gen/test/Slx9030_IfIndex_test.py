#!/usr/bin/python3
import unittest
import re
from BitMap import BitMap
from IntfTypeMap import IntfTypeMap
from TunnelTypeMap import TunnelTypeMap
from SLXRSpeedMap import SLXRSpeedMap
from SLXSSpeedMap import SLXSSpeedMap
from PortData import PortData
from PortMapping import PortMapping
from SLX_IfIndex_Core import Slx_IfIndex_Core
from IfIndex import IfIndex
from Slx9030_IfIndex import Slx9030_IfIndex


class TestSlx9030_IfIndex(unittest.TestCase):
    @staticmethod
    def bit_mapper(value, bit_count):
        return format(int(value), '0{}b'.format(int(bit_count)))

    def test_line_card(self):
        for test_value in ['72X10G', '72X10g', '60x40G', '36X100G', '36x100g']:
            with self.subTest(test_value):
                args = {'interface': 'e 1/1', 'speed': '10g'}
                args['linecard'] = test_value
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_portspeed_1to48(self):
        for test_value in ['1g', '10G', '25g', '40g', '50g', '100g', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/1'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_portspeed_49to54(self):
        for test_value in ['1g', '10g', '25g', '40G', '50g', '100G', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/49'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_portspeed_49to54_breakout(self):
        for test_value in ['1g', '10G', '25G', '40g', '50g', '100g', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/49:1'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_portspeed_1to48_breakout(self):
        for test_value in ['1g', '10G', '25G', '40g', '50g', '100g']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/1:1'}
                args['speed'] = test_value
                self.assertRaises(TypeError, Slx9030_IfIndex, **args)
        return

    def test_slot_garbage(self):
        garbage = [1, 9, -1, 'a']
        for test_value in garbage:
            with self.subTest(test_value):
                args = {'speed': '100g'}
                args['interface'] = 'e {}/49'.format(test_value)
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        for test_value in garbage:
            with self.subTest(test_value):
                args = {'speed': '10g'}
                args['interface'] = 'e {}/1'.format(test_value)
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_port_channel_garbage(self):
        for test_value in [0, 1025, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 'po {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_tunnel_garbage(self):
        for test_value in [0, 513, 'a', -1]:
            with self.subTest(test_value):
                args = {'tunnel_type': 'vxlan'}
                args['interface'] = 'tun {}'.format(test_value)
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_breakout_garbage(self):
        for test_value in [0, 5, 'a', -1]:
            with self.subTest(test_value):
                args = {'speed': '10g', 'linecard': '36x100G'}
                args['interface'] = 'e 1/1:{}'.format(test_value)
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_mgmt_garbage(self):
        for test_value in [1, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 'm {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_loopback_garbage(self):
        for test_value in [0, 257, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 'lo {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_ve_garbage(self):
        for test_value in [0, 8193, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 've {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9030_IfIndex, **args)
        return

    def test_mgmt_output(self):
        for test_value, test_result in [[0, 805306368]]:
            with self.subTest(test_value):
                args = {'interface': 'm {}'.format(test_value)}
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_port_channel_output(self):
        for test_value in range(1, 256):
            with self.subTest(test_value):
                test_result = 671088640 + test_value
                args = {'interface': 'po {}'.format(test_value)}
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_tunnel_output(self):
        max_tunnel_id = 1024
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'vxlan')):
                test_result = 2080374784 + test_value
                args = {'tunnel_type': 'vxlan'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'gre')):
                test_result = 2084569088 + test_value
                args = {'tunnel_type': 'gre'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'nvgre')):
                test_result = 2088763392 + test_value
                args = {'tunnel_type': 'nvgre'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'mpls')):
                test_result = 2092957696 + test_value
                args = {'tunnel_type': 'mpls'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_ve_output(self):
        max_ve_id = 4096
        for test_value in range(1, max_ve_id + 1):
            with self.subTest((test_value)):
                test_result = 1207959552 + test_value
                args = {'interface': 've {}'.format(test_value)}
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_loopback_output(self):
        for test_value in range(1, 256):
            with self.subTest(test_value):
                test_result = 1476395008 + test_value
                args = {'interface': 'lo {}'.format(test_value)}
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_49to54_port_output(self):
        args = {'speed': '100g', 'interface': 'e 0/49'}
        dummy = Slx9030_IfIndex(**args)
        intf_string = '000011'
        sub_port = self.bit_mapper(0, 4)
        speed_string = dummy.speed_map.map('100g')
        interfaces = [x.physical for x in dummy.mapping.interfaces
                      if '100g' in x.valid_speeds]
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for interface in interfaces:
            test_value = 'e {}/{}'.format(slot, interface)
            port_data = dummy.mapping.get_interface(interface)
            bit_map = (intf_string + slot_string
                       + self.bit_mapper(interface, 8) + sub_port
                       + speed_string
                       + self.bit_mapper(port_data.chip_num, 6))
            test_result = IfIndex(bit_map)
            with self.subTest(test_value):
                args = {'speed': '100g'}
                args['interface'] = '{}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal,
                                 test_result.Decimal)
        speed_string = dummy.speed_map.map('40g')
        interfaces = [x.physical for x in dummy.mapping.interfaces
                      if '40g' in x.valid_speeds]
        slot_string = self.bit_mapper(slot, 5)
        for interface in interfaces:
            test_value = 'e {}/{}'.format(slot, interface)
            port_data = dummy.mapping.get_interface(interface)
            bit_map = (intf_string + slot_string
                       + self.bit_mapper(interface, 8) + sub_port
                       + speed_string
                       + self.bit_mapper(port_data.chip_num, 6))
            test_result = IfIndex(bit_map)
            with self.subTest(test_value):
                args = {'speed': '40g'}
                args['interface'] = '{}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal,
                                 test_result.Decimal)
        return

    def test_49to54_breakout_port_output(self):
        args = {'speed': '100g', 'interface': 'e 0/49'}
        dummy = Slx9030_IfIndex(**args)
        intf_string = '000011'
        speed_string = dummy.speed_map.map('25g')
        interfaces = [x.physical for x in dummy.mapping.interfaces
                      if x.breakout]
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for interface in interfaces:
            for breakout in range(1, 5):
                sub_port = self.bit_mapper(breakout, 4)
                test_value = 'e {}/{}:{}'.format(slot, interface, breakout)
                port_data = dummy.mapping.get_interface(interface)
                bit_map = (intf_string + slot_string
                           + self.bit_mapper(interface, 8) + sub_port
                           + speed_string
                           + self.bit_mapper(port_data.chip_num, 6))
                test_result = IfIndex(bit_map)
                with self.subTest(test_value):
                    args = {'speed': '25g'}
                    args['interface'] = '{}'.format(test_value)
                    result = Slx9030_IfIndex(**args)
                    self.assertEqual(result.if_index.Decimal,
                                     test_result.Decimal)
        speed_string = dummy.speed_map.map('10g')
        interfaces = [x.physical for x in dummy.mapping.interfaces
                      if x.breakout]
        slot_string = self.bit_mapper(slot, 5)
        for interface in interfaces:
            for breakout in range(1, 5):
                sub_port = self.bit_mapper(breakout, 4)
                test_value = 'e {}/{}:{}'.format(slot, interface, breakout)
                port_data = dummy.mapping.get_interface(interface)
                bit_map = (intf_string + slot_string
                           + self.bit_mapper(interface, 8) + sub_port
                           + speed_string
                           + self.bit_mapper(port_data.chip_num, 6))
                test_result = IfIndex(bit_map)
                with self.subTest(test_value):
                    args = {'speed': '10g'}
                    args['interface'] = '{}'.format(test_value)
                    result = Slx9030_IfIndex(**args)
                    self.assertEqual(result.if_index.Decimal,
                                     test_result.Decimal)
        return

    def test_1to48_port_output(self):
        args = {'speed': '10g', 'interface': 'e 0/1'}
        dummy = Slx9030_IfIndex(**args)
        intf_string = '000011'
        sub_port = self.bit_mapper(0, 4)
        speed_string = dummy.speed_map.map('10g')
        interfaces = [x.physical for x in dummy.mapping.interfaces
                      if not x.breakout]
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for interface in interfaces:
            test_value = 'e {}/{}'.format(slot, interface)
            port_data = dummy.mapping.get_interface(interface)
            bit_map = (intf_string + slot_string
                       + self.bit_mapper(interface, 8) + sub_port
                       + speed_string
                       + self.bit_mapper(port_data.chip_num, 6))
            test_result = IfIndex(bit_map)
            with self.subTest(test_value):
                args = {'speed': '10g'}
                args['interface'] = '{}'.format(test_value)
                result = Slx9030_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal,
                                 test_result.Decimal)
        return
