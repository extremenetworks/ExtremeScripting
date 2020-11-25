#!/usr/bin/python3
'''
*** Copyright (c) 2017-2020 by Extreme Networks, Inc.
*** All rights reserved.
'''

import argparse
import re
import sys
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
from Slx_IfIndex import Slx_IfIndex


def main():
    '''
    This script uses the device type, human readable interface, interface
    speed, and other information to calculate the SNMP IFINDEX for that
    interface, and returns it as a decimal (for use with snmp), hexadecimal, or
    a binary value as a string.
    '''
    sys.tracebacklimit = 0
    parser = argparse.ArgumentParser(description='Script to generate ifIndex '
                                     + 'offline for SLX family of products.')
    parser.add_argument('--interface', '-i',
                        help='The interface name in the format of '
                        + '<type> <slot>/<port> or <type> <port>. '
                        + 'Examples: e 1/1, e 2/1:1, tun 1, ve 20,  po 1, m 1',
                        required=True)
    parser.add_argument('--device', '-d', type=str,
                        help='SLX device  in the format of the 4 digit '
                        + 'product number. Examples: 9850, 9140',
                        required=True)
    parser.add_argument('--linecard', '-l', default='', type=str,
                        choices=['72x10G', '36x100G', '48Y', '48XT', '40C',
                                 '80C'],
                        help='LC type for 9850, or model for 9150 '
                        + 'for physical ports', required=False)
    parser.add_argument('--speed', '-s', default='10g', type=str,
                        help='physical interface speed: [1g | 10g | 25g | 40g '
                        + '| 100g]', required=False)
    parser.add_argument('--tunnel_type', '-t', default='', type=str,
                        choices=['vxlan', 'gre', 'nvgre', 'mpls'],
                        help='Tunnel types', required=False)
    parser.add_argument('--output', '-o', default='dec',
                        choices=['dec', 'hex', 'bin', 'all'],
                        help='Output Display Mode: [bin | dec | hex | all]'
                        + '(default: dec)', required=False)
    args = parser.parse_args()
    args_dict = vars(args)
    # args1 = {'interface': 'e 1/1', 'linecard': '36x100G', 'device': '9850',
    #          'disp_mode': 'decimal', 'speed': '100g', 'tunnel_type': None}
    dummy = Slx_IfIndex(**args_dict)
    if args.output in ['dec', 'all']:
        print(dummy.get_if_index('decimal'))
    if args.output in ['hex', 'all']:
        print(dummy.get_if_index('hex'))
    if args.output in ['bin', 'all']:
        print(dummy.get_if_index('binary'))
    return


if __name__ == '__main__':
    main()
