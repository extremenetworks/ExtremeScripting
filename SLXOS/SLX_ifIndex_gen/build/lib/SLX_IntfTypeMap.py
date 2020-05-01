#!/usr/bin/python3
from SLX_BitMap import BitMap


class IntfTypeMap(BitMap):
    '''
    This has the mapping for the various interface types to a binary string.
    '''
    def __init__(self, bit_count=6):
        self.mapping = {}
        self.validate_bit_count(bit_count)
        # Physcial Break-out capable
        self.add_map('phy_bc', 3)
        self.add_map('phy',  6)
        # LAG (Port-channel) interface
        self.add_map('lag', 10)
        # VE (SVI) interface
        self.add_map('ve', 18)
        # Tunnel (MPLS, GRE, VxLAN) interface
        self.add_map('tunnel', 31)
        # L3 Loopback interface
        self.add_map('lb', 22)
        # Management interface (eth0, eth1, etc.,)
        self.add_map('mgmt', 12)
        return


def main():
    pass


if __name__ == '__main__':
    main()
