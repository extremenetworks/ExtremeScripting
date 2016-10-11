# usage: dhcp43.py [-h] [-s SERVER_ADDRESS] [-v VLAN_NAME] files [files ...]
# 
# This script will generate the hex needed to configure EXOS's built-in DHCP
# server with option 43 for ZTP. It will also either provide the command to use,
# or configure the option on the specified VLAN.
# 
# positional arguments:
#   files                 Files to be downloaded. If the '-s' option is used,
#                         this may be simply be a file name. If the '-s' option
#                         is not used, this should be a full URL. (IE,
#                         tftp://192.168.1.10/config.xsf)
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -s SERVER_ADDRESS, --server_address SERVER_ADDRESS
#                         IP Address of TFTP server for sub-option 100. May be
#                         omitted if a URL is used for sub-option 101.
#   -v VLAN_NAME, --vlan_name VLAN_NAME
#                         VLAN to configure option 43 on. If this is included,
#                         the option 43 config will be added to the DHCP server
#                         configuration on this switch for this VLAN. If not,
#                         the config command will simply be printed.



import binascii
import argparse
from exsh import clicmd
import sys

class ArgParser(argparse.ArgumentParser):
   def error(self, message):
      sys.stderr.write('error: %s\n' % message)
      self.print_help()
      sys.exit(2)


def main():

    parser = ArgParser(prog='dhcp43.py', 
                       description="This script will generate the hex needed to configure EXOS's built-in DHCP server with option 43 for ZTP. "
                                   "It will also either provide the command to use, or configure the option on the specified VLAN.")

    parser.add_argument('-s', '--server_address', 
                            help='IP Address of TFTP server for sub-option 100. May be omitted if a URL is used for sub-option 101.', 
                            type=str, default="")

    parser.add_argument('-v', '--vlan_name',
                            help='VLAN to configure option 43 on. If this is included, the option 43 config will be added to the DHCP '
                                 'server configuration on this switch for this VLAN. If not, the config command will simply be printed.', 
                            type=str, default="")
    parser.add_argument('files', 
                            help='Files to be downloaded. If the \'-s\' option is used, this may be simply be a file name. '
                                 'If the \'-s\' option is not used, this should be a full URL. (IE, tftp://192.168.1.10/config.xsf)',
                            type=str, nargs='+')

    args = parser.parse_args()

    vlan = args.vlan_name
    server = args.server_address
    files = args.files

    # Convert the IP address to hex, if it exists
    hex = []
    if len(server):
        
        ip = server.split('.')
        hex.append(binascii.hexlify(chr(100)))      #sub-option 100
        hex.append(binascii.hexlify(chr(4)))        #length = 4 bytes
        for i in ip:                                #convert each byte of the IP to hex
            hex.append(binascii.hexlify(chr(int(i)))) 

    # Convert the filenames/URLs to hex
    for i in files:
        
        hex.append(binascii.hexlify(chr(101)))      #sub-option 101
        hex.append(binascii.hexlify(chr(len(i))))   #length of filename/URL in bytes
        hex.append(binascii.hexlify(i))             #filename converted to hex
   

    #Generate the command needed to configure this:
    hex = ''.join(hex) #join all the hex into one string
    hex = ':'.join(hex[i:i+2] for i in range(0, len(hex), 2)) #delimit the bytes with ':', like EXOS expects

    
    if len(vlan): #if a vlan was give do the configuration
        cmd = 'configure vlan {0} dhcp-options code 43 hex {1}'.format(vlan, hex)
        clicmd(cmd)
    else:         #otherwise print the command
        vlan = '<vlan_name>'
        cmd = 'configure vlan {0} dhcp-options code 43 hex {1}'.format(vlan, hex)
        print cmd        
    

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        #catch SystemExit to prevent EXOS shell from exiting to login prompt
        pass