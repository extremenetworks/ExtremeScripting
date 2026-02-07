#!/usr/bin/env python2.7

# usage: mibview.py [-h] mibString
# 
# Convert wildcarded OID MIB views into OID/mask format as used by EXOS.
# 
# positional arguments:
#   mibString   Wildcard MIB string to be translated into OID/mask format
# 
# optional arguments:
#   -h, --help  show this help message and exit

import argparse
import sys


class ArgParser(argparse.ArgumentParser):
   def error(self, message):
      sys.stderr.write('error: %s\n' % message)
      self.print_help()
      sys.exit(2)


def main():

    parser = ArgParser(prog='mibview.py',
                       description='Convert wildcarded OID MIB views into OID/mask format as used by EXOS.')

    parser.add_argument('mibString',
                         help='Wildcard MIB string to be translated into OID/mask format',
                         type=str, nargs=1)

    args = parser.parse_args()

    mibView = args.mibString[0].split('.')

    #Bitmask to be used in the final output.
    mask = 0

    newMibView = []

    for branch in mibView:
        #Left shift the bits in the mask. 
        mask = mask << 1

        if branch is not '*': 
            #Insert a 1 in the low-order bits of the mask.
            mask = mask + 1
            #Also, add this value to the new MIB view we are building.
            newMibView.append(branch)

        else:
            #Keep the zero in the low-order bit. Add a zero to the new MIB view we are building.
            newMibView.append('0')


    
    newMibView = ".".join(newMibView)

    print newMibView + '/' + format(mask, 'X')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        #Catch SystemExit to prevent EXOS shell from exiting to login prompt, if we're running this in EXOS
        pass
