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

    return edp_vlan_list

#this function makes a list of all ports configures on the switch to check against the user input port.
def port_list():
    data = cmd2data('show port conf no')
    ports_table = []

    for line in data:
        port = line['show_ports_config']['port']
        ports_table.append(port)
    return ports_table




def main_func():
    #the rest of the code runs the functions check_edp_vlans and check_port_vlans 
    ports = port_list()
    port = raw_input("What port would you like to check?: ")
    n = 0 
#this value "n" is used to count how many ports that don't match the user input port  
#if "n" == how many ports configured on the switch the user did not enter a valid port.
    for line in ports:
        if  str(line) == port:
            #print ("works")
            edp_vlans = check_edp_vlans(port)
            edp_vlans = sorted(edp_vlans)
            port_vlans = check_port_vlans(port)
            print
            print
            print ('EDP VLAN data: %s' % sorted(edp_vlans))
            print ('VLANS on port: %s' % sorted(port_vlans))
            if sorted(edp_vlans) == sorted(port_vlans):
                print
                print ("They match!!!")
            else:
                print
                print ("No Match!!!")    
        else:
            n = n + 1
            if n == len(ports):
                print
                print ("please pick a valid port")
                print
                main_func()
main_func()
