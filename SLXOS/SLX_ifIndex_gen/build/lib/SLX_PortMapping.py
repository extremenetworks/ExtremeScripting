#!/usr/bin/python3
from SLX_PortData import PortData


class PortMapping():
    '''Port data management class.
    methods:
        add_interface - Adds an interface into the data structure.
                        See the PortData class for needed information.

        get_interface - Returns the PortData class for the desired port.

        get_max_interface - Returns the highest physical port in the
                            PortMapping.
    '''
    def __init__(self):
        self.interfaces = []

    def add_interface(self, physical,  chip_port, chip_num=0,
                      valid_speeds=['10g'], breakout=False,
                      breakout_speeds=[]):
        self.interfaces.append(PortData(physical, chip_port, chip_num,
                                        valid_speeds, breakout,
                                        breakout_speeds))
        return

    def get_interface(self, physical=''):
        int_list = [x for x in self.interfaces if x.physical == physical]
        if int_list:
            return int_list[0]
        return []

    def get_max_interface(self):
        return str(sorted([int(x.physical) for x in self.interfaces])[-1])


def main():
    pass


if __name__ == '__main__':
    main()
