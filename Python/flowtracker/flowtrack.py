"""
Flow tracker was made to easily apply dynamic ACLs
to count packets to see if traffic is received or sent on our switches.
"""
import argparse
import re
import json


def arg_parse():
    """arg_parse is used to capture user arguments and add them into a dictionary depending on what arguments are used.
    This dictionary is used throughout the script to check user input.
    """
    acl_name = 'Flow_track'
    parser = argparse.ArgumentParser(prog='flowtrack.py',
                                     description="This program is used to create a dynamic acl to count L2 or "
                                                 "L3 packets.  The ACL will not deny any traffic.  If creating"
                                                 " an L3 flow tracker use -i, -sip, -dip arguments.  If "
                                                 "creating an L2 flow tracker use -i, -sm, -dm arguments."
												 "To match on ICMP use '-p icmp'. For egress ACL use '-e'")
    parser.add_argument('-r', '--remove', help='removes all Flow_track ACLs from the switch', action='store_true')
    parser.add_argument('-p', '--protocol', nargs='?', const='NA', default='',
                        help='Protocol to match on.  ("ICMP") only')
    parser.add_argument('-sm', '--source_mac', nargs='?', const='None', default='None', help='Source MAC address',
                        required=False)
    parser.add_argument('-dm', '--destination_mac', nargs='?', const='None', default='None',
                        help='Destination MAC address', required=False)
    parser.add_argument('-sip', '--source_ip', nargs='?', const='None', default='None', help='Source IP address',
                        required=False)
    parser.add_argument('-dip', '--destination_ip', nargs='?', const='None', default='None',
                        help='Destination IP address', required=False)
    parser.add_argument('-i', '--interface', nargs='?', const='NA',
                        help='Switch Port number to apply the ACL counter', required=False)
    parser.add_argument('-e', '--egress', help='Make egress ACL (default: ingress)', action='store_true')
    args = parser.parse_args()

    if args.remove:
        acl_data = {'acl_name': acl_name}
        acl_clean(acl_data)
        quit()
    if args.egress:
        egress = 'egress'
    else:
        egress = 'ingress'

    # This will check to see if enough data was provided to make a IP ACL
    if args.source_ip != 'None' or args.destination_ip != 'None':
        if args.source_ip == 'None' and args.destination_ip == 'None':
            return False
        if args.source_mac == 'None' and args.destination_mac == 'None':
            L2_L3 = 'l3'
            protocol = args.protocol.lower()
            src_ip = args.source_ip
            dst_ip = args.destination_ip
            interface = args.interface

            return {'protocol': protocol, 'src_ip': src_ip, 'dst_ip': dst_ip, 'interface': interface, 'L2_L3': L2_L3,
                    'acl_name': acl_name, 'egress': egress}
    # This will check to see if enough data was provided to make a MAC ACL
    if args.source_mac != 'None' or args.destination_mac != 'None':
        if args.source_mac == 'None' and args.destination_mac == 'None':
            return False
        if args.source_ip == 'None' and args.destination_ip == 'None':
            L2_L3 = 'l2'
            protocol = args.protocol.lower()
            src_mac = args.source_mac
            dst_mac = args.destination_mac
            interface = args.interface
            return {'protocol': protocol, 'src_mac': src_mac, 'dst_mac': dst_mac, 'interface': interface,
                    'L2_L3': L2_L3, 'acl_name': acl_name, 'egress': egress}
    else:
        return False
    return False



def acl_clean(acl_data):
    print
    """
    acl_clean is called from all_check, it takes data from arg_parse and
    checks if the ACL has already been created.  If created it will unconfigure the ACL and print
    commands used to delete it.
    """
    try:
        acl_list = []
        cmd = 'debug cfgmgr show next acl.dynEntry'
        result = json.loads(exsh.clicmd(cmd, capture=True))
        for acl in result['data']:
            acl = str(acl['entryName'])
            acl_list.append(acl)
        if acl_data['acl_name'] in acl_list:
            cmd1 = "configure access-list delete %s all" % acl_data['acl_name']
            cmd2 = "delete access-list %s" % acl_data['acl_name']
            exsh.clicmd(cmd1)
            exsh.clicmd(cmd2)
            print ("+--------------------------------------------------+")
            print ("|          Removed ACL %s                  |") % acl_data['acl_name']
            print ("+--------------------------------------------------+")
            print ("| Commands used to remove ACL:                     |")
            print ("| %s      |") % cmd1
            print ("| %s                    |") % cmd2
            print ("+--------------------------------------------------+")
        else:
            pass
    except RuntimeError as cmdMsg:
        print 'Error:', cmdMsg, ':', cmd
        exsh.clicmd('create log message "flow_mod.py: Error: cmd={0} : msg={1}"'.format(cmd, cmdMsg), capture=False)
        return False



def port_check(port):
    """
    port_check is called from all_check.
    port_check runs the EXOS command "debug cfgmgr show next vlan.show_ports_info portList=* port=None"
    and grabs all ports provided into the function and places it into a dictionary;
    then it checks to see if 'ERROR' is in the table.  If it is the function returns false.  If not returns true.
    """
    try:
        ports_result = []
        cmd = 'debug cfgmgr show next vlan.show_ports_info portList={0} port=None'.format(port)
        result = json.loads(exsh.clicmd(cmd, capture=True))
        for status in result['data']:
            ports_result.append(status['status'])
        if 'ERROR' in ports_result:
            return False
        else:
            return True
    except RuntimeError as cmdMsg:
        print 'Error:', cmdMsg, ':', cmd
        exsh.clicmd('create log message "flow_mod.py: Error: cmd={0} : msg={1}"'.format(cmd, cmdMsg), capture=False)
        return False


def check_ip(ip):
    """
    check_ip is called from all_check.
    check_ip takes arguments src_ip and dst_ip from acl_data one at a time and parses through
    both variables to make sure they are correct ip addresses.

    Returns True if IP is correct, returns False if IP is wrong format.
    """
    ip = ip.split('.')

    if len(ip) != 4:
        return False
    for ock in ip:
        if not ock.isdigit():
            return False
        i = int(ock)
        if i < 0 or i > 255:
            return False
    return True


def check_mac(mac):
    """
    check_mac is called from all_check.
    check_mac takes arguments smac and dmac one at a time from variable in the acl_data dictionary and parses through
    them to make sure they are correct mac addresses.

    Returns True if MAC is correct returns False if MAC is wrong format.
    """
    allowed = re.compile(r"""
                         (
                             ^([0-9A-F]{2}[-]){5}([0-9A-F]{2})$
                            |^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$
                         )
                         """,
                         re.VERBOSE | re.IGNORECASE)

    if allowed.match(mac) is None:
        return False
    else:
        return True


def proto_check(proto):
    """
    proto_check is called from all_check.
    proto_check takes input of the protocol variable in the acl_data dictionary
    and checks to make sure the protocol is ip of icmp only.
    """
    if proto == 'NA':
        print ("Proto value not provided")
        return False
    if proto == 'icmp' or proto == '':
        return True
    else:
        print ("Protocol Check Failed")
        return False


def l2_l3_check(acl_data):
    """
    l2_l3_check is called from all_check.
    l2_l3_check takes the dictionary acl_data and parses the
    dictionary to make sure the user entered the required data.

    Returns True if required data is present in the acl_data dictionary.

    Returns False if required data is NOT present in the acl_data dictionary.
    """
    if acl_data['L2_L3'] == 'l2':
        smac = check_mac(acl_data['src_mac'])
        dmac = check_mac(acl_data['dst_mac'])
        if acl_data['src_mac'] == 'None' and acl_data['dst_mac'] == 'None':
            print ("SMAC and DMAC was not called")
            return False
        if smac == True and dmac == True:
            return True
        if smac:
            if acl_data['dst_mac'] == 'None':
                return True
        if dmac:
            if acl_data['src_mac'] == 'None':
                return True
        else:
            return False

    elif acl_data['L2_L3'] == 'l3':
        sip = check_ip(acl_data['src_ip'])
        dip = check_ip(acl_data['dst_ip'])
        if acl_data['src_ip'] == 'None' and acl_data['dst_ip'] == 'None':
            print ("SIP and DIP is = to None")
            return False
        if sip == True and dip == True:
            return True
        if sip:
            if acl_data['dst_ip'] == 'None':
                return True
        if dip:
            if acl_data['src_ip'] == 'None':
                return True
        else:
            return False


def all_check(acl_data):
    """
    all_check is used to call all functions to check required user input before applying ACL.
    If all called functions return true, all_check returns true if one returns false all_check returns False
    """
    acl_clean(acl_data)

    proto_status = proto_check(acl_data['protocol'])
    if acl_data['interface'] == 'None':
        return False
    port_final = port_check(acl_data['interface'])
    L2_L3_status = l2_l3_check(acl_data)

    if proto_status and L2_L3_status and port_final:
        return True
    else:
        return False


def acl_maker():
    """
    acl_maker is used to call arg_parse to capture user input, and then run all_check to verify user input.
    If arg_parse returns data it will run all_check to check user input.  If all check returns true the acl_data
    will be formatted and returned to main for use in acl_apply
    """
    acl_data = arg_parse()

    if acl_data is not False:
        all_done = all_check(acl_data)
        if all_done:

            if acl_data['protocol'] == 'icmp':
                acl_data['protocol'] = 'protocol icmp;'

            if acl_data['L2_L3'] == 'l2' and acl_data['src_mac'] == 'None':
                acl_data['dst_mac'] = acl_data['dst_mac'].replace('-', ':')
                acl_data['dst_mac'] = "ethernet-destination-address %s" % acl_data['dst_mac']
                acl_data['src_mac'] = ""
                return acl_data

            if acl_data['L2_L3'] == 'l2' and acl_data['dst_mac'] == 'None':
                acl_data['src_mac'] = acl_data['src_mac'].replace('-', ':')
                acl_data['src_mac'] = "ethernet-source-address %s" % acl_data['src_mac']
                acl_data['dst_mac'] = ""
                return acl_data

            if acl_data['L2_L3'] == 'l2' and acl_data['src_mac'] != '' and acl_data['dst_mac'] != '':
                acl_data['dst_mac'] = acl_data['dst_mac'].replace('-', ':')
                acl_data['src_mac'] = acl_data['src_mac'].replace('-', ':')
                acl_data['src_mac'] = "ethernet-source-address %s" % acl_data['src_mac']
                acl_data['dst_mac'] = ";ethernet-destination-address %s" % acl_data['dst_mac']
                return acl_data

            if acl_data['L2_L3'] == 'l3' and acl_data['src_ip'] == 'None':
                acl_data['dst_ip'] = "destination-address %s/32" % acl_data['dst_ip']
                acl_data['src_ip'] = ""
                return acl_data

            if acl_data['L2_L3'] == 'l3' and acl_data['dst_ip'] == 'None':
                acl_data['src_ip'] = "source-address %s/32" % acl_data['src_ip']
                acl_data['dst_ip'] = ""
                return acl_data

            if acl_data['L2_L3'] == 'l3' and acl_data['src_ip'] != '' and acl_data['dst_ip'] != '':
                acl_data['src_ip'] = "source-address %s/32" % acl_data['src_ip']
                acl_data['dst_ip'] = ";destination-address %s/32" % acl_data['dst_ip']
                return acl_data
        else:
            return False
    else:
        return False


def acl_apply(acl_data):
    try:
        """
        acl_apply is called from main if acl_maker returns true.
        This function apply's the ACL and displays the result of the ACL being applied, and commands used.
        If the ACL apply failed, an error is thrown.
        """

        show1 = "show access-list dynamic rule %s" % acl_data['acl_name']
        show2 = "show access-list dynamic counter ports %s %s" % (acl_data['interface'], acl_data['egress'])

        if acl_data['L2_L3'] == 'l2':

            cmd1 = "create access-list %s \"%s%s%s\" \"count %s\"" % (
                acl_data['acl_name'], acl_data['protocol'], acl_data['src_mac'], acl_data['dst_mac'], acl_data['acl_name'])
            cmd2 = "configure access-list add %s first ports %s %s" % (acl_data['acl_name'], acl_data['interface'], acl_data['egress'])

            cmd1ex = exsh.clicmd(cmd1, capture=True)

            if cmd1ex == "":
                cmd2ex = exsh.clicmd(cmd2, capture=True)
                if 'done' in cmd2ex:
                    print ("      L2 ACL applied correctly")
                    print ("+-----------------------------------+")
                    print ("|               ACL                 |")
                    print ("+-----------------------------------+")
                    print
                    print exsh.clicmd(show1, capture=True)
                    print
                    print
                    print ("+-----------------------------------+")
                    print ("|         ACL COUNTER               |")
                    print ("+-----------------------------------+")
                    print
                    print exsh.clicmd(show2, capture=True)
                    print
                    print
                    print ("Commands used to apply ACL:")
                    print cmd1
                    print cmd2

                else:
                    print ("Error applying ACL check for free slices")
            else:
                print ("Error creating ACL check ACL name")

        elif acl_data['L2_L3'] == 'l3':

            cmd1 = "create access-list %s \"%s%s%s\" \"count %s\"" % (
                acl_data['acl_name'], acl_data['protocol'], acl_data['src_ip'], acl_data['dst_ip'], acl_data['acl_name'])
            cmd2 = "configure access-list add %s first ports %s %s" % (acl_data['acl_name'], acl_data['interface'], acl_data['egress'])

            cmd1ex = exsh.clicmd(cmd1, capture=True)

            if cmd1ex == "":
                cmd2ex = exsh.clicmd(cmd2, capture=True)
                if 'done' in cmd2ex:
                    print ("     L3 ACL applied correctly")
                    print ("+-----------------------------------+")
                    print ("|               ACL                 |")
                    print ("+-----------------------------------+")
                    print
                    print exsh.clicmd(show1, capture=True)
                    print
                    print
                    print ("+------------------------------------------+")
                    print ("|               ACL COUNTER                |")
                    print ("+------------------------------------------+")
                    print
                    print exsh.clicmd(show2, capture=True)
                    print
                    print
                    print ("Commands used to apply ACL:")
                    print cmd1
                    print cmd2
                else:
                    print ("Error applying ACL check for free slices")
            else:
                print ("Error creating ACL check ACL name")
    except RuntimeError as cmdMsg:
        print
        print ("Error: Applying ACL.  Check for free slices, and if switch supports Egress ACL's if using -e")


def main():
    """
    The main function is used to prevent the script from exiting the EXOS session when quitting.
    It kicks off the script by calling acl_maker if ACL maker returns False, an error is shown,
    if else the acl_apply is called.
    """

    print
    acl_data = acl_maker()
    if not acl_data:
        print
        print ("#################################")
        print ("######## Error in syntax ########")
        print ("######## See help below #########")
        print ("#################################")
        print
        print ("Examples:")
        print ("run script flowtrack.py -sm 11-11-11-11-11-11 -dm 11-11-11-11-11-11  -p icmp -i 22")
        print ("run script flowtrack.py -dm 11-11-11-11-11-11 -i 22")
        print ("run script flowtrack.py -sip 4.4.4.4 -dip 2.2.2.2 -i 22")
        print ("run script flowtrack.py -sip 4.4.4.4 -p icmp -i 22")
        print ("run script flowtrack.py -sip 4.4.4.4 -p icmp -i 1-10,15")
        print
        print exsh.clicmd('run script flowtrack.py -h', capture=True)
    else:
        print
        print
        acl_apply(acl_data)
        print


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass
