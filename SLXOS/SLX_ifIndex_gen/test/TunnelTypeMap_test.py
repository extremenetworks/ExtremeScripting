#!/usr/bin/python3
import sys
import unittest
from BitMap import BitMap
from TunnelTypeMap import TunnelTypeMap


class TestTunnelTypeMap(unittest.TestCase):
    def test_input(self):
        self.assertRaises(ValueError, TunnelTypeMap, 0)
        self.assertRaises(ValueError, TunnelTypeMap, 32)
        self.assertRaises(ValueError, TunnelTypeMap, -1)
        self.assertRaises(TypeError, TunnelTypeMap, 'a')
        self.assertRaises(TypeError, TunnelTypeMap, 2.5)
        self.assertRaises(TypeError, TunnelTypeMap, [1])
        self.assertRaises(TypeError, TunnelTypeMap, True)
        return

    def test_output(self):
        dummy = TunnelTypeMap()
        self.assertEqual(dummy.map('vxlan'), '0000')
        self.assertEqual(dummy.map('gre'), '0001')
        self.assertEqual(dummy.map('nvgre'), '0010')
        self.assertEqual(dummy.map('mpls'), '0011')
        return
