#!/usr/bin/python3
from SLX_BitMap import BitMap


class SLXSSpeedMap(BitMap, object):
    '''This is the mapping for bits 8 to 6 for the SLX ifindex value.
    This mapping is only for the SLX 9140 and 9240'''
    def __init__(self, bit_count=3):
        self.mapping = {}
        self.validate_bit_count(bit_count)
        self.add_map('1g', 1)
        self.add_map('10g', 2)
        self.add_map('25g', 6)
        self.add_map('40g', 3)
        self.add_map('50g', 7)
        self.add_map('100g', 4)
        return


def main():
    return


if __name__ == '__main__':
    main()
