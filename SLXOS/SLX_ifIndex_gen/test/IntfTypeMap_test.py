#!/usr/bin/python3
import sys
import unittest
from BitMap import BitMap
from IntfTypeMap import IntfTypeMap


class TestIntfTypeMap(unittest.TestCase):
    def test_input(self):
        self.assertRaises(ValueError, IntfTypeMap, 0)
        self.assertRaises(ValueError, IntfTypeMap, 32)
        self.assertRaises(ValueError, IntfTypeMap, -1)
        self.assertRaises(TypeError, IntfTypeMap, 'a')
        self.assertRaises(TypeError, IntfTypeMap, 2.5)
        self.assertRaises(TypeError, IntfTypeMap, [1])
        self.assertRaises(TypeError, IntfTypeMap, True)
        return

    def test_output(self):
        dummy = IntfTypeMap()
        self.assertEqual(dummy.map('phy_bc'), '000011')
        self.assertEqual(dummy.map('phy'), '000110')
        self.assertEqual(dummy.map('lag'), '001010')
        self.assertEqual(dummy.map('ve'), '010010')
        self.assertEqual(dummy.map('tunnel'), '011111')
        self.assertEqual(dummy.map('lb'), '010110')
        self.assertEqual(dummy.map('mgmt'), '001100')
        return
