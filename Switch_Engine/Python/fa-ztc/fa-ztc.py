##########################################################
# XOS Python Script: FA-ZTC                              #
# Written by Ludovico Stevens, CSE Extreme Networks      #
##########################################################
# Implement Fabric Attach Zero-Touch-Client on XOS

__version__ = '1.0'

# To do:
# - make i-sid optional
# - ztc qos and keep-vlan
# - fa custom client

#
# Imports
#
from os import path
import re
import sys
import exsh
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

#
# Global Variables
#
Debug = False
ThisMod = __file__.split(path.sep)[-1].split('.')[0]    # Name of this module
VlanNamePrefix = 'ZTC_VLAN_' # Appended to VLAN-id for ZTC configured VLANs
FaClientTypes = { # These are the client types which are allowed in ZTC config
    'wap-type1'      : 6,
    'wap-type2'      : 7,
    'switch'         : 8,
    'router'         : 9,
    'phone'          : 10,
    'camera'         : 11,
    'video'          : 12,
    'security-device': 13,
    'virtual-switch' : 14,
    'srvr-endpt'     : 15,
    'ona-sdn'        : 16,
    'ona-spb-over-ip': 17,
}
FaElementTypes = { # Exhaustive list of FA Element types (lookup by id)
    1: 'type-other',
    2: 'server',
    3: 'proxy',
    4: 'server-noauth',
    5: 'proxy-noauth',
    6: 'wap-type1',
    7: 'wap-type2',
    8: 'switch',
    9: 'router',
   10: 'phone',
   11: 'camera',
   12: 'video',
   13: 'security-device',
   14: 'virtual-switch',
   15: 'srvr-endpt',
   16: 'ona-sdn',
   17: 'ona-spb-over-ip',
}
FaConfigFile = '/usr/local/cfg/.{0}/{0}.json'.format(ThisMod)
RegexPort = re.compile('^(?:[1-9]\d?:)?[1-9]\d?$')
RegexPortRange = re.compile('^([1-9]\d?)-([1-9]\d?)$')
RegexSlotPortRange = re.compile('^([1-9]\d?):([1-9]\d?)-([1-9]\d?)$')
RegexSlotStarRange = re.compile('^([1-9]\d?):\*$')
RegexSlotSlotRange = re.compile('^([1-9]\d?):([1-9]\d?)-([1-9]\d?):([1-9]\d?)$')
Command = ['ports', 'add', 'remove', 'show']

#
# Functions
#
def debug(debugOutput): # Use to include debugging in script; set above Debug variable to True or False to turn on or off debugging
    if Debug: print debugOutput


def printSyntax():
    def clientValue(elem): # Function to sort client types by their value
        return FaClientTypes[elem]
    clientTypes = sorted(FaClientTypes, key=clientValue)
    print "Fabric-Attach Zero-Touch-Client ({} version {})".format(ThisMod, __version__)
    print "=" * 52
    print "Usage:"
    print " {} ports <port-list|none|all>              : Set ports where to detect ztc clients".format(ThisMod)
    print " {} add <client-type> <vlan-id> <i-sid>     : Add vlan/i-sid binding for client type".format(ThisMod)
    print " {} remove <client-type>                    : Remove binding for client type".format(ThisMod)
    print " {} show                                    : Show ztc configuration".format(ThisMod)
    print
    print " <client-type>        : {}".format(','.join(clientTypes[:7]))
    print "                        {}".format(','.join(clientTypes[7:]))


def cliCmd(cmd, arg=None, fmt=None): # Send a command, with optional args; fmt = None|raw|xml
    if fmt == 'xml':
        captFlag = False
        xmlFlag = True
    elif fmt == 'raw':
        captFlag = True
        xmlFlag = False
    else:
        captFlag = False
        xmlFlag = False
    try:
        output = exsh.clicmd(cmd, args=arg, capture=captFlag, xml=xmlFlag)
        debug("cliCmd -> {}".format(cmd))

    except RuntimeError as detail:
        print "RuntimeError:", detail
        print "Unable to execute CLI command '{}'".format(cmd)
        if arg: print " with arguments '{}'".foramt(arg)
        sys.exit(1)

    if fmt == 'xml':
        # because exsh.clicmd returns malformed XML
        output = '<xmldata>' + output + '</xmldata>'

    return output


def writeZtcConfig(cfgDict): # Writes config to fa-ztc.json file
    # Format of ZtcConfig JSON file:
    #{
    #   "ports": "1:1-2:54", # Ports where ZTC enabled
    #   "client": { # ZTC client config
    #      "<fa-client>": {
    #         "isid": <isid>,
    #         "vlan": <vlan>
    #      },
    #   },
    #   "port": { # Used to reverse VLAN config on port upon device-undetect
    #      "<port>": {
    #         "client" : "<fa-client#>",
    #         "add": {
    #            "untagged": [<vlan-id-list-added-to-port>],
    #            "tagged":   [<vlan-id-list-added-to-port>]
    #         },
    #         "del": {
    #            "untagged": [<vlan-id-list-removed-from-port>],
    #            "tagged":   [<vlan-id-list-removed-from-port>]
    #         },
    #      },
    #   },
    #   "vlan": { # Used to reverse VLAN creation upon device-undetect
    #      "<vlan-id>": 1,
    #   },
    #   "isid": { # Used to remove I-SID from VLAN (where VLAN already existed without I-SID) upon device-undetect
    #      "<isid>": 1,
    #   },
    #   "debug": 1,
    #}
    try:
        json.dump(cfgDict, fp=open(FaConfigFile, 'w'), indent=3)
        debug("writeZtcConfig -> {}".format(FaConfigFile))
    except IOError as detail:
        print 'IOError:', detail
        print 'Unable to write config file: {}'.format(FaConfigFile)
        sys.exit(1)


def readZtcConfig(): # Reads fa-ztc.json file to obtain config 
    try:
        cfgDict = json.load(open(FaConfigFile))
        debug("readZtcConfig -> {}".format(FaConfigFile))
    except IOError as detail:
        print 'IOError:', detail
        print 'Unable to read config file:', FaConfigFile
        sys.exit(1)
    except ValueError as detail:
        print 'ValueError:', detail
        print 'JSON error reading config file:', FaConfigFile
        sys.exit(1)
    if 'debug' in cfgDict.keys():
        global Debug
        Debug = cfgDict['debug']
    return cfgDict


def installFaZtc(cfgOverwrite): # Steps to hook the script in
    # Create a hidden directory; will be used to store json config file
    cliCmd('mkdir .{}'.format(ThisMod))

    if cfgOverwrite: # We create a new empty config file
        writeZtcConfig({'ports': None, 'client': {}, 'port': {}, 'vlan': {}, 'isid': {}, 'debug': Debug})
        debug("installFaZtc -> created clean ZTC config")

    # Create an alias to running this Python script
    # Aliases cannot be created for the current shell session using UPM scripts or Python scripts
    # So, we append it inside exshrc.xsf
    # Specify full file path as Python running on exos will otherwise default to directory /exos/bin
    aliasCmd = 'alias {0} "run script {0}.py"\n'.format(ThisMod)
    xsfFile = '/usr/local/cfg/exshrc.xsf'
    updateExshrc = True
    try:
        with file(xsfFile) as f:
            contents = f.read()
        if re.search(aliasCmd, contents): # Alias command is already in there
            updateExshrc = False
            debug("installFaZtc -> no need to update {}".format(xsfFile))
    except:
        pass
    if updateExshrc:
        try:
            with open(xsfFile, 'a') as myFile:
                myFile.write(aliasCmd)
            debug("installFaZtc -> updated {}".format(xsfFile))
        except IOError as detail:
            print 'IOError:', detail
            print 'Unable to append alias to xsf: {}'.format(xsfFile)
            sys.exit(1)

    # Create a xsf script file to get the UPM profile created (cannot do using exsh.clicmd with Python)
    # Specify full file path as Python running on exos will otherwise default to directory /exos/bin
    xsfFile = '/usr/local/cfg/{}.xsf'.format(ThisMod)
    try:
        with open(xsfFile, 'w') as myFile:
            myFile.write('create upm profile {}-detect\n'.format(ThisMod))
            myFile.write('run script {}.py upm-detect $EVENT.USER_PORT $EVENT.DEVICE_MAC\n'.format(ThisMod))
            myFile.write('.\n')
            myFile.write('create upm profile {}-undetect\n'.format(ThisMod))
            myFile.write('run script {}.py upm-undetect $EVENT.USER_PORT\n'.format(ThisMod))
            myFile.write('.\n')
        debug("installFaZtc -> created {}".format(xsfFile))
    except IOError as detail:
        print 'IOError:', detail
        print 'Unable to write UPM Profile xsf install script: {}'.format(xsfFile)
        sys.exit(1)

    # Create the UPM profile by running this xsf file
    cliCmd('run script {}.xsf'.format(ThisMod))
    # Delete the xsf file as will no longer be needed
    cliCmd('rm {}.xsf'.format(ThisMod))

    if not cfgOverwrite: # If we are using an existing config file...
        cfgDict = readZtcConfig()
        if cfgDict['ports']: # And it has ports defined..
            addFaPorts(cfgDict['ports'])
            plumbZtcClients(cfgDict, cfgDict['ports'])


def uninstallFaZtc(): # Steps to unhook the script
    # Remove the alias from exshrc.xsf
    aliasCmd = 'alias {0} "run script {0}.py"\n'.format(ThisMod)
    xsfFile = '/usr/local/cfg/exshrc.xsf'
    updateExshrc = False
    try:
        with file(xsfFile) as f:
            contents = f.read()
        updatedContents = re.sub(aliasCmd, '', contents) # Remove the alias command if there
        if updatedContents is not contents: # I.e. we did find it and so made a substitution..
            updateExshrc = True
            debug("uninstallFaZtc -> need to update {}".format(xsfFile))
    except:
        pass
    if updateExshrc:
        try:
            with open(xsfFile, 'w') as myFile:
                myFile.write(updatedContents)
            debug("uninstallFaZtc -> updated {}".format(xsfFile))
        except IOError as detail:
            print 'IOError:', detail
            print 'Unable to re-write contents to xsf: {}'.format(xsfFile)
            sys.exit(1)

    # Delete the UPM profile
    cliCmd('delete upm profile {}-detect'.format(ThisMod))
    cliCmd('delete upm profile {}-undetect'.format(ThisMod))


def checkAlreadyInstalled(): # Checks whether this script has already been added as a UPM profile
    xmlOutput = cliCmd('show upm profile', fmt='xml')
    if re.search(r'<!\[CDATA\['+ThisMod+'-(?:un)?detect\]\]>', xmlOutput): return True
    return False


def readXosVersion(): # Get the XOS software version from the switch
    cliOutput = cliCmd('show version', fmt='raw')
    matchObj = re.search(r'ExtremeXOS version ([\d\.]+)', cliOutput)
    debug("readXosVersion = {}".format(matchObj.group(1)))
    return matchObj.group(1)


def readExistingVlans(): # Obtains a list of VLANs currently configured on this switch with name and i-sid info
    xmlOutput = cliCmd('show vlan', fmt='xml')
    # this command does not seem to work on our X460-STK: debug cfgmgr show next vlan.vlanMap
    vlanDb = {}
    root = ET.fromstring(xmlOutput)
    for record in root.findall('.//vlanProc'):
        name = str(record.find('name1').text)
        tag = int(record.find('tag').text)
        vlanDb[tag] = {'name': name, 'isid': None}

    if re.match(r'^22\.|30\.1', readXosVersion()): # Old syntax
        xmlOutput = cliCmd('show vlan fabric attach mappings', fmt='xml')
    else: # New syntax
        xmlOutput = cliCmd('show fabric attach assignments', fmt='xml')
    # this command does not always return all bindings: debug cfgmgr show next lldp.faMapping
    # xml of cli command used provides some duplicate bindings.. but is safer
    root = ET.fromstring(xmlOutput)
    for record in root.findall('.//faMapping'):
        isid = int(record.find('nsi').text)
        tag = int(record.find('vlanId').text)
        vlanDb[tag]['isid'] = isid

    debug("readExistingVlans -> {}".format(vlanDb))
    return vlanDb


def lookupExistingIsids(vlanDb, isid): # If i-sid is present in vlanDb returns the corresponding vlan; else None
    for vlan in vlanDb.keys():
        if vlanDb[vlan]['isid'] == isid:
            return vlan
    return None


def readPortVlans(ports): # For the specified ports, obtains a data structure detailing which VLANs are assigned to the port as tagged and/or untagged
    xmlOutput = cliCmd('show port {} vlan'.format(ports), fmt='xml')
    portVlanDb = {}
    root = ET.fromstring(xmlOutput)
    for record in root.findall('.//show_ports_info_detail_vlans'):
        port = str(record.find('port').text)
        vlan = int(record.find('vlanId').text)
        tag = int(record.find('tagStatus').text)
        debug("readPortVlans -> port = {} / vlan = {} / tag = {}".format(port, vlan, tag))
        if port not in portVlanDb.keys():
            portVlanDb[port] = {'untagged': [], 'tagged': []}
        if tag: portVlanDb[port]['tagged'].append(vlan)
        else  : portVlanDb[port]['untagged'].append(vlan)

    debug("readPortVlans -> {}".format(portVlanDb))
    return portVlanDb


def readVlanMembers(vlan): # For the specified vlan, obtains a data structure listing all tagged and untagged ports
    cliLines = cliCmd('show vlan {}'.format(vlan), fmt='raw').splitlines()
    vlanMemberDb = {'untagged': [], 'tagged': []}
    section = None
    for line in cliLines:
        if re.match(r'^\s+Untag:', line):
            section = 'untagged'
            debug("readVlanMembers -> section = {}".format(section))
        elif re.match(r'^\s+Tag:', line):
            section = 'tagged'
            debug("readVlanMembers -> section = {}".format(section))
        elif re.match(r'^\s+Flags:', line):
            section = None
            debug("readVlanMembers -> section = {}".format(section))
        if section == None:
            continue
        line = re.sub(r'\([^\)]+\)', '', line) # wipe out the port names lest they might trigger false ports
        debug("readVlanMembers -> line to process = {}".format(line))
        portList = re.findall(r'((?:\d+:)?\d+)', line)
        debug("readVlanMembers -> ports extracted = {}".format(portList))
        vlanMemberDb[section].append(portList)

    debug("readVlanMembers -> vlanMemberDb = {}".format(vlanMemberDb))
    return vlanMemberDb


def readSwitchPorts(): # Obtains slot/port structure of switch
    cliOutput = cliCmd('show ports no-refresh', fmt='raw')
    portDb = defaultdict(list)
    for (slot, port) in re.findall(r'^(?:(\d):)?(\d+)', cliOutput, re.MULTILINE):
        if len(slot): # SummitStack
            currentSlot = int(slot)
        else:         # Standalone switch
            currentSlot = 0
        portDb[currentSlot].append(int(port)) # Thanks to defaultdict don't have to init the list

    debug("readSwitchPorts -> portDb = {}".format(portDb))
    return portDb


def allPortsRange(portDb): # Generates a range for all ports on switch
    slotList = sorted(portDb)
    debug("allPortsRange -> slotList = {}".format(slotList))
    if 0 in slotList: # Standalone switch
        allPorts = "{0}-{1}".format(portDb[0][0], portDb[0][-1])
    else:             # SummitStack
        allPorts = "{0}:{1}-{2}:{3}".format(slotList[0], portDb[slotList[0]][0], slotList[-1], portDb[slotList[-1]][-1])
    debug("allPortsRange -> allPorts = {}".format(allPorts))
    return allPorts


def generatePortList(portDb, portStr): # Given a port list/range, validates it and returns an ordered port list with no duplicates
    # Ported from ERS-NAC-Enforce.py & acli.pl
    debug("generatePortList IN = {}".format(portStr))
    slotList = sorted(portDb)
    portDict = {} # Use a dict, will ensure no port duplicate keys
    separator = ':' # We only handle XOS here
    for port in portStr.split(','):
        port = re.sub(r'^[\s\(]+', '', port) # Remove leading spaces  [ or '(' ]
        port = re.sub(r'[\s\)]+$', '', port) # Remove trailing spaces [ or ')' => XMC bug on ERS standalone units]
        if not len(port): # Skip empty string
            continue

        rangeMatch = RegexPortRange.match(port) # x-y
        if rangeMatch:
            if 0 not in slotList: return [] # Only accept this if Standalone switch 
            startPort = int(rangeMatch.group(1))
            endPort = int(rangeMatch.group(2))
            for port in range(startPort, endPort + 1):
                if port < portDb[0][0] or port > portDb[0][-1]: return []
                portDict[str(port)] = 1
            continue

        rangeMatch = RegexSlotPortRange.match(port) # s/x-y
        if rangeMatch:
            if 0 in slotList: return [] # Only accept this if a Stack
            startSlot = int(rangeMatch.group(1))
            startPort = int(rangeMatch.group(2))
            endPort = int(rangeMatch.group(3))
            if startSlot not in slotList: return []
            for port in range(startPort, endPort + 1):
                if port < portDb[startSlot][0] or port > portDb[startSlot][-1]: return []
                portDict[str(startSlot) + separator + str(port)] = 1
            continue

        rangeMatch = RegexSlotStarRange.match(port) # s/*
        if rangeMatch:
            if 0 in slotList: return [] # Only accept this if a Stack
            startSlot = int(rangeMatch.group(1))
            if startSlot not in slotList: return []
            for port in range(portDb[startSlot][0], portDb[startSlot][-1] + 1):
                portDict[str(startSlot) + separator + str(port)] = 1
            continue

        rangeMatch = RegexSlotSlotRange.match(port) # s/x-t/y
        if rangeMatch:
            if 0 in slotList: return [] # Only accept this if a Stack
            startSlot = int(rangeMatch.group(1))
            startPort = int(rangeMatch.group(2))
            endSlot = int(rangeMatch.group(3))
            endPort = int(rangeMatch.group(4))
            if startSlot not in slotList or endSlot not in slotList: return []
            for slot in slotList:
                if slot < startSlot: continue
                if slot > endSlot: break
                for port in range(portDb[slot][0], portDb[slot][-1] + 1):
                    if slot == startSlot and port < startPort: continue
                    if slot == endSlot and port > endPort: break
                    portDict[str(slot) + separator + str(port)] = 1
            continue

        if RegexPort.match(port): # Port is in valid format
            portDict[port] = 1
            continue

        # If we get here, we have a not recognized format
        return []

    # Sort and return the list as a comma separated string
    def portValue(port): # Function to pass to sorted(key)
        slotPort = port.split(':')
        if len(slotPort) == 2: # slot/port format
            idx = int(slotPort[0])*100 + int(slotPort[1])
        else: # standalone port (no slot)
            idx = int(slotPort[0])
        return idx
    portList = sorted(portDict, key=portValue)

    debug("generatePortList OUT = {}".format(portList))
    return portList


def generatePortRange(portDb, portList): # Given an ordered list of ports, generates a compacted port list/range string for use on CLI commands
    # Ported from acli.pl; this version of this function is customized for XOS only
    debug("generatePortRange IN = {}".format(portList))
    slotList = sorted(portDb)
    separator = ':' # We only handle XOS here

    def nextSlot(slot): # Next slot after current slot; 0 if last
        nextSlot = 0
        for s in slotList:
            if s > slot:
                nextSlot = s
                break
        return nextSlot

    def lastPortOfSlot(slot, port): # Returns true if port is last port of slot; false otherwise
        lastPortOfSlot = False
        if portDb[slot][-1] == port:
            lastPortOfSlot = True
        return lastPortOfSlot

    def rangeLast(slot, port, startSlot):
        if slot == startSlot:
            return str(port)
        else:
            return str(slot) + separator + str(port)

    elementList = []
    elementBuild = None
    currentType = None
    currentSlot = None
    currentPort = None
    elemRangeLast = None
    for port in portList:
        debug("generatePortRange port = {}".format(port))
        slotPort = re.split(':', port) # Split on ':'(XOS)
        # slotPort[0] = slot / slotPort[1] = port
        if len(slotPort) == 2: # slot/port
            slotN = int(slotPort[0])
            portN = int(slotPort[1])
            if elementBuild:
                if currentType == 's/p' and slotN == currentSlot and portN == currentPort + 1:
                    currentPort = portN
                    elemLastPortOfSlot = lastPortOfSlot(currentSlot, currentPort)
                    elemRangeLast = rangeLast(currentSlot, currentPort, startSlot)
                    debug("generatePortRange s/p port++ / elemRangeLast : {}".format(elemRangeLast))
                    continue
                elif currentType == 's/p' and slotN == elemNextSlot and elemLastPortOfSlot and portN == 1:
                    currentSlot = slotN
                    currentPort = portN
                    elemLastPortOfSlot = lastPortOfSlot(currentSlot, portN)
                    elemNextSlot = nextSlot(currentSlot)
                    elemRangeLast = rangeLast(currentSlot, currentPort, startSlot)
                    debug("generatePortRange s/p slot++ / elemRangeLast : {}".format(elemRangeLast))
                    continue
                else: # Range complete
                    if elemRangeLast:
                        elementBuild += '-' + elemRangeLast
                    elementList.append(elementBuild)
                    debug("generatePortRange added s/p elementBuild = {}".format(elementBuild))
                    elementBuild = None
                    elemRangeLast = None
                    # Fall through below
            currentType = 's/p'
            currentSlot = slotN
            currentPort = portN
            startSlot = currentSlot
            elemNextSlot = nextSlot(currentSlot)
            elemLastPortOfSlot = lastPortOfSlot(currentSlot, portN)
            elementBuild = port
            debug("generatePortRange s/p currentSlot & startSlot = {} / currentPort = {} / elemNextSlot = {} / elementBuild : {}".format(currentSlot, currentPort, elemNextSlot, elementBuild))

        if len(slotPort) == 1: # simple port (no slot)
            portN = int(port)
            if elementBuild:
                if currentType == 'p' and portN == currentPort + 1:
                    currentPort = portN
                    elemRangeLast = str(currentPort)
                    debug("generatePortRange p port++ / elemRangeLast : {}".format(elemRangeLast))
                    continue
                else: # Range complete
                    if elemRangeLast:
                        elementBuild += '-' + elemRangeLast
                    elementList.append(elementBuild)
                    debug("generatePortRange added p elementBuild = {}".format(elementBuild))
                    elementBuild = None
                    elemRangeLast = None
                    # Fall through below
            currentType = 'p'
            currentPort = portN
            elementBuild = port
            debug("generatePortRange p currentPort = {} / elementBuild = {}".format(currentPort, elementBuild))

    if elementBuild: # Close off last element we were holding
        if elemRangeLast:
            elementBuild += '-' + elemRangeLast
        elementList.append(elementBuild)
        debug("generatePortRange added last elementBuild = {}".format(elementBuild))

    portStr = ','.join(elementList)
    debug("generatePortRange OUT = {}".format(portStr))
    return portStr                


def addFaPorts(ports):
    error = cliCmd('configure upm event device-detect profile {0}-detect ports {1}'.format(ThisMod, ports), fmt='raw')
    if error: return False
    error = cliCmd('configure upm event device-undetect profile {0}-undetect ports {1}'.format(ThisMod, ports), fmt='raw')
    if error: return False
    return True


def deleteFaPorts():
    error = cliCmd('unconfigure upm event device-detect profile {0}-detect'.format(ThisMod), fmt='raw')
    if error: return False
    error = cliCmd('unconfigure upm event device-undetect profile {0}-undetect'.format(ThisMod), fmt='raw')
    if error: return False
    return True


def readLldpNeighbours(ports): # Extracts data from LLDP neighbours on ports specified
    class local: # Can't use nonlocal to let nested function modify variables of outer function with Python 2.x 
        # Workaround from: https://stackoverflow.com/questions/3190706/nonlocal-keyword-in-python-2-x
        lldpDb = {}
        matchFlag = {}
        keyOrder = []

    def matchLine(key, regex, port, line, integer=False):
        if key not in local.matchFlag.keys():
            local.keyOrder.append(key) # Recors keys we checked, for each line
            match = re.match(regex, line)
            #debug("readLldpNeighbours -> match {0}".format(key))
            if match:
                if len(match.groups()):
                    data = match.group(1)
                    if integer:
                        data = int(data)
                else:
                    data = True
                local.lldpDb[port][key] = data
                debug("readLldpNeighbours -> {0} = {1}".format(key, data))
                for skipKey in local.keyOrder: # No point checking again for these keys on future LLDP lines for same port
                    local.matchFlag[skipKey] = 1
                return True
        return False

    cliOutput = cliCmd('show lldp ports {} neighbors detailed'.format(ports), fmt='raw')
    port = None
    faSection = False
    for line in cliOutput.splitlines():
        # Empty the keyOrder list at every new line
        local.keyOrder = []

        # Match section line for port LLDP neighbour
        match = re.match(r'^LLDP Port ((?:\d)?:\d+) detected 1 neighbor', line)
        if match: # We expressly only match ports with 1 and only 1 LLDP neighbour!
            port = match.group(1)
            local.lldpDb[port] = {}
            local.matchFlag = {}  # Clear all keys
            debug("readLldpNeighbours -> port = {}".format(port))
            continue
        if re.match(r'^LLDP Port (?:\d)?:\d+ detected \d neighbor', line): # If > 1 LLDP neighbour, skip the port
            port == None
        if port == None: continue # Go no further unless we are locked on a port

        # LLDP general data; must be entered in the same order it appears in command output
        if matchLine('chassId', r'^\s+Chassis ID\s+:\s+(\S+)', port, line): continue
        if matchLine('sysName', r'^\s+- System Name:\s+"([^"]+)"', port, line): continue
        if matchLine('sysDescr', r'^\s+- System Description:\s+"([^"]+)"', port, line): continue
        if matchLine('mgmtAddr', r'^\s+Management Address\s+:\s+(\S+)', port, line): continue
        if matchLine('medModelName', r'^\s+- MED Model Name:\s+"([^"]+)"', port, line): continue

        # LLDP FA section
        if matchLine('faClient', r'^\s+- Avaya/Extreme Fabric Attach element', port, line):
            debug("readLldpNeighbours -> start of FA section")
            faSection = True
            continue
        if not faSection: continue # Go no further unless we have an FA section

        # LLDP FA data
        if matchLine('faElemType', r'^\s+Element Type   : (\d+)', port, line, integer=True): continue
        if matchLine('faElemState', r'^\s+State          : (\d+)', port, line, integer=True): continue
        if matchLine('faMgmtVlan', r'^\s+Management Vlan: (\d+)', port, line, integer=True): continue
        if matchLine('faSysId', r'^\s+SystemId       :\s+(\S+)', port, line):
            local.lldpDb[port]['faSysId'] = re.sub(':', '-', local.lldpDb[port]['faSysId'])
            continue
        if matchLine('faSysId2', r'^\s+Link Info      :\s+(\S+)', port, line):
            # We need to append this to the faSysId key data
            local.lldpDb[port]['faSysId'] += '-' + local.lldpDb[port]['faSysId2']
            del local.lldpDb[port]['faSysId2']
            debug("readLldpNeighbours -> faSysId = {}".format(local.lldpDb[port]['faSysId']))
            continue

    debug("readLldpNeighbours -> LLDP Data Collected = {}".format(local.lldpDb))
    return local.lldpDb


def plumbZtcClients(cfgDict, ports, clientType=None): # Configures VLAN/I-SID on ports where FA clients discovered
    # Get fresh LLDP data on the configured ports
    lldpDb = readLldpNeighbours(ports)
    # Read in existing switch VLANs & I-SIDs config
    vlanDb = readExistingVlans()
    # Read in the current VLAN config of the port we are working with
    portVlanDb = readPortVlans(ports)
    # Flag indicating if the ZTC config has changed
    ztcConfigModified = False

    # Cycle through every port where LLDP data was extracted
    for port in lldpDb.keys():
        debug("plumbZtcClients -> looking at lldp neighbour on port {}".format(port))
        if 'faClient' not in lldpDb[port]:
            # Currently, we only process FA CLients
            debug("plumbZtcClients -> skipping non-FA client")
            continue
        faClientNumber = lldpDb[port]['faElemType']
        if faClientNumber < 6:
            # We do not process ZTC on FA Server/Proxy element types
            debug("plumbZtcClients -> skipping server/proxy element = {}".format(faClientNumber))
            continue
        if clientType and FaClientTypes[clientType] != faClientNumber:
            # If a clientType was provided, then we only handle those FA client types
            debug("plumbZtcClients -> skipping different client type from specified = {}".format(clientType))
            continue
        # Determine FA Client type (name, not number)
        faClientName = FaElementTypes[faClientNumber]
        debug("plumbZtcClients -> faClientName = {}".format(faClientName))
        if faClientName not in cfgDict['client'].keys():
            # We don't have any ZTC config for this client type
            debug("plumbZtcClients -> no ZTC config for faClientName = {}".format(faClientName))
            continue
        # If we get here, then we have detected an FA client for which we have ZTC config
        cliCmd('create log message "{0}: detected FA client {1} on port {2}"'.format(ThisMod, faClientName, port))

        # Before doing any config, verify that ZTC vlan/isid data can be applied on switch
        vlan = cfgDict['client'][faClientName]['vlan']
        isid = cfgDict['client'][faClientName]['isid']
        debug("plumbZtcClients -> ztc vlan = {} isid = {}".format(vlan, isid))
        isidVlan = lookupExistingIsids(vlanDb, isid)
        debug("plumbZtcClients -> isidVlan = {}".format(isidVlan))
        if isidVlan and isidVlan != vlan:
            # We have a clash, ZTC isid is already assigned to a different VLAN
            debug("plumbZtcClients -> isid clash, isid {} already assigned to vlan {}".format(isid, isidVlan))
            cliCmd('create log message "{0}: ERROR - i-sid {1} is already assigned to vlan {2}"'.format(ThisMod, isid, isidVlan))
            continue

        if vlan not in vlanDb.keys():
            # VLAN for this ZTC client does not exist, we need to create it 
            error = cliCmd('create vlan {0}{1:04d} tag {1}'.format(VlanNamePrefix, vlan), fmt='raw')
            if error:
                debug("plumbZtcClients -> error creating vlan = {}".format(vlan))
                cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                return
            debug("plumbZtcClients -> created vlan = {}".format(vlan))
            cfgDict['vlan'][vlan] = 1 # Remember that we created the VLAN
            ztcConfigModified = True
            debug("plumbZtcClients -> created record in ZTC config file for vlan {} creation".format(vlan))

        if isidVlan == None:
            # I-SID is not configured on the VLAN
            error = cliCmd('configure vlan {} add isid {}'.format(vlan, isid), fmt='raw')
            if error:
                debug("plumbZtcClients -> failed to assign i-sid {} to vlan {}".format(isid, vlan))
                cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                return
            debug("plumbZtcClients -> assigned i-sid {} to vlan {}".format(isid, vlan))
            if not ztcConfigModified: # Only if we did not create the vlan just above
                # Case where the VLAN existed on the switch, but had no I-SID binding
                cfgDict['isid'][isid] = 1 # Remember that we created the ISID binding on an already existing VLAN
                ztcConfigModified = True
                debug("plumbZtcClients -> created record in ZTC config file for isid {} assignment".format(isid))

        if vlan not in portVlanDb[port]['untagged']:
            # VLAN not already configured as untagged on port, we need to add it
            # Do we need to bother with ?: 'config vlan untagged-ports auto-move on'
            error = cliCmd('configure vlan {} add ports {} untagged'.format(vlan, port), fmt='raw')
            if error:
                debug("plumbZtcClients -> failed to assign vlan {} to port {}".format(vlan, port))
                cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                return
            debug("plumbZtcClients -> assigned vlan {} to port {}".format(vlan, port))
            if vlan in vlanDb.keys(): # VLAN was already there, we have a name for it
                cliCmd('create log message "{}: applied vlan \'{}\'({}) i-sid {} on port {}"'.format(ThisMod, vlanDb[vlan]['name'], vlan, isid, port))
            else: # We just created the VLAN, so we don't have a name for it (a dynamic name anyway..)
                cliCmd('create log message "{}: applied vlan {} i-sid {} on port {}"'.format(ThisMod, vlan, isid, port))
            if port not in cfgDict['port'].keys(): # This is the 1st time ZTC configures this port
                cfgDict['port'][port] = {'client': faClientNumber, 'add': {'untagged': []}, 'del': {'untagged': []}}
                ztcConfigModified = True
                debug("plumbZtcClients -> created record in ZTC config file for port {}".format(port))
            if vlan not in cfgDict['port'][port]['add']['untagged']: # Unless already listed..
                cfgDict['port'][port]['add']['untagged'].append(vlan) # We add the vlan to the list
                if portVlanDb[port]['untagged']: # If untagged vlans were on the port, these will get bumped, so..
                    cfgDict['port'][port]['del']['untagged'] = list(portVlanDb[port]['untagged']) # Copy the list across (not the pointer)
                ztcConfigModified = True
                debug("plumbZtcClients -> added vlan {} port {} in ZTC config file".format(vlan, port))

    #cliCmd('save configuration')
    return ztcConfigModified


def unplumbZtcClients(cfgDict, ports, portList=[], clientType=None): # Unconfigures VLAN/I-SID on ports where FA clients removed, or config withdrawn
    # Read in existing switch VLANs & I-SIDs config
    vlanDb = readExistingVlans()
    # Read in the current VLAN config of the port we are working with
    portVlanDb = readPortVlans(ports)
    # Flag indicating if the ZTC config has changed
    ztcConfigModified = False
    if not portList: # Single port syntax
        portList = [ports]

    for port in portList:
        if port not in cfgDict['port'].keys():
            # No ZTC config for this port
            debug("unplumbZtcClients -> skipping port {} as it has no ZTC config".format(port))
            continue
        faClientNumber = cfgDict['port'][port]['client']
        if clientType and FaClientTypes[clientType] != faClientNumber:
            # If a clientType was provided, then we only handle those FA client types
            debug("unplumbZtcClients -> skipping port {} as it has different client type from specified = {}".format(clientType))
            continue

        # If we get here, then we have ZTC config on this port which needs removing
        for vlan in cfgDict['port'][port]['add']['untagged']:
            if vlan not in vlanDb.keys():
                debug("unplumbZtcClients -> ztc originally added untagged vlan {} no longer exists; no need to remove it".format(vlan, port))
                continue
            if vlan not in portVlanDb[port]['untagged']:
                debug("unplumbZtcClients -> ztc originally added untagged vlan {} is no longer on port {}; no need to remove it from port".format(vlan, port))
                continue
            error = cliCmd('configure vlan {} delete ports {}'.format(vlan, port), fmt='raw')
            if error:
                debug("unplumbZtcClients -> failed to remove vlan {} from port {}".format(vlan, port))
                cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                return
            debug("unplumbZtcClients -> removed vlan {} from port {}".format(vlan, port))
            cliCmd('create log message "{}: removed vlan \'{}\'({}) i-sid {} from port {}"'.format(ThisMod, vlanDb[vlan]['name'], vlan, vlanDb[vlan]['name'], port))
            isid = vlanDb[vlan]['isid']
            if str(vlan) in cfgDict['vlan'].keys(): # We originally created the vlan
                if vlanDb[vlan]['name'] == "{}{:04d}".format(VlanNamePrefix, vlan): # Vlan still has ZTC generated name
                    vlanMemberDb = readVlanMembers(vlan)
                    if len(vlanMemberDb['untagged']) == 0 and len(vlanMemberDb['tagged']) <= 1: # VLAN seems is unused 
                        error = cliCmd('delete vlan {}'.format(vlan), fmt='raw')
                        if error:
                            debug("unplumbZtcClients -> failed to delete vlan {}".format(vlan))
                            cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                            return
                        debug("unplumbZtcClients -> deleted vlan {}".format(vlan))
                        del cfgDict['vlan'][str(vlan)]
            elif str(isid) in cfgDict['isid'].keys(): # We originally assigned the isid
                vlanMemberDb = readVlanMembers(vlan)
                if len(vlanMemberDb['untagged']) == 0 and len(vlanMemberDb['tagged']) <= 1: # VLAN seems is unused 
                    error = cliCmd('configure vlan {} delete isid {}'.format(vlan, isid), fmt='raw')
                    if error:
                        debug("unplumbZtcClients -> unable to remove isid {} from vlan {}".format(isid, vlan))
                        cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                        return
                    debug("unplumbZtcClients -> removed isid {} from vlan {}".format(isid, vlan))
                    del cfgDict['isid'][str(isid)]

        for vlan in cfgDict['port'][port]['del']['untagged']:
            if vlan not in vlanDb.keys():
                debug("unplumbZtcClients -> vlan {} we are trying to restore on port {} no longer exists on switch; skipping restore".format(vlan, port))
                continue
            error = cliCmd('configure vlan {} add ports {} untagged'.format(vlan, port), fmt='raw')
            if error:
                debug("unplumbZtcClients -> failed to restore untagged vlan {} on port {}".format(vlan, port))
                cliCmd('create log message "{}: {}"'.format(ThisMod, error))
                return
            debug("unplumbZtcClients -> restored untagged vlan {} on port {}".format(vlan, port))

        # Empty the config record of ZTC vlans
        del cfgDict['port'][port]
        ztcConfigModified = True

    #cliCmd('save configuration')
    return ztcConfigModified

#
# Main
#
def main():
    if len(sys.argv) == 1: # Script called with no arguments
        if checkAlreadyInstalled():
            printSyntax()
        else:
            print "\nFabric-Attach Zero-Touch-Client (fa-ztc version {})\n".format(__version__), '=' * 52
            print "This Python script will do the following:"
            print " - Anchor itself into the XOS switch Universal Port Manager (UPM)"
            print "   as an event handler responding to 'device-detect' and"
            print "   'device-undetect' events"
            print " - Create an alias command '{}' on the XOS switch to allow".format(ThisMod)
            print "   user to configure ZTC via command line\n"
            confirm = raw_input("Ok to proceed (y/n) ?").lower()[0]
            if confirm != 'y': sys.exit(0)
            cfgOverwrite = True
            if path.isfile(FaConfigFile):
                print "\nA ZTC config already exists on this switch\n"
                confirm = raw_input("Overwrite that config file with an empty config (y/n) ?").lower()[0]
                if confirm != 'y':
                    cfgOverwrite = False
            installFaZtc(cfgOverwrite)
            print "\nFA Zero-Touch_client script is now active"
            print "Please logout and log back in for alias '{}' to be active".format(ThisMod)
            print "Then can use command '{}' to configure ZTC bindings".format(ThisMod)
            print "To uninstall, use command 'run script {}.py uninstall'".format(ThisMod)

    else:
        mode = sys.argv[1]
        matchList = [cmd for cmd in Command if re.match('^'+mode, cmd)]
        if len(matchList) == 1:
            userCmd = matchList[0]
        else:
            userCmd = None
        if mode == 'upm-detect': # Launched by UPM
            port = sys.argv[2]
            clientMac = sys.argv[3]  # We don't use this however..
            debug("fa-ztc upm-detect -> port = {} mac = {}".format(port, clientMac))
            # Read the ZTC config
            cfgDict = readZtcConfig()
            # Add client on detection port
            if plumbZtcClients(cfgDict, port):
                writeZtcConfig(cfgDict)

        elif mode == 'upm-undetect': # Launched by UPM
            port = sys.argv[2]
            debug("fa-ztc upm-undetect -> port = {}".format(port))
            # Read the ZTC config
            cfgDict = readZtcConfig()
            # Remove client on detection port
            if unplumbZtcClients(cfgDict, port):
                writeZtcConfig(cfgDict)

        elif mode == 'uninstall': # Uninstall
            if checkAlreadyInstalled():
                print "\nYou are about to uninstall the Fabric-Attach Zero-Touch-Client (ZTC) script.\n"
                confirm = raw_input("Ok to proceed (y/n) ?").lower()[0]
                if confirm != 'y': sys.exit(0) 
                uninstallFaZtc()
                print "\nFabric-Attach Zero-Touch-Client (ZTC) script has been uninstalled"
                print "Please logout and log back in for alias '{}' to be de-activated".format(ThisMod)
            else:
                print "Fabric-Attach Zero-Touch-Client (ZTC) script is not installed on this switch\n"

        elif mode == 'debug': # Toggles debug mode
            # Read the ZTC config
            cfgDict = readZtcConfig()
            global Debug
            debug("Debug disabled")
            cfgDict['debug'] = not cfgDict['debug']
            Debug = cfgDict['debug']            
            debug("Debug enabled")
            writeZtcConfig(cfgDict)

        elif mode == 'dump' and Debug: # For debugging only
            if len(sys.argv) > 3 and sys.argv[2] == 'vlan':
                readVlanMembers(sys.argv[3])
                return
            elif len(sys.argv) > 3 and sys.argv[2] == 'port':
                portDb = readSwitchPorts()
                ports = sys.argv[3]
            else:
                portDb = readSwitchPorts()
                ports = allPortsRange(portDb)
            portList = generatePortList(portDb, ports)
            portRange = generatePortRange(portDb, portList)
            readExistingVlans()
            readPortVlans(portRange)
            readLldpNeighbours(portRange)

        elif userCmd: # Launched by user to configure bindings
            # Read the ZTC config
            cfgDict = readZtcConfig()
            if userCmd == 'add' and len(sys.argv) == 5: # Add a binding
                clientType = sys.argv[2]
                vlan = int(sys.argv[3])
                isid = int(sys.argv[4])
                debug("fa-ztc add -> {} vlan = {} isid = {}".format(clientType, vlan, isid))
                if vlan > 4095 or vlan <= 0:
                    print 'Error: Vlan id value needs to be between 1-4095'
                    sys.exit(1)
                if isid > 15999999 or isid <= 0:
                    print 'Error: I-sid value needs to be between 1-15999999'
                    sys.exit(1)
                if clientType in cfgDict['client']:
                    print 'Error: ZTC binding already exists for FA client {}'.format(clientType)
                    sys.exit(1)
                vlanDb = readExistingVlans()
                if vlan in vlanDb and vlanDb[vlan]['isid'] != None and vlanDb[vlan]['isid'] != isid:
                    print 'Error: Vlan {} is already assigned to a different i-sid {}'.format(vlan, isid)
                    sys.exit(1)
                # check also that isid not assigned to a diff vlan
                cfgDict['client'][clientType] = {'vlan': vlan, 'isid': isid}
                if cfgDict['ports']: # Trawl the active ports for existing FA Clients of type just added
                    plumbZtcClients(cfgDict, cfgDict['ports'], clientType)
                writeZtcConfig(cfgDict)

            elif userCmd == 'remove' and len(sys.argv) == 3: # Remove a binding
                clientType = sys.argv[2]
                debug("fa-ztc remove -> {}".format(clientType))
                if not clientType in cfgDict['client']:
                    print 'Error: There are no ZTC bindings for FA client {}'.format(clientType)
                    sys.exit(1)
                del cfgDict['client'][clientType]
                if cfgDict['ports']: # Trawl the active ports for existing FA Clients of type just deleted
                    portDb = readSwitchPorts()
                    portList = generatePortList(portDb, cfgDict['ports'])
                    unplumbZtcClients(cfgDict, cfgDict['ports'], portList, clientType)
                writeZtcConfig(cfgDict)

            elif userCmd == 'ports' and len(sys.argv) == 3: # Set FA access ports for ZTC
                portList = sys.argv[2]
                debug("fa-ztc ports -> {}".format(portList))
                portDb = readSwitchPorts() # In all cases we will need this
                if portList.lower() == 'none':
                    newPorts = None
                    newPortList = []
                elif portList.lower() == 'all':
                    newPorts = allPortsRange(portDb)
                    newPortList = generatePortList(portDb, newPorts)
                else:
                    newPortList = generatePortList(portDb, portList)
                    if newPortList:
                        newPorts = generatePortRange(portDb, newPortList)
                    else:
                        print 'Error: invalid port list {}'.format(portList)
                        return
                # Clean up old ports
                if cfgDict['ports'] != None:
                    ok = deleteFaPorts()
                    if not ok: return
                    # Obtain a list of ports where we are about to disable ZTC
                    oldPortList = generatePortList(portDb, cfgDict['ports'])
                    deletePortList = [x for x in oldPortList if x not in newPortList]
                    if deletePortList:
                        deletePorts = generatePortRange(portDb, deletePortList)
                        unplumbZtcClients(cfgDict, deletePorts, deletePortList)
                # Assign the new ports
                cfgDict['ports'] = newPorts
                if cfgDict['ports'] != None:
                    if cfgDict['client']: # If client bindings present, trawl the ports existing FA Clients
                        plumbZtcClients(cfgDict, cfgDict['ports'])
                    ok = addFaPorts(cfgDict['ports'])
                    if not ok: return
                writeZtcConfig(cfgDict)

            elif userCmd == 'show' and len(sys.argv) == 2: # Show ZTC configuration
                debug("fa-ztc show")
                print "\nFabric-Attach Zero-Touch-Client (ZTC) configuration\n", '=' * 51
                print "FA ports (UPM): {}\n".format(cfgDict['ports'])
                print "Type  Client Name        VLAN       I-SID\n", '-' * 41
                for client in cfgDict['client'].keys():
                    print '{:3}   {:15}    {:4d}    {:8d}'.format(FaClientTypes[client], client, cfgDict['client'][client]['vlan'], cfgDict['client'][client]['isid'])
                print
            else:
                printSyntax()

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
