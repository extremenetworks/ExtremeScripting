#!/usr/bin/python3
import sys
import unittest
from BitMap import BitMap
from SLXSSpeedMap import SLXSSpeedMap


class TestSLXSSpeedMap(unittest.TestCase):
    def test_input(self):
        self.assertRaises(ValueError, SLXSSpeedMap, 0)
        self.assertRaises(ValueError, SLXSSpeedMap, 32)
        self.assertRaises(ValueError, SLXSSpeedMap, -1)
        self.assertRaises(TypeError, SLXSSpeedMap, 'a')
        self.assertRaises(TypeError, SLXSSpeedMap, 2.5)
        self.assertRaises(TypeError, SLXSSpeedMap, [1])
        self.assertRaises(TypeError, SLXSSpeedMap, True)
        return

    def test_output(self):
        dummy = SLXSSpeedMap()
        self.assertEqual(dummy.map('1g'), '001')
        self.assertEqual(dummy.map('10g'), '010')
        self.assertEqual(dummy.map('25g'), '110')
        self.assertEqual(dummy.map('40g'), '011')
        self.assertEqual(dummy.map('50g'), '111')
        self.assertEqual(dummy.map('100g'), '100')
        return
