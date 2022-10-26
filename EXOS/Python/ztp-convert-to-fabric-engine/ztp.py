##########################################################
# XOS Python Script: Convert to Fabric Engine            #
# Written by Ludovico Stevens, TME Extreme Networks      #
##########################################################

__version__ = '1.1'

Description = '''
Script Version {}. Converts Universal Hardware to Fabric Engine.
This script needs to be placed on a USB stick and named "ztp.py"
together with the desired VOSS image for the Universal platform.
When the unconfigured Universal Hardware boots into Switch Engine OS
this script will automatically execute and install the correct
VOSS image onto the swtich. If many VOSS images are present on the
USB stick, the script will locate the correct one based on switch
model and most recent software version, but will anyway keep trying
with all supplied VOSS images until one succeeds. The script will
only terminate once the OS conversion has been triggered and the
switch is reset, or if the USB stick is removed.
'''.format(__version__)

# Changes
# 1.0  - Initial version
# 1.1  - Modified to run with Python3 as well as Python2; EXOS32.2 introduces Python3 and drops Python2 support

#
# Imports
#
from os import path, listdir
import re
import sys
import datetime
import exsh
import time
import argparse

#
# Global Variables
#
Debug = False
Sanity = False
LOG = None
LastError = None
RegexError  = re.compile(
    '^%|\x07|error|invalid|cannot|unable|bad|not found|not exist|not allowed|no such|out of range|incomplete|failed|denied|can\'t|ambiguous|do not|unrecognized',
    re.IGNORECASE | re.MULTILINE
)
ConfigHistory = []

ThisMod = __file__.split(path.sep)[-1].split('.')[0]    # Name of this module
UsbPath = '/usr/local/ext/'
IntPath = '/usr/local/cfg/'
ZtpLog = UsbPath + 'ztp-conversion.log'
DebugLog = IntPath + 'ztp-debug.log'
RetryDelay = 30

CLI_Dict = {
        'disable_cli_prompting'      : 'disable cli prompting',
        'get_switch_serial_number'   : 'str://show version | include Switch||^Switch *: *\S+ +(\S+)',
        'get_switch_type'            : 'str://show switch | include "System Type:"||^System Type: +(\d{4})',
        'install_usb_image'          : 'download url file:///usr/local/ext/{} install', # Filename
        'reboot'                     : 'reboot',
}

#
# Functions
#

def getUserParams(): # Set up argparse
    parser = argparse.ArgumentParser(description=Description + '='*78)
    parser.add_argument('-d', '--debug', nargs='?', const=True, default=False, help="Debug")
    parser.add_argument('-s', '--sanity', nargs='?', const=True, default=False, help="Sanity")
    return parser.parse_args()

def logMessage(logMsg): # Print message on console + append to USB log file
    print("{}: {}".format(ThisMod, logMsg))
    if LOG: LOG.write("{}: {}\n".format(datetime.datetime.now(), logMsg))

def debug(debugOutput): # Use to include debugging in script; set above Debug variable to True or False to turn on or off debugging
    if Debug: logMessage(debugOutput)
    try: # Always append debug to the debug file
        dbgLog = open(DebugLog, "a")
        dbgLog.write(debugOutput + "\n")
        dbgLog.close()
    except IOError: # We don't want to bomb out if we cant write the debug log...
        print("Unable to open ztp debug log file: {}".format(dbgLog))


def exitError(errmsg): # v1 - Exit script with error message and setting status appropriately
    logMessage(errmsg)
    if LOG: LOG.close()
    sys.exit(1)

def abortError(cmd, errorOutput): # v1.1 - A CLI command failed, before bombing out send any rollback commands which may have been set
    print("Aborting script due to error on previous command")
    try:
        rollbackStack()
    finally:
        print("Aborting because this command failed: {}".format(cmd))
        exitError(errorOutput)

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
        dbgLog = open(DebugLog, "a")
        dbgLog.write("{}# {}\n".format(datetime.datetime.now(), cmd))
    except IOError: # We don't want to bomb out if we cant write the debug log...
        print("Unable to open ztp debug log file: {}".format(dbgLog))

    try:
        output = exsh.clicmd(cmd, args=arg, capture=captFlag, xml=xmlFlag)
    except RuntimeError as detail:
        if dbgLog: dbgLog.close()
        errmsg = "Unable to execute CLI command '{}'".format(cmd)
        if arg: errmsg += " with arguments '{}'".foramt(arg)
        exitError(errmsg)

    if fmt == 'xml':
        # because exsh.clicmd returns malformed XML
        output = '<xmldata>' + output + '</xmldata>'

    if dbgLog:
        dbgLog.write("{}\n".format(output))
        dbgLog.close()

    return output

def cliError(outputStr): # v1 - Check command output for CLI error message
    if RegexError.search(outputStr):
        return True
    else:
        return False

def parseRegexInput(cmdRegexStr): # v1.1 - Parses input command regex for both sendCLI_showRegex() and xmcLinuxCommand()
    # cmdRegexStr format: <type>://<cli-show-command> [& <additional-show-cmd>]||<regex-to-capture-with>
    if re.match(r'\w+(?:-\w+)?://', cmdRegexStr):
        mode, cmdRegexStr = map(str.strip, cmdRegexStr.split('://', 1))
    else:
        mode = None
    cmd, regex = map(str.strip, cmdRegexStr.split('||', 1))
    cmdList = list(map(str.strip, cmd.split('&'))) # map() returns list in Python2 but iterator in Python3
    return mode, cmdList, regex

def formatOutputData(data, mode): # v3 - Formats output data for both sendCLI_showRegex() and xmcLinuxCommand()
    if not mode                 : value = data                                   # Legacy behaviour same as list
    elif mode == 'bool'         : value = bool(data)                             # No regex capturing brackets required
    elif mode == 'str'          : value = str(data[0]) if data else None         # Regex should have 1 capturing bracket at most
    elif mode == 'str-lower'    : value = str(data[0]).lower() if data else None # Same as str but string made all lowercase
    elif mode == 'str-upper'    : value = str(data[0]).upper() if data else None # Same as str but string made all uppercase
    elif mode == 'str-join'     : value = ''.join(data)                          # Regex with max 1 capturing bracket, joins list to string
    elif mode == 'str-nwlnjoin' : value = "\n".join(data)                        # Regex with max 1 capturing bracket, joins list to multi-line string
    elif mode == 'int'          : value = int(data[0]) if data else None         # Regex must have 1 capturing bracket at most
    elif mode == 'list'         : value = data                                   # If > 1 capturing brackets, will be list of tuples
    elif mode == 'list-reverse' : value = list(reversed(data))                   # Same as list but in reverse order
    elif mode == 'list-diagonal': value = [data[x][x] for x in range(len(data))] # Regex pat1|pat2 = list of tuples; want [0][0],[1][1],etc
    elif mode == 'tuple'        : value = data[0] if data else ()                # Regex > 1 capturing brackets, returns 1st tuple
    elif mode == 'dict'         : value = dict(data)                             # Regex must have 2 capturing brackets exactly
    elif mode == 'dict-reverse' : value = dict(map(reversed, data))              # Same as dict, but key/values will be flipped
    elif mode == 'dict-both'    : value = dict(data), dict(map(reversed, data))  # Returns 2 dict: dict + dict-reverse
    elif mode == 'dict-diagonal': value = dict((data[x][x*2],data[x][x*2+1]) for x in range(len(data))) # {[0][0]:[0][1], [1][2]:[1][3], etc}
    elif mode == 'dict-sequence': value = dict((data[x*2][0],data[x*2+1][1]) for x in range(len(data)/2)) # {[0][0]:[1][1], [2][0]:[3][1], etc}
    else:
        RuntimeError("formatOutputData: invalid scheme type '{}'".format(mode))
    return value

def sendCLI_showCommand(cmd, returnCliError=False, msgOnError=None): # v2.1 - Send a CLI show command; return output
    global LastError
    outputStr = cliCmd(cmd, fmt='raw')
    if outputStr and cliError("\n".join(outputStr.split("\n")[:4])): # If there is output, check for error in 1st 4 lines only
        if returnCliError: # If we asked to return upon CLI error, then the error message will be held in LastError
            LastError = outputStr
            if msgOnError:
                print("==> Ignoring above error: {}\n\n".format(msgOnError))
            return None
        abortError(cmd, outputStr)
    LastError = None
    return outputStr

def sendCLI_showRegex(cmdRegexStr, debugKey=None, returnCliError=False, msgOnError=None): # v1 - Send show command and extract values from output using regex
    # Regex is by default case-sensitive; for case-insensitive include (?i) at beginning of regex on input string
    mode, cmdList, regex = parseRegexInput(cmdRegexStr)
    for cmd in cmdList:
        # If cmdList we try each command in turn until one works; we don't want to bomb out on cmds before the last one in the list
        ignoreCliError = True if len(cmdList) > 1 and cmd != cmdList[-1] else returnCliError
        outputStr = sendCLI_showCommand(cmd, ignoreCliError, msgOnError)
        if outputStr:
            break
    if not outputStr: # returnCliError true
        return None
    data = re.findall(regex, outputStr, re.MULTILINE)
    debug("sendCLI_showRegex() raw data = {}".format(data))
    # Format we return data in depends on what '<type>://' was pre-pended to the cmd & regex
    value = formatOutputData(data, mode)
    if Debug:
        if debugKey: debug("{} = {}".format(debugKey, value))
        else: debug("sendCLI_showRegex OUT = {}".format(value))
    return value

def sendCLI_configCommand(cmd, returnCliError=False, msgOnError=None, waitForPrompt=True): # v3.1 - Send a CLI config command
    global LastError
    cmdStore = re.sub(r'\n.+$', '', cmd) # Strip added CR+y or similar
    if Sanity:
        print("SANITY> {}".format(cmd))
        ConfigHistory.append(cmdStore)
        LastError = None
        return True
    outputStr = cliCmd(cmd, fmt='raw')
    if outputStr and cliError("\n".join(outputStr.split("\n")[:4])): # If there is output, check for error in 1st 4 lines only
        if returnCliError: # If we asked to return upon CLI error, then the error message will be held in LastError
            LastError = outputStr
            if msgOnError:
                print("==> Ignoring above error: {}\n\n".format(msgOnError))
            return False
        abortError(cmd, outputStr)
    ConfigHistory.append(cmdStore)
    LastError = None
    return True

def sortImageFiles(switchType, vossImageFiles): # Sort the available VOSS image files
    orderedImages = []
    imageDict = {}
    imageOther = []

    def versionValue(version): # v1 - Function to pass to sorted(key) to sort version numbers
        verList = re.split(r'\.|int', version, maxsplit=5)
        intList = [int(re.sub(r'[^0-9]', '', v)) for v in verList] # As integers
        idx = intList[0]
        idx = idx*100 + intList[1]
        idx = idx*100 + intList[2]
        idx = idx*100 + intList[3]
        idx = idx*1000 + intList[4] if len(intList) > 4 else idx*1000
        return idx

    for imageFile in vossImageFiles:
        imageMatch = re.match(r'(\d{4})\.(\d[\.\d]+.*)\.voss$', imageFile)
        if imageMatch:
            model = imageMatch.group(1)
            version = imageMatch.group(2)
            if model not in imageDict:
                imageDict[model] = {}
            imageDict[model].update({version: imageFile})
        else:
            imageOther.append(imageFile)
    debug("sortImageFiles() imageDict = {}".format(imageDict))

    if switchType in imageDict:
        versionList = sorted(imageDict[switchType], key=versionValue, reverse=True)
        for version in versionList:
            orderedImages.append(imageDict[switchType][version])
        del imageDict[switchType]

    for switchType in imageDict:
        versionList = sorted(imageDict[switchType], key=versionValue, reverse=True)
        for version in versionList:
            orderedImages.append(imageDict[switchType][version])

    for otherImage in imageOther:
        orderedImages.append(otherImage)

    debug("sortImageFiles() orderedImages = {}".format(orderedImages))
    return orderedImages

#
# Main
#
def main():
    global Debug, Sanity, LOG

    # Get arguments if any
    args = getUserParams()
    if args.debug:
        Debug = True
        logMessage("Debug flag true")
    if args.sanity:
        Sanity = True
        logMessage("Sanity flag true")

    try:
        LOG = open(ZtpLog, "a")
    except IOError:
        print("Unable to open ztp log file on USB: {}".format(ZtpLog)) # We don't want to bomb out even if we can't write to USB log file..

    logMessage("=~=~=~=~=~=~=~=~=~=~= {} =~=~=~=~=~=~=~=~=~=~=".format(ThisMod))
    logMessage("Executing {} - ZTP conversion to Fabric Engine".format(ThisMod))

    # Disable CLI prompting
    sendCLI_configCommand(CLI_Dict['disable_cli_prompting'])
    logMessage("Disabled CLI prompting")

    # Find out the switch serial number; for log reporting only
    switchSerialNumber = sendCLI_showRegex(CLI_Dict['get_switch_serial_number'], "switchSerialNumber")
    logMessage("Switch has serial number: {}".format(switchSerialNumber))

    # Find out the Universal Model number
    switchType = sendCLI_showRegex(CLI_Dict['get_switch_type'], "switchType")
    if switchType:
        logMessage("Switch is Universal Hardware model: {}".format(switchType))
    else:
        logMessage("This switch is not a Universal Hardware model; aborting")
        LOG.close()
        return # Come out

    # List available *.voss files on USB
    vossImageFiles = [f for f in listdir(UsbPath) if path.isfile(path.join(UsbPath, f)) and f.endswith('.voss')]
    debug("vossImageFiles = {}".format(vossImageFiles))

    # Arrange images in order of preference
    orderedImageFiles = sortImageFiles(switchType, vossImageFiles)

    installSucceeded = False
    while (not installSucceeded): # Try until we succeed
        for vossImage in orderedImageFiles:
            logMessage("Selected VOSS image file {}".format(vossImage))

            # Install the VOSS image
            logMessage("Installing VOSS image {}".format(vossImage))
            sendCLI_configCommand(CLI_Dict['install_usb_image'].format(vossImage), returnCliError=True)
            if not LastError:
                installSucceeded = True
                logMessage("Completed installation of VOSS image {}".format(vossImage))
                break # We exit only if we succeed

            logMessage("Failed to install VOSS image {} with error: {}".format(vossImage, LastError))
            logMessage("Waiting {} seconds before trying again".format(RetryDelay))
            time.sleep(RetryDelay)

    # Reboot the switch
    logMessage("Rebooting the switch into VOSS!!\n")
    LOG.close() # Close the file before rebooting
    sendCLI_configCommand(CLI_Dict['reboot'], waitForPrompt=False)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
