# watch.py
# This script displays the output of a specified CLI command every n seconds
# 
# Usage: run script watch.py <seconds> <cli_cmd>
#     seconds: delay between commands in seconds
#     cli_cmd: CLI command to be watched
#
# Note: CLI commands will need to be enclosed in quotes
#
# Last updated: August 25, 2015


from exsh import clicmd
from time import sleep
import sys

if(len(sys.argv) == 3):
	command = sys.argv[2]
	time = int(sys.argv[1])

	while(True):
		print clicmd(command, True)
		sleep(time)

else:
	print "Error: Incorrect number of arguments"
	print "Usage: run script watch.py <seconds> <cli_cmd>"
	print "    seconds: time between commands in seconds"
	print "    cli_cmd: CLI command to be watched"
	print "Note: CLI commands will need to be enclosed in quotes"
