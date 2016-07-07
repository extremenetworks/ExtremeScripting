# watch.py
# usage: watch.py [-h] [-c COUNT] [-i INTERVAL] [-d] command
#
# This script displays the output of a specified CLI command every n seconds
# Example "run script watch.py "show port packet no-ref""
#
# positional arguments:
#   command               Command to iterate. Should be enclosed in quotes (i.e.
#                         "show l2stats vlan Mgmt")
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -c COUNT, --count COUNT
#                         Number of times to issue the command (default 3)
#   -i INTERVAL, --interval INTERVAL
#                         Wait time between command iterations (default 5 sec)
#   -d, --diff            If numerical values have changed in an ouput print
#                         difference between previous and current command
#                         iteration
# Last updated: March 31, 2016


import argparse
import shlex
from exsh import clicmd
from time import sleep
import sys
import re
import subprocess

def try_cli(command):
    """Try CLI command and exit if invalid"""

    try:
        return clicmd(command, True)
    except:
        print 'Script Error: Check Command Syntax'
        exit()

class ArgParser(argparse.ArgumentParser):
   def error(self, message):
      sys.stderr.write('error: %s\n' % message)
      self.print_help()
      sys.exit(2)


def main():

    parser = ArgParser(prog='watch.py', description = "This script displays the output of a "
                                                                        "specified CLI command every n seconds "
                                                                        "Example \"run script watch.py \"show port "
                                                                        "packet no-ref\"\"")
    parser.add_argument("command", help="Command to iterate.  Should be enclosed in quotes "
                                        "(i.e. \"show l2stats vlan Mgmt\")")
    parser.add_argument('-c', '--count', help='Number of times to issue the command (default 3)', type=int, default=3)
    parser.add_argument('-i', '--interval', help='Wait time between command iterations (default 5 sec)', type=int,
                        default=5)
    parser.add_argument('-d', '--diff', help='If numerical values have changed in an ouput print difference between '
                                             'previous and current command iteration', action="store_true")
    args = parser.parse_args()
    cmd = args.command
    count = args.count
    interval = args.interval
    stat_diff = args.diff

    cli_refresh = True
    # Check to see if cli refresh is disabled
    cli_out = clicmd('show management | include "CLI refresh"', True)
    if 'Disabled' in cli_out:
        cli_refresh = False

    print cli_refresh
    if cli_refresh:
        # Temporarily disable refreshing CLI commands to prevent script from hanging
        clicmd('disable cli refresh')

    if stat_diff:
        prev_output = try_cli(cmd)
        print prev_output
        count -=1
        prev_output = prev_output.split('\n')

        while count != 0:
            sleep(interval)
            curr_output = try_cli(cmd).split('\n')
            for index in range(len(prev_output)):
                # Split current and prev command outputs into list divided based on numerical and non-numerical strings
                prev = re.split(r'(\d+)', prev_output[index])
                curr = re.split(r'(\d+)', curr_output[index])
                for i in range(len(prev)):
                    if prev[i].isdigit() and curr[i] > prev[i]:
                        diff = int(curr[i]) - int(prev[i])
                        diff = '+' + str(diff)
                        FMT = '{0:>' + str(len(curr[i])) + '}'
                        sys.stdout.write(FMT.format(diff))
                    else:
                        sys.stdout.write(prev[i])
                sys.stdout.flush()
                print
            count -= 1
            prev_output = curr_output

    else:
        for i in range(count):
            print try_cli(cmd)
            sleep(interval)

    if cli_refresh:
        # Restore CLI refresh
        clicmd('enable cli refresh')


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass
