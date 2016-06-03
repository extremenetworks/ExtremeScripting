from exsh import clicmd
from difflib import Differ
from time import time


def main():

    print "Comparing configurations, please wait..."

    #create unique names for temp files

    t_stamp = str(time())

    saved_name = '/usr/local/cfg/saved_{0}.temp'.format(t_stamp[:-3])
    running_name = '/usr/local/cfg/running_{0}.temp'.format(t_stamp[:-3])
    temp_config = 'temp_{0}'.format(t_stamp[:-3])

    saved_file = open(saved_name, 'w')
    running_file = open(running_name, 'w')


    # find the selected config file
    output = clicmd('show switch | include "Config Selected"', True).split()
    selected_config = output[2]
    selected_config = selected_config[:-4]

    # save the running config to a temp file, 
    # then convert both config files from XML to human-readable format

    clicmd("save config {0}".format(temp_config))
    saved_file.write(clicmd("debug cfgmgr show configuration file {0}".format(selected_config), True))
    running_file.write(clicmd("debug cfgmgr show configuration file {0}".format(temp_config), True))

    # set the selected config back, since the save config changed it
    clicmd("use config {0}".format(selected_config), False)

    # close the files, and reopen them for reading
    saved_file.close()
    running_file.close()

    saved_file = open(saved_name, 'r')
    running_file = open(running_name, 'r')

    # diff the two configs


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
    clicmd("rm {0}".format(saved_name))
    clicmd("rm {0}".format(running_name))
    clicmd("rm {0}.cfg".format(temp_config))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to login prompt
        pass