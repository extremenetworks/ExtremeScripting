#!/usr/bin/python3
from SLX_BitMap import BitMap


class TunnelTypeMap(BitMap, object):
    '''This is the tunnel type mapping for the SLX ifindex value.
    This applies only for tunnel interfaces'''
    def __init__(self, bit_count=4):
        self.mapping = {}
        self.validate_bit_count(bit_count)
        self.add_map('vxlan', 0)
        self.add_map('gre', 1)
        self.add_map('nvgre', 2)
        self.add_map('mpls', 3)
        return


def main():
    return


if __name__ == '__main__':
    main()
