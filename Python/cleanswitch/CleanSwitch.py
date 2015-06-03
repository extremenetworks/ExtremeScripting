#!/usr/bin/env python
'''
Script        : CleanSwitch
Revision      : 1.0

Purpose:  This widget provides a method of deleting all configuration
          parameters and files from an ExtremeXOS(TM) switch.  Once the
          files are removed, the switch will reboot using its factory
          default configuration.

          Specifically, this widget performs the following functions:

          1.  Removes all files from the internal drive
          2.  Removes all log entries
          3.  Removes administrative password and SSH private key
          4.  Reboots the switch using default configuration
'''
def exosCmd(cmd):
    print cmd
    try:
        exsh.clicmd(cmd,True)
    except RuntimeError as msg:
        print 'Error',msg
    return

exosCmd('rm *')
exosCmd('clear log messages nvram')
exosCmd('clear log static')
exosCmd('unconfigure switch all')
