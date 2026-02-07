from exsh import clicmd
from difflib import Differ
from time import time
import argparse

class ArgParser(argparse.ArgumentParser):
   def error(self, message):
      sys.stderr.write('error: %s\n' % message)
      self.print_help()
      sys.exit(2)



def main():

    parser = ArgParser(prog='conf_diff.py',
                       description='Compare the saved configuration with the currently running one.')

    parser.add_argument('-d', '--debug', 
                         help='Enables verbose logging and leaves temp files for debugging',
                         action='store_true')
    parser.add_argument('-c', '--clean',
                        help='Remove previous debug files. Executes "rm temp_*; rm *.temp"',
                        action='store_true')

    args = parser.parse_args()

    debug = args.debug
    clean = args.clean

    if clean:
        print "DEBUG: Cleaning up previous debug files"
        clicmd("rm temp_*")
        clicmd("rm *.temp")

    print "Comparing configurations, please wait..."

    #create unique names for temp files

    t_stamp = str(time())

    if debug:
        print "DEBUG: Creating temp files"

    saved_name = '/usr/local/cfg/saved_{0}.temp'.format(t_stamp[:-3])
    running_name = '/usr/local/cfg/running_{0}.temp'.format(t_stamp[:-3])
    temp_config = 'temp_{0}'.format(t_stamp[:-3])

    saved_file = open(saved_name, 'w')
    running_file = open(running_name, 'w')


    # find the selected config file

    if debug:
        print "DEBUG: Finding selected config"


    output = clicmd('show switch | include "Config Selected"', True).split()
    selected_config = output[2]
    selected_config = selected_config[:-4]

    # save the running config to a temp file, 
    # then convert both config files from XML to human-readable format

    if debug:
        print "DEBUG: Generating temp version of running config"

    clicmd("save config {0}".format(temp_config))

    if debug:
        print "DEBUG: Generating temp cfgmgr version of selected config"

    saved_file.write(clicmd("debug cfgmgr show configuration file {0}".format(selected_config), True))

    if debug:
        print "DEBUG: Generating temp cfgmgr version of running config"

    running_file.write(clicmd("debug cfgmgr show configuration file {0}".format(temp_config), True))

    # set the selected config back, since the save config changed it
    clicmd("use config {0}".format(selected_config), False)

    # close the files, and reopen them for reading
    saved_file.close()
    running_file.close()

    saved_file = open(saved_name, 'r')
    running_file = open(running_name, 'r')

    # diff the two configs

    if debug:
        print "DEBUG: Diffing configs"

    d = Differ()

    diff = list(d.compare(saved_file.readlines(), running_file.readlines()))

    # print the results of the diff
    print " "
    print "If line starts with \'+\', the command has been added since last save."
    print "If line starts with \'-\', the command was present in the last save, and has been deleted."
    print " "
    print "Config changes:"

    for line in diff:
        if line.startswith('+ ') or line.startswith('- '):
            print line[:-1]

    print "Note that this script has cleared the CLI dirty bit. The configuration has not been saved."
    
    # clean up
    saved_file.close()
    running_file.close()

    # remove files that were opened
    if not debug:
        clicmd("rm {0}".format(saved_name))
        clicmd("rm {0}".format(running_name))
        clicmd("rm {0}.cfg".format(temp_config))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to login prompt
        pass