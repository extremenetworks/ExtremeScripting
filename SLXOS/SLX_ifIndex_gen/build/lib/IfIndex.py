#!/usr/bin/python3


class IfIndex():
    '''This is the class for the result of the ifindex script.'''
    def __init__(self, bit_map):
        self.Decimal = int(bit_map, 2)
        self.Hex = hex(int(bit_map, 2))[2:].zfill(8)
        self.binary = bit_map
        return


def main():
    pass


if __name__ == '__main__':
    main()
