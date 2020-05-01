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
from Slx9150_IfIndex import Slx9150_IfIndex


class TestSlx9150_IfIndex(unittest.TestCase):
    @staticmethod
    def bit_mapper(value, bit_count):
        return format(int(value), '0{}b'.format(int(bit_count)))

    def test_line_card(self):
        test_values = ['72X10G', '60x40G', '36X100G', '48y', '48xt']
        for test_value in test_values:
            with self.subTest(test_value):
                args = {'interface': 'e 0/1', 'speed': '10g'}
                args['linecard'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_portspeed_48Y(self):
        for test_value in ['1g', '10G', '25G', '40g', '50g', '100g', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/1', 'linecard': '48Y'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        for test_value in ['1g', '10g', '25g', '40G', '50g', '100G', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/50', 'linecard': '48Y'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_portspeed_48XT(self):
        for test_value in ['1g', '10G', '25g', '40G', '50g', '100G', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/1', 'linecard': '48XT'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        for test_value in ['1g', '10g', '25g', '40G', '50g', '100G', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/50', 'linecard': '48Y'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_portspeed_48Y_breakout(self):
        for test_value in ['1g', '10G', '25G', '40g', '50g', '100g', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/49:1', 'linecard': '48Y'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
                args = {'interface': 'e 0/56:1', 'linecard': '48Y'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_portspeed_48XT_breakout(self):
        for test_value in ['1g', '10G', '25G', '40g', '50g', '100g', '']:
            with self.subTest(test_value):
                args = {'interface': 'e 0/49:1', 'linecard': '48XT'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
                args = {'interface': 'e 0/54:1', 'linecard': '48XT'}
                args['speed'] = test_value
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_slot_garbage(self):
        garbage = [1, 9, -1, 'a']
        for test_value in garbage:
            with self.subTest(test_value):
                args = {'speed': '100g', 'linecard': '48Y'}
                args['interface'] = 'e {}/49'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        for test_value in garbage:
            with self.subTest(test_value):
                args = {'speed': '100g', 'linecard': '48XT'}
                args['interface'] = 'e {}/49'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_48Y_port_garbage(self):
        for test_value in [0, 57, 'a', -1]:
            with self.subTest(test_value):
                args = {'speed': '100g', 'linecard': '48Y'}
                args['interface'] = 'e 0/{}'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_48XT_port_garbage(self):
        for test_value in [0, 55, 'a', -1]:
            with self.subTest(test_value):
                args = {'speed': '100g', 'linecard': '48XT'}
                args['interface'] = 'e 1/{}'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_port_channel_garbage(self):
        for test_value in [0, 257, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 'po {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_tunnel_garbage(self):
        for test_value in [0, 513, 'a', -1]:
            with self.subTest(test_value):
                args = {'tunnel_type': 'vxlan'}
                args['interface'] = 'tun {}'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_breakout_garbage(self):
        for test_value in [0, 5, 'a', -1]:
            with self.subTest(test_value):
                args = {'speed': '10g', 'linecard': '48Y'}
                args['interface'] = 'e 0/1:{}'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
                args = {'speed': '10g', 'linecard': '48XT'}
                args['interface'] = 'e 0/1:{}'.format(test_value)
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_mgmt_garbage(self):
        for test_value in [1, 3, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 'm {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_loopback_garbage(self):
        for test_value in [0, 256, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 'lo {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_ve_garbage(self):
        for test_value in [0, 8193, 'a', -1]:
            with self.subTest(test_value):
                args = {'interface': 've {}'.format(test_value)}
                self.assertRaises(ValueError, Slx9150_IfIndex, **args)
        return

    def test_mgmt_output(self):
        for test_value, test_result in [[0, 805306368]]:
            with self.subTest(test_value):
                args = {'interface': 'm {}'.format(test_value)}
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_port_channel_output(self):
        for test_value in range(1, 257):
            with self.subTest(test_value):
                test_result = 671088640 + test_value
                args = {'interface': 'po {}'.format(test_value)}
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_tunnel_output(self):
        max_tunnel_id = 1024
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'vxlan')):
                test_result = 2080374784 + test_value
                args = {'tunnel_type': 'vxlan'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'gre')):
                test_result = 2084569088 + test_value
                args = {'tunnel_type': 'gre'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'nvgre')):
                test_result = 2088763392 + test_value
                args = {'tunnel_type': 'nvgre'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        for test_value in range(1, max_tunnel_id + 1):
            with self.subTest((test_value, 'mpls')):
                test_result = 2092957696 + test_value
                args = {'tunnel_type': 'mpls'}
                args['interface'] = 'tunnel {}'.format(test_value)
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_ve_output(self):
        max_ve_id = 4096
        for test_value in range(1, max_ve_id + 1):
            with self.subTest((test_value)):
                test_result = 1207959552 + test_value
                args = {'interface': 've {}'.format(test_value)}
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_loopback_output(self):
        for test_value in range(1, 256):
            with self.subTest(test_value):
                test_result = 1476395008 + test_value
                args = {'interface': 'lo {}'.format(test_value)}
                result = Slx9150_IfIndex(**args)
                self.assertEqual(result.if_index.Decimal, test_result)
        return

    def test_48Y_port_output(self):
        args = {'speed': '10g', 'linecard': '48Y',
                'interface': 'e 0/1'}
        dummy = Slx9150_IfIndex(**args)
        intf_string = '000011'
        sub_port = self.bit_mapper(0, 4)
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for speed in ['100g', '40g', '25g', '10g']:
            speed_string = dummy.speed_map.map(speed)
            interfaces = [x.physical for x in dummy.mapping.interfaces
                          if speed in x.valid_speeds]
            for interface in interfaces:
                test_value = 'e {}/{}'.format(slot, interface)
                port_data = dummy.mapping.get_interface(interface)
                bit_map = (intf_string + slot_string
                           + self.bit_mapper(interface, 8) + sub_port
                           + speed_string
                           + self.bit_mapper(port_data.chip_num, 6))
                test_result = IfIndex(bit_map)
                with self.subTest(test_value):
                    args = {'speed': speed, 'linecard': '48Y'}
                    args['interface'] = '{}'.format(test_value)
                    result = Slx9150_IfIndex(**args)
                    self.assertEqual(result.if_index.Decimal,
                                     test_result.Decimal)
        return

    def test_48XT_port_output(self):
        args = {'speed': '10g', 'linecard': '48XT',
                'interface': 'e 0/1'}
        dummy = Slx9150_IfIndex(**args)
        intf_string = '000011'
        sub_port = self.bit_mapper(0, 4)
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for speed in ['100g', '40g', '10g']:
            speed_string = dummy.speed_map.map(speed)
            interfaces = [x.physical for x in dummy.mapping.interfaces
                          if speed in x.valid_speeds]
            for interface in interfaces:
                test_value = 'e {}/{}'.format(slot, interface)
                port_data = dummy.mapping.get_interface(interface)
                bit_map = (intf_string + slot_string
                           + self.bit_mapper(interface, 8) + sub_port
                           + speed_string
                           + self.bit_mapper(port_data.chip_num, 6))
                test_result = IfIndex(bit_map)
                with self.subTest(test_value):
                    args = {'speed': speed, 'linecard': '48XT'}
                    args['interface'] = '{}'.format(test_value)
                    result = Slx9150_IfIndex(**args)
                    self.assertEqual(result.if_index.Decimal,
                                     test_result.Decimal)
        return

    def test_48Y_breakout_port_output(self):
        args = {'speed': '10g', 'linecard': '48Y',
                'interface': 'e 0/1'}
        dummy = Slx9150_IfIndex(**args)
        intf_string = '000011'
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for speed in ['25g', '10g']:
            speed_string = dummy.speed_map.map(speed)
            interfaces = [x.physical for x in dummy.mapping.interfaces
                          if speed in x.breakout_speeds]
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
                    with self.subTest(msg='{}, {}'.format(test_value, speed)):
                        args = {'speed': speed, 'linecard': '48Y'}
                        args['interface'] = '{}'.format(test_value)
                        result = Slx9150_IfIndex(**args)
                        self.assertEqual(result.if_index.Decimal,
                                         test_result.Decimal)
        return

    def test_48XT_breakout_port_output(self):
        args = {'speed': '10g', 'linecard': '48XT',
                'interface': 'e 0/1'}
        dummy = Slx9150_IfIndex(**args)
        intf_string = '000011'
        slot = 0
        slot_string = self.bit_mapper(slot, 5)
        for speed in ['10g']:
            speed_string = dummy.speed_map.map(speed)
            interfaces = [x.physical for x in dummy.mapping.interfaces
                          if speed in x.breakout_speeds]
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
                    with self.subTest(msg='{}, {}'.format(test_value, speed)):
                        args = {'speed': speed, 'linecard': '48XT'}
                        args['interface'] = '{}'.format(test_value)
                        result = Slx9150_IfIndex(**args)
                        self.assertEqual(result.if_index.Decimal,
                                         test_result.Decimal)
        return
