#!/usr/bin/python3
import sys
import unittest
from BitMap import BitMap
from SLXRSpeedMap import SLXRSpeedMap


class TestSLXRSpeedMap(unittest.TestCase):
    def test_input(self):
        self.assertRaises(ValueError, SLXRSpeedMap, 0)
        self.assertRaises(ValueError, SLXRSpeedMap, 32)
        self.assertRaises(ValueError, SLXRSpeedMap, -1)
        self.assertRaises(TypeError, SLXRSpeedMap, 'a')
        self.assertRaises(TypeError, SLXRSpeedMap, 2.5)
        self.assertRaises(TypeError, SLXRSpeedMap, [1])
        self.assertRaises(TypeError, SLXRSpeedMap, True)
        return

    def test_output(self):
        dummy = SLXRSpeedMap()
        self.assertEqual(dummy.map('1g'), '010')
        self.assertEqual(dummy.map('10g'), '000')
        self.assertEqual(dummy.map('25g'), '101')
        self.assertEqual(dummy.map('40g'), '011')
        self.assertEqual(dummy.map('50g'), '110')
        self.assertEqual(dummy.map('100g'), '100')
        return
