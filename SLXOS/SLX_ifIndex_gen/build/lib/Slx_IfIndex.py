#!/usr/bin/python3
import argparse
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
from Slx9850_IfIndex import Slx9850_IfIndex
from Slx9740_IfIndex import Slx9740_IfIndex
from Slx9640_IfIndex import Slx9640_IfIndex
from Slx9540_IfIndex import Slx9540_IfIndex
from Slx9250_IfIndex import Slx9250_IfIndex
from Slx9240_IfIndex import Slx9240_IfIndex
from Slx9150_IfIndex import Slx9150_IfIndex
from Slx9140_IfIndex import Slx9140_IfIndex
from Slx9030_IfIndex import Slx9030_IfIndex


class Slx_IfIndex(object):
    '''Slx_IfIndex class validates the device and passes all other data to the
    device specific class for further validation and computation.
    Methods:
        validate_device - Valdates that the device information from the user is
                          is a valid SLX device.

        get_if_index - Returns the ifindex in the specified format.
                       Formats are: decimal, binary, hex
    '''
    def __init__(self, interface, device, linecard='', speed='',
                 tunnel_type='', **kwargs):
        # add new SLX devices and thier classes here.
        self.device_class_map = {'9850': 'Slx9850_IfIndex',
                                 '9740': 'Slx9740_IfIndex',
                                 '9640': 'Slx9640_IfIndex',
                                 '9540': 'Slx9540_IfIndex',
                                 '9250': 'Slx9250_IfIndex',
                                 '9240': 'Slx9240_IfIndex',
                                 '9150': 'Slx9150_IfIndex',
                                 '9140': 'Slx9140_IfIndex',
                                 '9030': 'Slx9030_IfIndex',
                                 }
        self.validate_device(device)
        data = {'interface': interface, 'linecard': linecard,
                'speed': speed, 'tunnel_type': tunnel_type}
        arg_string = ', '.join(["{}='{}'".format(x, data[x])
                                for x in data.keys()])
        # instantiate the correct device class
        class_name = self.device_class_map[self.device]
        tmp_code = 'self.device_object = {}({})'.format(class_name, arg_string)
        self.device_object = None
        try:
            exec(tmp_code)
        except Exception as err:
            print('ERROR: Failed to init the device level class to calculate '
                  + 'the if_index due to the following:')
            raise err
        return

    def validate_device(self, device):
        if device not in self.device_class_map.keys():
            raise ValueError('{} is not a supported device')
        self.device = device
        return

    def get_if_index(self, format='decimal'):
        if format.lower() not in ['decimal', 'hex', 'binary']:
            raise ValueError('Format should be decimal, hex, or binary')
        if format.lower() == 'decimal':
            ret_val = self.device_object.if_index.Decimal
        if format.lower() == 'hex':
            ret_val = self.device_object.if_index.Hex
        if format.lower() == 'binary':
            ret_val = self.device_object.if_index.binary
        return ret_val


def main():
    return


if __name__ == '__main__':
    main()
