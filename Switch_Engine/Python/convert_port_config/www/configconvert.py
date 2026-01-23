#!/usr/bin/env python

import cgi
import re
import cgitb
import collections
cgitb.enable()

def header():
    header = "Content-Type: text/html;charset=utf-8"
    header += "\n"
    header += "\n"
    header += "<HTML>"
    header += "<HEAD><TITLE>Port Config Converter</TITLE>"
    header += "<script src=\"jquery.min.js\"></script>"
    header += "<script src=\"scroll.js\"></script>"
    header += "</HEAD>"
    header += "<BODY>"

    return header

def footer():
    footer = "<div id=\"footer\">"
    footer += "Problems with this tool? <a href=\"https://github.com/extremenetworks/ExtremeScripting/issues\" target=\"_blank\">Create a new issue on GitHub</a>."
    footer += "</div></BODY></HTML>"
    return footer

def addport(port):
        global features
        if port not in ports_used.keys():
            ports_used[port] = 1
        else:
            ports_used[port] += 1
        if port not in features.keys():
            features[port] = ""


def addfeature(port,feature):
    global features
    if port in features.keys():
        if feature not in features[port]:
            features[port] += feature
    else:
        features[port] = feature

def Feature_icons(port):
    ret = ""
    global features
    global MouseOver
    for feat in features[port].split(","):
        if len(feat) > 1:
            ret += "<IMG SRC=\"icon/"+feat.upper()+".png\" TITLE=\""+MouseOver[feat.upper()]+"\">"
    return ret

def intport(port):
    if ":" in port:
        global Slots
        Slots=True
        modport = port.split(':')
        iport = modport[0].zfill(2)+":"+modport[1].zfill(2)
        return iport
    else:
        return port.zfill(2)

def real_port(port):
    if ":" in port:
        modport = port.split(':')
        return str(int(modport[0]))+":"+str(int(modport[1]))
    else:
        return str(int(port))

def splitports(portlist):
    ports = re.sub('[^0123456789:,-]','',portlist).rstrip("-")
    portsreturn = []
    if ":" in ports:
        for prt in ports.split(','):
            if prt.count('-') == 0:
                portsreturn.append(prt)
            else:
                modport = prt.split(':')
                prts = modport[1].split('-')
                startport = int(prts[0])
                endport = int(prts[1])
                while startport <= endport:
                   portsreturn.append(modport[0]+":"+str(startport))
                   startport += 1
    else:
        for prt in ports.split(','):
            if prt.count('-') == 0:
                portsreturn.append(prt)
            else:
                prts = prt.split('-')
                startport = int(prts[0])
                endport = int(prts[1])
                while startport <= endport:
                    portsreturn.append(str(startport))
                    startport += 1
    return portsreturn

def main():
    print header()
    form = cgi.FieldStorage()
    if "use_original_ports" in form.keys():
        orgports = True
    else:
        orgports = False

    if form['file'].filename:
        config = form['file'].file.read().replace('\n\n', '\n')
    elif len(form["config"].value) > 20:
        config = form["config"].value.replace('\n\n', '\n')

    if config:
        global ports_used
        global features
        global Slots
        global MouseOver
        Slots=False
        features = {}
        MouseOver = {}
        MouseOver['RTLMT'] = "Rate-limit flood"
        MouseOver['MIR'] = "Mirror to port"
        MouseOver['ACL'] = "Access-list"
        MouseOver['MLAG'] = "MLAG port"
        MouseOver['LAG'] = "LAG port"
        MouseOver['EAPS'] = "EAPS port"
        MouseOver['ERPS'] = "ERPS port"
        MouseOver['STP'] = "STP port"
        MouseOver['CDP'] = "CDP enabled"
        MouseOver['IDMGR'] = "Identity-management enabled"
        MouseOver['LLDP'] = "LLDP enabled"
        MouseOver['NLOGIN'] = "Netlogin port"
        ports_used = {}
        sharingports={}
        newconfig=""
        modules={}
        
        
        for line in config.splitlines():
            vtag = re.search(r'(configure\sv[l|m]an\s\S+\sadd\sports\s)(.*)(\stagged.*)',line)
            vuntag = re.search(r'(configure\sv[l|m]an\s\S+\sadd\sports\s)(.*)(\suntagged.*)',line)
            vpvlan = re.search(r'(configure\sv[l|m]an\s\S+\sadd\sports\s)(.*)(\sprivate-vlan.*)',line)
            vcep = re.search(r'(configure\sv[l|m]an\s\S+\sadd\sports\s)(.*)(\scep.*)',line)
            vl = re.search(r'(configure\sv[l|m]an\s\S+\sadd\sports\s)(.*)',line)
            portlist = None
            cmdline = None
            if vtag:
                portlist = vtag.group(2)
                cmdline = vtag.group(1) +"portlistword"+vtag.group(3)
            elif vuntag:
                portlist = vuntag.group(2)
                cmdline = vuntag.group(1) +"portlistword"+vuntag.group(3)
            elif vpvlan:
                portlist = vpvlan.group(2)
                cmdline = vpvlan.group(1) +"portlistword"+vpvlan.group(3)
            elif vcep:
                portlist = vcep.group(2)
                cmdline = vcep.group(1) +"portlistword"+vcep.group(3)
            elif vl:
                portlist = vl.group(2)
                cmdline = vl.group(1) +"portlistword"

            if portlist and cmdline:
                ports = splitports(portlist)
                for port in ports:
                    addport(intport(port))
                    newconfig+=re.sub(r'portlistword',port,cmdline)+"\n"
            else:
                mod = re.search(r'configure\sslot\s(\d+)\smodule\s(\S+)',line)
                if mod:
                    modules[mod.group(1)] = mod.group(2)
                eaps = re.search(r'configure\seaps\s\S+\s(primary|secondary)\sport\s(\S+)',line)
                if eaps:
                    addfeature(intport(eaps.group(2)),"EAPS,")

                eaps = re.search(r'configure\serps\s\S+\s(\S+\-port)\s(east\s|west\s|)([0-9|:]+)',line)
                if eaps:
                    addfeature(intport(eaps.group(3)),"ERPS,")

                stp = re.search(r'configure\sstpd\s\S+\sadd\svlan.*\sports\s([0-9|:]+).*',line)
                if stp:
                    addfeature(intport(stp.group(1)),"STP,")

                nlogin = re.search(r'enable\snetlogin\sports\s([0-9|:]+).*',line)
                if nlogin:
                    addfeature(intport(nlogin.group(1)),"NLOGIN,")

                rtlmt = re.search(r'config\S*\sport\s([0-9|:]+)\srate\-limit\sflood.*',line)
                if rtlmt:
                    addfeature(intport(rtlmt.group(1)),"RTLMT,")

                cdp = re.search(r'enable\scdp\sports\s([0-9|:]+).*',line)
                if cdp:
                    for port in splitports(cdp.group(1)):
                        iport = intport(port)
                        addfeature(intport(cdp.group(1)),"CDP,")

                lldp = re.search(r'enable\slldp\sports\s([0-9|:]+).*',line)
                if lldp:
                    for port in splitports(lldp.group(1)):
                        iport = intport(port)
                        addfeature(intport(lldp.group(1)),"LLDP,")

                mirror = re.search(r'configure\smirror\s\S+\sto\sport\s([0-9|:]+)',line)
                if mirror:
                    addport(intport(mirror.group(1)))
                    addfeature(intport(mirror.group(1)),"MIR,")

                idmgr = re.search(r'configure\sidentity-management\sadd\sports\s([0-9|:|,|\-| ]+)',line)
                if idmgr:
                    for port in splitports(idmgr.group(1)):
                        iport = intport(port)
                        addfeature(iport,"IdMgr,")
 
                acl = re.search(r'configure\saccess-list\s\S+\sports\s([0-9|:|,|\-| ]+)',line)
                if acl:
                    for port in splitports(acl.group(1)):
                        iport = intport(port)
                        addfeature(iport,"ACL,")
 
                mlag = re.search(r'enable\smlag\sport\s([0-9|:]+)',line)
                if mlag:
                    for port in splitports(mlag.group(1)):
                        iport = intport(port)
                        addfeature(iport,"MLAG,")

                sharing = re.search(r'enable sharing ([0-9|:]+) grouping ([0-9|:|,|\-| ]+)\s(.*)',line)
                if sharing:
                    masterport = intport(sharing.group(1))
                    sharingports[masterport] = []
                    for port in splitports(sharing.group(2)):
                        iport = intport(port)
                        sharingports[masterport].append(iport)
                        addfeature(iport,"LAG,")
                        addport(iport)
                    sharingports[masterport].append(sharing.group(3))
                newconfig+=line+"\n"


        print "<form action='newconfig.py' method='post'>"
        print "<input type='checkbox' name='commentout'>Leave original lines in but comment out<br>"

 
        if Slots:
            print "<table><TR><TH>slot</TH><TH>Module</TH><TH>New module</TH></TR>"
            for slot in sorted(modules):
                print "<TR><TD>"+slot+"</TD><TD>"+modules[slot]+"</TD>"
                print "<TD><INPUT NAME=\"slot_"+slot+"\" value=\""+modules[slot]+"\"></TD></TR>\n"
            print "</TABLE>"


        print "<table><TR><TH>Port</TH><TH>Sharing</TH><TH>#vlans</TH><TH>Features</TH><TH>New port</TH></TR>"
        for port in sorted(ports_used):
            realport = real_port(port)
            print "<TR valign='top'><TD>"+realport+"</TD>"

            print "<TD>"
            Masterport = False
            for master, member in sharingports.iteritems():
                if port in member:
                    for prt in member:
                        if re.match(r'[[0-9|:]+', prt):
                            print real_port(prt)+"<br>"
                    Masterport = master
            print "</TD>"

            if Masterport:
                print "<TD>"+str(ports_used[Masterport])+"</TD>"
                print "<TD>"+Feature_icons(Masterport)+"</TD>"
            else:
                print "<TD>"+str(ports_used[port])+"</TD>"
                print "<TD>"+Feature_icons(port)+"</TD>"
            print "<TD><INPUT NAME=\"port_"+port+"\" "
            if orgports:
                print " VALUE=\""+realport+"\""
            print "></TD></TR>\n"
        
        print "</TABLE>\n"
        
        print "<INPUT TYPE='hidden' name='config' VALUE='"+newconfig+"'>"   

        for masport in sharingports:
            shline = "<input type='hidden' name='sharing_"+masport+"' value='"
            for memport in sharingports[masport]:
                shline += memport+";"
            print shline + "'>\n"
        print "<INPUT TYPE='submit'></FORM>"   
        

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass

