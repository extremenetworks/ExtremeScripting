import os

print
print ("Note: please only use the show configuration output for this script.")
print ("      Make sure the starting non stack configuration file is in the same folder as the python script")
print
#nonstack = 'test.txt'
nonstack = raw_input("what is the non stacking configuration file name? ")
newstack = ("stack_%s") % nonstack

'''
This section will check to see if your running the script on EXOS or not.
It does this by trying to run show version through the exsh.clicmd() function.
If the exsh.clicmd() function works it will save the file to /usr/local/cfg/.
if the exsh.clicmd() function fails it will save the config to the current working directory.
'''
try:
    exoscli = ''
    exoscli = exsh.clicmd('show version', capture=True) #function in exos to run "show version"
    if exoscli == '':
        newstack = ("stack_%s") % nonstack
    else:
        newstack = ("/usr/local/cfg/stack_%s") % nonstack
        nonstack = ("/usr/local/cfg/%s") % nonstack
    print
except:
    pass


'''
This function receives the ports in the configuration and changes them to stacking configured ports
and sends it back to the "for" loop
'''
def change_port(port):
    if port == '' or port == 'all' or port[-0] == '"': # no change on blank or all or port groups
        return port
    if ',' in port: # check for , for port list
        ports = []
        port = port.split(',') # split to table based on ,
        for index in port: # changes each port index by index
            port = '1:%s,' % index # adds 1: in front
            ports.append(port) # appends each group of ports.
        ports = "".join(ports) # puts the ports together
        ports = ports.rstrip(ports[-1:]) # removes the last ", "
        return ports

    else:
        ports = "1:%s" % port # non portlist catch, adds "1:" to each port
        return ports


'''
We try to open the file the user entered.
If file is not there the Script will quit
'''
def line_change(stackport, port, sline):
        f = open(("%s" % newstack), 'a') # opens the file
        sline[port] = stackport
        line = " ".join(sline) # removing the table so it looks like a command
        f.write("%s\n" % line) # writing the line to the new config file

'''
We try to open the file the user entered.
If file is not there the Script will quit
'''
def main():
    try:
        with open (("%s" % nonstack), "r") as myfile: # tries to open the "show config" output
            line_data=myfile.readlines() # makes the "show config" output into a table or lines
    except:
        print
        print("+---------------------------------------------+")
        print("| Unable to find configuration file specified |")
        print("+---------------------------------------------+")
        print
        quit()

    '''
    We try to delete the old stacking config that matched the file we plan to create.
    '''
    try:
        os.remove("%s" % newstack)
    except:
        pass
    print
    print ("The new stacking configuration will be saved as %s.") % newstack
    '''
    This loop is used to check the configuration file one line at a time and
    replace the ports with stacking ports 1:* into a new config file.
    '''
    for line in line_data:
        try:
            f = open(("%s" % newstack), 'a') # opens the file
            sline = line.split( ) # splits the line into a table

            #configure stpd s0 ports bpdu-restrict enable 10 recovery-timeout 6
            if ('stpd' in sline and 'enable' in sline) and ('edge-safeguard' or 'bpdu-restrict' in sline):
                port = sline.index(sline[6])
                stackport =  change_port(sline[6])
                line_change(stackport, port, sline)
                pass

            #configure stpd s0 add vlan <VLAN> ports 57 dot1d
            elif 'stpd' in sline and 'ports' in sline and 'add' in sline:
                port = sline.index(sline[-2])
                stackport =  change_port(sline[-2])
                line_change(stackport, port, sline)
                pass
            #configure stpd s0 ports mode dot1d 1
            elif 'stpd' in sline and 'ports' in sline:
                port = sline.index(sline[-1])
                stackport =  change_port(sline[-1])
                line_change(stackport, port, sline)
                pass
            #configure policy rule admin-profile port 5 mask <mask> port-string 1-10 storage-type volatile
            elif 'port-string' in sline:
                pi1 = sline.index('port') + 1
                pi2 = sline.index('port-string') + 1
                port1 = change_port(sline[pi1])
                port2 = change_port(sline[pi2])
                sline[pi1] = port1
                sline[pi2] = port2
                line = " ".join(sline) # removing the table so it looks like a command
                f.write("%s\n" % line) # writing the line to the new config file
                pass

            #configure lacp member-port 4 priority <port_priority>
            elif 'member-port' in sline:
                port =  sline.index('member-port') + 1 #finding index where the ports are
                stackport =  change_port(sline[port]) #calling function to change ports
                line_change(stackport, port, sline)
                pass

            #create mirror <mirror_name_li> to port-list 1-10 loopback-port 5
            elif 'mirror' in sline:
                if 'create' in sline and 'mirror' in sline and 'loopback-port' in sline and 'to' in sline:
                    port1 = change_port(sline[5])
                    port2 = change_port(sline[7])
                    sline[5] = port1
                    sline[7] = port2
                    line = " ".join(sline) # removing the table so it looks like a command
                    f.write("%s\n" % line) # writing the line to the new config file

                #enable mirror to port-list 1-10 loopback-port 5 remote-tag <rtag>
                elif 'enable' in sline and 'mirror' in sline and 'loopback-port' in sline:
                    port1 = change_port(sline[4])
                    port2 = change_port(sline[6])
                    sline[4] = port1
                    sline[6] = port2
                    line = " ".join(sline) # removing the table so it looks like a command
                    f.write("%s\n" % line) # writing the line to the new config file
                pass

            # If port-list is seen in the line.
            elif 'port-list' in sline:
                port =  sline.index('port-list') + 1 #finding index where the ports are
                stackport =  change_port(sline[port]) #calling function to change ports
                line_change(stackport, port, sline)
                pass

            #disable lldp ports 13, configure vlan default delete ports 1
            elif 'ports' in sline: # looking for "ports" in table
                port =  sline.index('ports') + 1 #finding index where the ports are
                stackport =  change_port(sline[port]) #calling function to change ports
                line_change(stackport, port, sline)
                pass

            #enable port 1, disable port 1-10
            elif 'port' in sline: # looking for "port" in table
                port =  sline.index('port') + 1 #finding index where the ports are
                stackport =  change_port(sline[port]) #calling function to change ports
                line_change(stackport, port, sline)
                pass

            #configure eaps shared-port 4 mode controller, configure eaps shared-port 4 mode partner
            elif 'shared-port' in sline:
                port =  sline.index('shared-port') + 1 #finding index where the ports are
                stackport =  change_port(sline[port]) #calling function to change ports
                line_change(stackport, port, sline)
                pass

            #configure sharing, enable sharing
            elif 'sharing' in sline:
                ##configure sharing 5 lacp activity-mode active
                if 'lacp' == sline[3]:
                    port = 2
                    stackport =  change_port(sline[port]) #calling function to change ports
                    stackport = change_port(sline[port])
                    line_change(stackport, port, sline)

                #configure sharing 5 minimum-active 4
                elif 'minimum-active' in sline:
                    port1 = change_port(sline[2])
                    sline[2] = port1
                    line = " ".join(sline) # removing the table so it looks like a command
                    f.write("%s\n" % line) # writing the line to the new config file

                #enable sharing 5 grouping 1-10
                else:
                    sharing = change_port(sline[2])
                    grouping = change_port(sline[4])
                    sline[2] = sharing
                    sline[4] = grouping
                    line = " ".join(sline) # removing the table so it looks like a command
                    f.write("%s\n" % line) # writing the line to the new config file
                    pass
                pass

            #configure netlogin dynamic-vlan uplink-ports 1-10
            elif 'uplink-ports' in sline:
                port =  sline.index('uplink-ports') + 1 #finding index where the ports are
                stackport =  change_port(sline[port]) #calling function to change ports
                line_change(stackport, port, sline)
                pass
            else:
                f.write("%s" % line) # catch all when port not in the line

        except: # catch when a port is at the end of the line
            f.write("%s" % line)
            pass
    f.close()
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        pass
