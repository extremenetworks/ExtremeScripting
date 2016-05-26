#!/usr/bin/env python
# Version 1.0

import sys
import re
import argparse


def checkIP(IP):
    m = re.search(r'\d+\.\d+\.\d+\.\d+',IP)
    if m:
        return True
    else:
        return False

def wildcardTOmask(IP):
    parts = IP.split(".")
    bin1 = bin(int(parts[0]))[2:]
    bin2 = bin(int(parts[1]))[2:]
    bin3 = bin(int(parts[2]))[2:]
    bin4 = bin(int(parts[3]))[2:]
    ones = bin1.count("1")
    ones += bin2.count("1")
    ones += bin3.count("1")
    ones += bin4.count("1")
    return str(32-ones)

def IPstringDecode(prts):
    if prts[0] == "any":
        retstring = "0.0.0.0/0;"
        used = 1
    elif checkIP(prts[0]):
        srcmask = wildcardTOmask(prts[1])
        retstring = prts[0]+"/"+srcmask+";"
        used = 2
    elif prts[0] == "host" and checkIP(prts[1]):
        retstring = prts[1]+"/32;"
        used = 2
    return [retstring,used]

def PortDecode(prts):
    if prts[0] == "eq":
        retstring = prts[1]+";"
        used = 2
    if prts[0] == "range":
        retstring = prts[1]+" "+prts[2]+";"
        used = 3
    return [retstring,used]



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file containing Cisco ACL")
    args = parser.parse_args()
    out = ""
    rule = 0
    protocol = {}
    protocol["ahp"] = "51";
    protocol["eigrp"] = "88";
    protocol["esp"] = "50";
    protocol["gre"] = "47";
    protocol["ipinip"] = "94";
    protocol["nos"] = "47";
    protocol["object-group"] = "53";
    protocol["ospf"] = "89";
    protocol["pcp"] = "108";
    protocol["pim"] = "103";
    protocol["tcp"] = "tcp";
    protocol["udp"] = "udp";

    if args.file:
        filename = args.file.split(".")
        ACLname = filename[0]
        f = open(args.file,'r')
        for line in f: 
            action = ""
            parts = line.lstrip().rstrip().split()
            m = re.search(r'\s*ip\saccess-list\s[extended]*\s(\S+)',line)
            if m:
                if len(out) > 1:
                    f = open(ACLname+".pol",'w')
                    f.write(out)
                    f.close()
                    print "ACL is saved to "+ACLname+".pol\n"
                ACLname = m.group(1)
                out = ""
            elif len(parts) > 0 and parts[0] == "remark":
                out += "@"
                for prt in parts:
                    out += prt
                out += "\n"
            elif len(parts) > 3:
                try:
                    rule += 1
                    out += "entry "+filename[0]+"_"
                    if parts[0] == "permit":
                        out += "permit"+str(rule)+" { if {"
                        action = "permit"
                    elif parts[0] == "deny":
                        out += "deny"+str(rule)+" { if {"
                        action = "deny"
                
                    if parts[1] in protocol.keys():
                        out += " protocol "+protocol[parts[1]]+";"
                    elif parts[1].isdigit():
                        out += " protocol "+parts[1]+";"
   
                    srcIP = IPstringDecode(parts[2:])
                    out += " source-address "+srcIP[0]
                
                    next = 2 + srcIP[1]
                    if parts[next] == "eq" or parts[next] == "range":
                        srcport = PortDecode(parts[next:])
                        out += " source-port "+srcport[0]
                        next += srcport[1]
                

                    #Destination
                    dstIP = IPstringDecode(parts[next:])
                    out += " destination-address "+dstIP[0]
            
                    next += dstIP[1]
            
                    if len(parts) > next:
                        if parts[next] == "eq" or parts[next] == "range":
                            dstport = PortDecode(parts[next:])
                            out += " destination-port "+dstport[0]

                    out+= "} then { "+action+";}}\n"

                except:
                    out+= "  ERROR! \n"

        f.close()
        if len(out) > 1:
            f = open(ACLname+".pol",'w')
            f.write(out)
            f.close()
            print "ACL is saved to "+ACLname+".pol\n"
 
                
    
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass