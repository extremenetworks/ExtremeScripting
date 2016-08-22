#!/usr/bin/env python

# Wizard to configure or delete SNMPv3 configuration
##############################################################################
# Imports
##############################################################################
import re
#############################################################################
# SNMP v3 Variable definitions
#############################################################################
config = exsh.clicmd('show config snmp', capture=True)
version = exsh.clicmd('show version', capture=True)
##############################################################################
# Main function
##############################################################################
def main():
    dec = get_input('Would you like to (D)elete or (C)onfigure SNMPv3? ', 2)
    ###############################################################################
    # Delete SNMP configuration function
    ###############################################################################
    if dec == 'd':
        confirmation = get_input("This script will completely delete the currently existing SNMPv3 configuration. "
                                 "Are you sure you wish to do this? (y/n): ", 0)
        if confirmation:
            print("Deleting SNMP configuration...")
            exsh.clicmd('create log entry \"Deleting SNMP Configuration using SNMPassist.py\"', capture=True)
            print("Deleting trap receivers...")
            exsh.clicmd('configure snmp delete trapreceiver all')
            print("Deleting notification logs...")
            exsh.clicmd('configure snmp delete notification-log default', capture=False)
            print("Deleting non-default SNMPv3 groups")
            print("Deleting non-default SNMPv3 access profiles...")
            exsh.clicmd('configure snmpv3 delete access all-non-defaults')
            print("Deleting non-default SNMPv3 communities...")
            exsh.clicmd('configure snmpv3 delete community all-non-defaults')
            print("Deleting filters...")
            exsh.clicmd('configure snmpv3 delete filter all')
            print("Deleting filter profiles...")
            exsh.clicmd('configure snmpv3 delete filter-profile all')
            print("Deleting non-default mib views...")
            exsh.clicmd('configure snmpv3 delete mib-view all-non-defaults')
            print("Deleting non-default notify configurations...")
            exsh.clicmd('configure snmpv3 delete notify all-non-defaults')
            print("Deleting notify target addresses...")
            exsh.clicmd('configure snmpv3 delete target-addr all')
            print("Deleting target parameters...")
            exsh.clicmd('configure snmpv3 delete target-params all')
            print("Deleting non-default SNMPv3 users...")
            exsh.clicmd('configure snmpv3 delete user all-non-defaults')
            print("Deleting non-default communities...")
            exsh.clicmd('configure snmp delete community readwrite all')
            print("Deleting SNMP readonly communities...")
            exsh.clicmd('configure snmp delete community readonly all')
            print("Deleting groups...")
            for line in config.splitlines():
                p = re.compile(ur'configure\ssnmpv3\sadd\sgroup\s\"(\S+)"')
                x = re.search(p, line)
                if x != None:
                    exsh.clicmd('configure snmpv3 delete group ' + x.group(1) + ' user all-non-default', capture=True)
            print("Enabling SNMPv3 default group...")
            exsh.clicmd('enable snmpv3 default-group')
            print("Enabling SNMPv3 default user...")
            exsh.clicmd('enable snmpv3 default-user')
            print
            exsh.clicmd('create log entry \"SNMP configuration has been deleted by SNMPassist.py\"', capture=True)
            print("SNMP configuration has been deleted.")

    ####################################################################################
    # Configure SNMPv3 function
    ####################################################################################
    if dec == 'c':
        exsh.clicmd('create log entry \"Starting configuration of SNMPv3 using SNMPassist.py\"', capture=True)
        snmpuser = raw_input("Please enter your SNMPv3 User name: ")
        authpw = get_input("Please enter your SNMPv3 User password (8 to 49 char): ", 1)
        privpw = get_input("Please enter your SNMPv3 privacy password (8 to 49 char): ", 1)
        authtype = get_input("Please enter your authentication type (SHA/MD5): ", 3)
        privtype = get_input("Please enter your encryption type (3DES, AES, DES, HEX): ", 4)
        if privtype == 'aes':
            string = exsh.clicmd('show configuration', True)
            if string.find("enable ssh2") != -1:
                pass
            else:
                print
                ynenablessh = get_input("SSH2 must be enabled to configure privacy type as AES. If you choose to \n"
                                        'enable it, key generation can take 10-15 minutes to complete and the \nCLI '
                                        'will be unavailable during that time. \n'
                                         "Would you like to enable it? (y/n): ", 0)
                if version.find('21.1') != -1 or version.find('16.2') != -1:
                    if ynenablessh:
                        exsh.clicmd('enable ssh2', capture=True)
                        print('After running the script, please restart process snmpMaster and snmpSubagent')
                    else:
                        privtype = get_input("Please enter your encryption type (DES, HEX): ", 5)
                else:
                    print('Please download and install the SSH xmod from https://support.extremenetworks.com')
                    print('After installing the SSH xmod, please re-run the script to complete configuration '
                          'after SSH is enabled.')
                    pass
        if privtype == '3des':
            string = exsh.clicmd('show configuration', True)
            if string.find("enable ssh2") != -1:
                pass
            else:
                print
                ynenablessh = get_input("SSH2 must be enabled to configure privacy type as 3DES. If you choose to \n"
                                        'enable it, key generation can take 10-15 minutes to complete and the \nCLI '
                                        'will be unavailable during that time. \n'
                                         "Would you like to enable it? (y/n): ", 0)
                if version.find('21.1') != -1 or version.find('16.2') != -1:
                    if ynenablessh:
                        exsh.clicmd('enable ssh2', capture=True)
                        print('After running the script, please restart process snmpMaster and snmpSubagent')
                else:
                    print('Please download and install the SSH xmod from our support portal')
                    print('After installing the SSH xmod, please re-run the script to complete configuration '
                          'after SSH is enabled.')
                    pass
        exsh.clicmd('configure snmpv3 add user {0} authentication {1} {2} privacy {3} {4}'.format
                    (snmpuser, authtype, authpw, privpw, privtype))
        print
        print('SNMP Group name is used to link multiple SNMP users together. Its not something that '
              'Netsight/ExtremeControl asks for.')
        snmpgroupname = raw_input("Please enter your SNMPv3 Group name: ")
        exsh.clicmd('configure snmpv3 add group {0} user {1} sec-model usm'.format(snmpgroupname,snmpuser), capture=True)
        snmpaccessname = raw_input("Please enter your SNMPv3 Access preferences: ") #Optional to enter a new access name
        exsh.clicmd('configure snmpv3 add access %s sec-model usm sec-level priv read-view defaultAdminView '
                    'write-view defaultAdminView notify-view defaultAdminView' % snmpaccessname, capture=True)
        yndisablev1v2access = get_input("Would you like to disable SNMP v1v2c access? (y/n): ", 0)
        yndisablev3user = get_input("Would you like to disable the default SNMPv3 user? (y/n): ", 0)
        yndisablev3group = get_input("Would you like to disable the default SNMPv3 group? (y/n): ", 0)
        exsh.clicmd('enable snmp access vr vr-default', capture=True)
        if yndisablev1v2access:
            exsh.clicmd('disable snmp access snmp-v1v2c')
        else:
            exsh.clicmd("enable snmp access snmp-v1v2c")
        if yndisablev3user:
            exsh.clicmd("disable snmpv3 default-user")
        else:
            exsh.clicmd("enable snmpv3 default-user")
        if yndisablev3group:
            exsh.clicmd("disable snmpv3 default-group")
        else:
            exsh.clicmd("enable snmpv3 default-group")
        exsh.clicmd('create log entry \"SNMPv3 configuration has been completed using SNMPassist.py\"', capture=True)
        print("SNMPv3 configuration has been completed")


def get_input(request, fmt_chk):
    '''
    :param request:

    :param fmt_chk: Indicates what format check is required
    0 = Y/N
    1 = Password Check
    2 = Args check
    :return:
    '''
    input = raw_input(request)
    if fmt_chk == 0:
        if input in ('y', 'Y'):
            return True
        elif input in ('n', 'N', ''):
            return False
        print 'Invalid input.  Please enter \'y\' or \'n\''
        get_input(request, fmt_chk)
    if fmt_chk == 1:
        if 7 < len(input) < 49:
            return input
        print 'Invalid input.  Password must be between 8 and 49 characters'
        get_input(request, fmt_chk)
    if fmt_chk == 2:
        if input in ('d', 'D'):
            return "d"
        elif input in ('c', 'C', ''):
            return "c"
        print 'Invalid input.  Please enter \'D\' or \'C\''
        get_input(request, fmt_chk)
    if fmt_chk == 3:
        if input in ('md5', 'MD5', 'Md5', 'mD5'):
            return "md5"
        elif input in ('SHA', 'sha', 'sHa', 'Sha', 'sHA', 'SHa'):
            return "sha"
        print 'Invalid input. Please enter \'sha\' or \'md5\''
        get_input(request, fmt_chk)
    if fmt_chk == 4:
        if input in ('3DES', '3des', '3Des', '3DEs', '3dES', '3DeS', '3DeS'):
            return "3des"
        if input in ('aes', 'AES', 'Aes', 'AEs', 'aeS', 'AeS'):
            return "aes"
        if input in ('hex', 'Hex', 'hEx', 'heX', 'HEx', 'hEX', 'HeX'):
            return "hex"
        elif input in ('des', 'DES', 'DEs', 'Des', 'dES'):
            return "des"
        print 'Invalid input.  Please enter \'sha\' or \'md5\''
    if fmt_chk == 5:
        if input in ('des', 'DES', 'DEs', 'Des', 'dES'):
            return "des"
        elif input in ('hex', 'Hex', 'hEx', 'heX', 'HEx', 'hEX', 'HeX'):
            return "hex"
        print 'Invalid input. Please enter \'hex\' or \'des\''

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass