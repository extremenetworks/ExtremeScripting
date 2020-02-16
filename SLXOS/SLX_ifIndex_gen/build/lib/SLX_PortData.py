#!/usr/bin/python3


class PortData():
    '''PortData structure.
    physical  = the port number on the face plate of the SLX as a string
    chip_num =  the chip that port is connected to, default is 0
    chip_port =  the port on the chip the physical port is connected to.
    valid_speeds = list of strings with the valid speeds for the port.
    breakout = boolean if the port can do breakout to 4 10g or 4 25g
    '''
    def __init__(self, physical,  chip_port, chip_num=0,
                 valid_speeds=['10g'], breakout=False, breakout_speeds=[]):
        self.physical = physical
        self.chip_num = chip_num
        self.chip_port = chip_port
        self.valid_speeds = valid_speeds
        self.breakout = breakout
        if not self.breakout and breakout_speeds != []:
            raise ValueError('Interfaces that do not support breakout, cannot '
                             + 'have breakout_speeds defined')
        self.breakout_speeds = breakout_speeds
        return


def main():
    pass


if __name__ == '__main__':
    main()
