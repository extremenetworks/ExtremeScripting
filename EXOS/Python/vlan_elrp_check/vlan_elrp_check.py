'''
This Python Script will run elrp on every configured VLAN on the switch.  If you have > 20 of VLANs this script will ask if you want to run as it can take a long time
Please use caution when running this script.

'''
#This function is is used to break cli output into a list of dictionary for easy parsing.
import exsh

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

#this is the main function of the script.  It checks to see if there are more that 20 vlans configured.
#It also will call other functions to start the elrp script
def start_elrp_script():
    answer = ("")
    if  len(get_vlans()) > 20:
        print (f"Are you sure you want to run elrp on {len(get_vlans())} VLANs?")
        answer = input("y/n: ").lower()

        if answer == 'y':
            print("continuing")
            Run_ELRP()

        elif answer == 'n':
            print
            print (f"Script Canceled, ending elrp status is: {check_elrp_stat()}")
            print
            print
        elif answer != 'y' and answer != 'n':
            print
            print ("Please select 'y' for Yes and 'n' for No")
            print
            print
            start_elrp_script()
    else:
        Run_ELRP()

#defining a function to check if ELRP is Enabled or not
def check_elrp_stat():
    elrp_status = cmd2data('show elrp')
    elrp_status =  elrp_status[0]['elrpGlobalCfg']['enable']
    if elrp_status == 1:
        return 'Enabled'
    else:
        return 'Disabled'

#defining function that gets all vlans and places them into a table
def get_vlans():
    ##Getting the data needed for vlans and creating a blank table to put them.
    show = cmd2data('show vlan')
    number_of_lines = len(show)
    vlan_table = []

    #scraping output for vlan's and appending them to the "vlan_table"
    for line in show:
        vlan_name = line['vlanProc']['name1']
        vlan_table.append(vlan_name)
    return vlan_table

#Runs ELRP on all vlans found in get_vlans function
def Run_ELRP():
    #saving the start value of elrp
    elrp_start_value = check_elrp_stat()

    #Making sure ELRP is Enabled
    if check_elrp_stat() == 'Enabled':
        print
        print
        print ("**************************")
        print ("* ELRP is already Enabled*")
        print ("**************************")
        print
        print
    else:
        (exsh.clicmd('enable elrp', True))
        print
        print
        print ("*************************************")
        print ("* ELRP has been temporarily Enabled *")
        print ("*************************************")
        print
        print

    #Running ELRP using the get_vlans function to get a table list of vlans
    for vlan in get_vlans():
        print (f"Running ELRP on VLAN {vlan}.")
        elrp_output = (exsh.clicmd(f"configure elrp-client one-shot {vlan} ports all print", True))
        print (elrp_output)
        print
        print


    #print elrp_status and disable ELRP if needed

    if elrp_start_value == 'Enabled':
        print ("********************")
        print ("*No clean up needed*")
        print ("********************")
        print (f"Ending status of ELRP is: {check_elrp_stat()}")
    else:
        print ("**************")
        print ("*Cleaning up!*")
        print ("**************")
        (exsh.clicmd('disable elrp', True))
        print (f"Ending status of ELRP is: {check_elrp_stat()}")

start_elrp_script()
