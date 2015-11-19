import argparse
import re

def chk_port(port):
    if re.search('\d{1,2}',port):
        return True
    elif re.search('\d{1,2}:\d{1,2}',port):
        return True
    else:
        return False

def getvlans(port):
    cmd = "show port "+port+" info detail"
    vlaninfo = exsh.clicmd(cmd,capture=True)
    vlans=[]
    for line in vlaninfo.splitlines():
        m = re.search('\s+Name:\s(\S+),\s(\S+)\sTag\s=\s.*',line)
        if m:
            if m.group(2) == "Internal":
                tagged = "untagged"
            else:
                tagged = "tagged"
            vlans.append(m.group(1)+","+tagged)
    return vlans

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",dest="sourceport",default="none", required=False, help="Port to copy from")
    parser.add_argument("-d",dest="destport",default="none", required=False, help="Port to copy to")
    args = parser.parse_args()

    sourceport = args.sourceport
    destport = args.destport

    if chk_port(sourceport) and chk_port(sourceport):
        exsh.clicmd("disable clipaging",capture=False)
        vlans = getvlans(sourceport)
        for vlan in vlans:
            vpif = vlan.split(",")
            # Intentionally left out keyword vlan/vman so we can add vlan and vman with same command
            cmd = "configure "+vpif[0]+" add port "+destport+" "+vpif[1]
            exsh.clicmd(cmd,capture=True)
        delsrcport = raw_input("Do you want to delete all vlans from port "+sourceport+" (y/N) ? ")     
        if delsrcport == "Y" or delsrcport == "y":                                                      
            print "Deleting vlans from port "+sourceport+"."                                            
            for vlan in vlans:                                                                          
                vpif = vlan.split(",")                                                                  
                # Intentionally left out keyword vlan/vman so we can add vlan and vman with same command
                cmd = "configure "+vpif[0]+" del port "+sourceport
                exsh.clicmd(cmd,capture=True)       

    else:
        print "No ports or wrong port format given!"


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
