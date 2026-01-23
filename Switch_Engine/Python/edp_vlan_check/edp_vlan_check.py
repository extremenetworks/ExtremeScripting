'''
This script uses EDP and the port configuration to see if the same vlans exist on both sides of the link.  Make sure EDP is enabled

Made By: Stephen Williams

'''
#this is used to convert cli command to XML data from exos and return a a table of dictionary's
def cmd2data(clicmd):
    import re
    import xml.etree.cElementTree as ElementTree
    re_reply = re.compile(r'<reply>.+?</reply>', re.DOTALL)
    xmlout = exsh.clicmd(clicmd, capture=False, xml=True)
    data = []
    for reply in re.finditer(re_reply, xmlout):
        if reply:
            reply_xml = reply.group()
            root = ElementTree.fromstring(reply_xml)
            for message in root.iter('message'):
                for element in message:
                    mdata = {}
                    edata = {}
                    for e in element:
                        text = int(e.text) if e.text is not None and e.text.isdigit() else e.text
                        edata[e.tag] = text
                    mdata[element.tag] = edata
                    data.append(mdata)
    return data



# this uses function cmd2data to create a table of configured vlans on the user selected port
def check_port_vlans(port):
    data = cmd2data('show port %s info det' % (port))
    port_vlan_list = []

    for line in data:
        vlan_table = 'show_ports_info_detail_vlans' in line

        if vlan_table == True:
            onevlan = line['show_ports_info_detail_vlans']['vlanName']
            port_vlan_list.append(onevlan)

    return port_vlan_list

# this uses function cmd2data to create a table of configured vlans on the remote port found by EDP
def check_edp_vlans(port):
    data = cmd2data('show edp ports %s detail' % (port))
    edp_vlan_list = []
    for line in data:
        edp_vlan_line = 'edpNbrVlan' in line
        if edp_vlan_line == True:
            one_edp_vlan = line['edpNbrVlan']['name']
            edp_vlan_list.append(one_edp_vlan)
        remoteport = 'edpNbr' in line
        if remoteport == True:
            rmtport =  ("{0}:{1}").format(line['edpNbr']['remoteSlot'], line['edpNbr']['nbrPort'])

    return edp_vlan_list, rmtport


"""
port_check runs the EXOS command "debug cfgmgr show next vlan.show_ports_info portList=* port=None"
then it checks to see if 'ERROR' is in the table.  If it is the function returns false.  If not returns true.
"""	
def port_check(port):
    import json
    port = port.replace(" ", "")

    cmd = 'debug cfgmgr show next vlan.show_ports_info portList={0} port=None'.format(port)
    result = json.loads(exsh.clicmd(cmd, capture=True))

    result = result['data'][0]['status']

    if result == 'ERROR':
        return False
    else:
        return True



def main_func():
    #the rest of the code runs the functions check_edp_vlans and check_port_vlans 
    #ports = port_list()
    port = raw_input("What port would you like to check?: ")
    if  port_check(port):
        edp_vlans, rmtport = check_edp_vlans(port)
        port_vlans = check_port_vlans(port)
        print
        if sorted(edp_vlans) != sorted(port_vlans):
            print ("Local port {0} and/or remote port {1} configurations do NOT match!!!").format(port, rmtport)  
            print
            diff_remote = list(set(edp_vlans) - set(port_vlans))
            diff_local = list(set(port_vlans) - set(edp_vlans))
            if len(diff_remote) != 0:
                print ("Please add the below vlans to port {0}.").format(port)
                print sorted(diff_remote)
                print
            if len(diff_local) != 0:
                print ("Please add the below vlans to the remote port {0}.").format(rmtport)
                print sorted(diff_local)

        if sorted(edp_vlans) == sorted(port_vlans):
            print ("Local and remote port vlan configurations match.")   
    else:
            print
            print ("please pick a valid port")
            print
            main_func()
main_func()
