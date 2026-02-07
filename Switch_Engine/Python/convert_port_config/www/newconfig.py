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
    return footer


def intport(port):
    if ":" in port:
        global Slots
        Slots=True
        modport = port.split(':')
        iport = modport[0].zfill(2)+":"+modport[1].zfill(2)
        return iport
    else:
        return port.zfill(2)

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
    config = form["config"].value
    portreplacement = {}
    slotreplacement = {}
    sharingports = {}
    if "commentout" in form.keys():
        OldLines = True
    else:
        OldLines = False
   
    print "<PRE>"
    for val in form:
        if val[0:5] == "port_":
            nport = str(form[val].value)
            if ":" in nport:
                modport = nport.split(":")
                realport = str(int(modport[0]))+":"+str(int(modport[1]))
            else:
                realport = str(int(nport))
            portreplacement[val[5:]] = realport

        if val[0:5] == "slot_":
            slotreplacement[int(val[5:])] = str(form[val].value)

        if val[0:8] == "sharing_":
            sharingports[val[8:]] = form[val].value

    for line in config.splitlines():
        newline = "not yet"
        slt = re.search(r'configure slot (\d+) module.*',line)
        if slt:
            try:
                if len(slotreplacement[int(slt.group(1))]) > 0 :
                    newline = re.sub(r'module\s.*','module '+slotreplacement[int(slt.group(1))],line)
                elif OldLines:
                    newline = "# "+line
                else:
                    newline = ""
            except:
                if OldLines:
                    newline = "# "+line
                else:
                    newline = ""

        vport = re.search(r'configure\sv[l|m]an\s\S+\sadd\sports\s(\S+)\s.*',line)
        if vport:
             if intport(vport.group(1)) in portreplacement.keys():
                 newline = line.replace(vport.group(1),portreplacement[intport(vport.group(1))],1)
             elif OldLines:
                 newline = "# "+line
             else:
                 newline = ""

        m = re.search(r'configure\sports\s(\S+)\s.*',line)
        if m:
            if intport(m.group(1)) in portreplacement.keys():
                 newline = line.replace(m.group(1),portreplacement[intport(m.group(1))],1)
            elif OldLines:
                 newline = "# "+line
            else:
                 newline = ""

        m = re.search(r'configure\seaps\s(\S+)\s(primary|secondary)\sport\s(.*)',line)
        if m:
            if intport(m.group(3)) in portreplacement.keys():
                newline = line.replace(m.group(3),portreplacement[intport(m.group(3))],1)
            elif OldLines:
                newline = "# "+line
            else:
                newline = ""

        m = re.search(r'(create|configure)\seaps\sshared-port\s([0-9|:]+).*',line)
        if m:
            if intport(m.group(2)) in portreplacement.keys():
                newline = line.replace(m.group(2),portreplacement[intport(m.group(2))],1)
            elif OldLines:
                newline = "# "+line
            else:
                newline = ""

        m = re.search(r'enable sharing ([0-9|:]+) grouping ([0-9|:|,|\-| ]+)\s(.*)',line)
        if m:
            iport = intport(m.group(1))
            if iport in portreplacement.keys():
                nwline = "enable sharing "+portreplacement[iport] + " grouping " 
                alg = ""
                for prt in sharingports[iport].split(";"):
                    if ":" in prt or prt.isdigit():
                        if intport(prt) in portreplacement.keys():
                            nwline += portreplacement[intport(prt)]+","
                    elif len(alg)==0:
                        alg = prt
                newline = nwline.rstrip(",") + " " + alg
            elif OldLines:
                newline = "# "+line
            else:
                newline = ""
             

        m = re.search(r'(enable|disable)\s\S+\sports?\s(\S+).*',line)
        if m and newline is "not yet":
            if intport(m.group(2)) in portreplacement.keys():
                newline = line.replace(m.group(2),portreplacement[intport(m.group(2))],1)
            elif OldLines:
                newline = "# "+line
            else:
                newline = ""


        if newline is "not yet":
            lastTry = m = re.search(r'.*\sports?\s([0-9|:|,|\-| ]+).*',line)
            if lastTry:
                newline = ""
                for prt in splitports(lastTry.group(1)):
                    if intport(prt) in portreplacement.keys():
                        newline += line.replace(lastTry.group(1),portreplacement[intport(prt)]+" ",1) +" \n"
            else:
                newline = line
     
        if not re.match(r'^\s*$', newline):
            print newline

    print "</PRE></BODY></HTML>"


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass

