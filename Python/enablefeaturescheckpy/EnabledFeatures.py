#!/usr/bin/env python
'''
This script scans the output of 'show configuration detail' looking for specific
features.
Example output looks like:
RADIUS                : disabled
TACACS                : disabled
Access List(s)        : None Configured
BGP                   : disabled
Configuration logging : disabled
CLI scripting         : enabled
EAPS                  : disabled
EDP                   : disabled
ELRP                  : disabled
ELSM                  : disabled
Debug Mode            : disabled
ESRP                  : disabled
IPARP                 : enabled
IGMP Snooping         : enabled
MLD                   : disabled
MVR                   : disabled
MSDP                  : disabled
NetLogin              : disabled
OSPF                  : disabled
OSPFv3                : disabled
PIM                   : disabled
RIP                   : disabled
RIPNG                 : disabled
IP route sharing      : enabled
SNMP                  : enabled
Spanning Tree         : disabled
Telnet                : enabled
Web mode HTTP         : enabled
Web mode HTTPS        : disabled
VLAN(s)               : created
VMAN(s)               : created
'''
def printStatus(feature, status):
    print '{0:<22s}: {1}'.format(feature, status)

string = exsh.clicmd('show configuration detail', True)
if (string.find("enable radius") != -1):
        printStatus("RADIUS","enabled")
else:
        printStatus("RADIUS","disabled")
if (string.find("enable tacacs") != -1):
        printStatus("TACACS","enabled")
else:
        printStatus("TACACS","disabled")

string2 = exsh.clicmd('show access-list', True)
if (string2.find("No entry found") != -1):
        printStatus("Access List(s)","None Configured")
else:
        printStatus("Access List(s)","configured")

if (string.find("enable bgp") != -1):
        printStatus("BGP","enabled")
else:
        printStatus("BGP","disabled")
if (string.find("enable cli-config-logging") != -1):
        printStatus("Configuration logging","enabled")
else:
        printStatus("Configuration logging","disabled")
if (string.find("enable cli scripting") != -1):
        printStatus("CLI scripting","enabled")
else:
        printStatus("CLI scripting","disabled")
if (string.find("enable eaps") != -1):
        printStatus("EAPS","enabled")
else:
        printStatus("EAPS","disabled")
if (string.find("enable edp") != -1):
        printStatus("EDP","enabled")
else:
        printStatus("EDP","disabled")
if (string.find("enable elrp") != -1):
        printStatus("ELRP","enabled")
else:
        printStatus("ELRP","disabled")
if (string.find("enable elsm") != -1):
        printStatus("ELSM","enabled")
else:
        printStatus("ELSM","disabled")
if (string.find("enable log debug-mode") != -1):
        printStatus("Debug Mode","enabled")
else:
        printStatus("Debug Mode","disabled")
if (string.find("enable esrp") != -1):
        printStatus("ESRP","enabled")
else:
        printStatus("ESRP","disabled")
if (string.find("enable iparp") != -1):
        printStatus("IPARP","enabled")
else:
        printStatus("IPARP","disabled")
if (string.find("enable igmp snooping") != -1):
        printStatus("IGMP Snooping","enabled")
else:
        printStatus("IGMP Snooping","disabled")
if (string.find("enable MLD vlan") != -1):
        printStatus("MLD","enabled")
else:
        printStatus("MLD","disabled")
if (string.find("enable mvr") != -1):
        printStatus("MVR","enabled")
else:
        printStatus("MVR","disabled")
if (string.find("enable msdp vr") != -1):
        printStatus("MSDP","enabled")
else:
        printStatus("MSDP","disabled")
if (string.find("enable netlogin ports") != -1):
        printStatus("NetLogin","enabled on port(s)")
else:
        printStatus("NetLogin","disabled")

if (string.find("enable ospf\n") != -1):
        printStatus("OSPF","enabled")
else:
        printStatus("OSPF","disabled")
if (string.find("enable ospfv3") != -1):
        printStatus("OSPFv3","enabled")
else:
        printStatus("OSPFv3","disabled")
if (string.find("enable pim") != -1):
        printStatus("PIM","enabled")
else:
        printStatus("PIM","disabled")
if (string.find("enable rip\n") != -1):
        printStatus("RIP","enabled")
else:
        printStatus("RIP","disabled")
if (string.find("enable ripng") != -1):
        printStatus("RIPNG","enabled")
else:
        printStatus("RIPNG","disabled")
if (string.find("enable iproute") != -1):
        printStatus("IP route sharing","enabled")
else:
        printStatus("IP route sharing","disabled")
if (string.find("enable snmp") != -1):
        printStatus("SNMP","enabled")
else:
        printStatus("SNMP","disabled")
if (string.find("enable stp\n") != -1):
        printStatus("Spanning Tree","enabled")
else:
        printStatus("Spanning Tree","disabled")
if (string.find("enable telnet") != -1):
        printStatus("Telnet","enabled")
else:
        printStatus("Telnet","disabled")
if (string.find("disable web http\n") != -1):
        printStatus("Web mode HTTP","disabled")
else:
        printStatus("Web mode HTTP","enabled")
if (string.find("enable web https\n") != -1):
        printStatus("Web mode HTTPS","enabled")
else:
        printStatus("Web mode HTTPS","disabled")
if (string.find("create vlan") != -1):
        printStatus("VLAN(s)","created")
else:
        printStatus("VLAN(s)","not created other than default and mgmt")
if (string.find("create vman") != -1):
        printStatus("VMAN(s)","created")
else:
        printStatus("VMAN(s)","not created")
