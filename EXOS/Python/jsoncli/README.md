# JSONRPC CLI Example
## Description
This python script is an example of how to interface with EXOS 21.1 using JSONRPC over HTTP/HTTPS.
The script runs on a server communicating with a remote EXOS switch. The script does not run on an EXOS switch. 

JSONRPC offers a means of collecting the data from an EXOS switch in a machine readable JSON format.
This is the same data used to create user formatted display information.

Customers that manage their own automation are forced to ‘screen scrape’ to get information from switches not available via SNMP MIBs
- *Screen Scraping - Normally, data transfer between programs is accomplished using data structures suited for automated processing by computers, not people. EXOS shell CLI output is intended for display to an end-user, rather than as input to another program.  Scraping data from CLI output requires a customer to reverse engineer the CLI information display to collect the desired information.*

Using ‘expect scripts’ to scrape the data off the EXOS CLI output is highly dependent on the display format. If the display changes from release to release, the expect scripts break. 
### BENEFIT
Customers that have their own automation system have a programmatic interface into EXOS. Making the same CLI display data available in JSON variables greatly simplifies the task of automation by eliminating the need to ‘screen scrape’ to extract the desired switch information.
### FEATURE
JSONRPC is a standardized handshake over HTTP/HTTPS that allows any CLI command to be sent to an EXOS switch providing a programmatic way to manage switches and collect information.

EXOS shell CLI output produces a human readable display. Over the JSONRPC HTTP/HTTPS interface, the same EXOS CLI command returns the _data_ EXOS used to construct the CLI display. Customers no longer have to ‘scrape’ the data from a CLI display, they are provided with the actual data variables EXOS used to construct the display.
By using the CLI commands, the interface is well documented and evolves along with any new CLI or CLI updates. Customers can find the data elements they are interested in via CLI displays and then use the same CLI command on the JSONRPC interface to collect the data elements directly.
#### jsoncli.py example script
The jsoncli.py example script is intended to show a Python programmer how to interface their own Python applications with the EXOS JSONRPC `cli` method. Python developers may use parts of this script, specifically the JsonRPC class, as a guide when developing their applications.

```
E.g. The CLI command `show port 1 statistics` returns the machine readable JSON variables:
    {
      "show_ports_stats": {
        "dot1dTpPortInDiscards": 0,
        "dot1dTpPortInFrames": 6393,
        "dot1dTpPortMaxInfo": 1500,
        "dot1dTpPortOutFrames": 9707,
        "linkState": 1,
        "port": 1,
        "portList": 1,
        "portNoSnmp": 1,
        "rxBcast": 0,
        "rxByteCnt": 845258,
        "rxMcast": 6191,
        "rxPktCnt": 6393,
        "txBcast": 0,
        "txByteCnt": 851807,
        "txMcast": 9497,
        "txPktCnt": 9707
      },
      "status": "SUCCESS"
    }
```
### jsoncli.py
EXOS JSONRPC offers a number of 'methods' as described in JSONRPC release notes.
The `cli` method is illustrated in the jsoncli.py script.

### Files
* [jsoncli.py](jsoncli.py)
* [README.md](README.md)
* [JSONRPC Release Notes](http://documentation.extremenetworks.com/app_notes/MMI/121152_MMI_Application_Release_Notes.pdf)

### Requirements
- ExtremeXOS 21.1.1.4 and later.
- The web interface is enabled (default for EXOS 21.1 and later).
- if HTTPS is desired, the EXOS ssl module is configured

### Usage
`python jsoncli.py [-h] [-i IPADDRESS] [-u USERNAME] [-p PASSWORD]`

Command line parameters:
```
  -h, --help            show this help message and exit
  -i IPADDRESS, --ipaddress IPADDRESS
                IP address of remote EXOS switch
  -u USERNAME, --username USERNAME
                Login username for the EXOS switch
  -p PASSWORD, --password PASSWORD
			(optional)
                Login password for the EXOS switch. If the EXOS switch does not have a password, this option is not needed.
```
or
If the command line parameters are not specified, jsoncli.py will prompt for the information:
```
# python jsoncli.py
Enter remote system IP address: 10.68.65.80
Enter remote system username: admin
Remote system password: <enter>
Enter EXOS cli:
```
is the same as:
```
# python jsoncli.py -i 10.68.65.80 -u admin
```

#### Example 1
In this example, we will use the EXOS CLI command `show port 1-2 stat` which collects the port statistics for ports 1 and 2.
The response is both the JSON that is returned and the formatted display.
The formatted display is actualy returned in the JSON variable `CLIoutput`. jsoncli.py simply prints the contents of the variable to show what it would look like when the CLI command was directly entered into an EXOS shell.

By examining the display and the JSON variables, the mapping of which variables provide the different parts of the display can be determined.

```
# python jsoncli.py -i 10.68.65.80 -u admin
Enter EXOS cli: show port 1-2 stat
JSONRPC Response for: show port 1-2 stat
********************************************************************************
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": [
    {
      "CLIoutput": "Port      Link       Tx Pkt     Tx Byte      Rx Pkt     Rx Byte      Rx Pkt      Rx Pkt      Tx Pkt      Tx Pkt\n          State       Count       Count       Count       Count       Bcast       Mcast       Bcast       Mcast\n========= ===== =========== =========== =========== =========== =========== =========== =========== ===========\n1         A           33731     4404010        3593      623754         443        1000           0       31736\n2         A            4978      814892       33827     4432278           0       31730         443        2499\n========= ===== =========== =========== =========== =========== =========== =========== =========== ===========\n          > in Port indicates Port Display Name truncated past 8 characters\n          > in Count indicates value exceeds column width. Use 'wide' option or '0' to clear.\n          Link State: A-Active, R-Ready, NP-Port Not Present, L-Loopback\n"
    },
    {
      "show_ports_stats": {
        "dot1dTpPortInDiscards": 0,
        "dot1dTpPortInFrames": 3593,
        "dot1dTpPortMaxInfo": 1500,
        "dot1dTpPortOutFrames": 33731,
        "linkState": 1,
        "port": 1,
        "portList": "1-2",
        "portNoSnmp": 1,
        "rxBcast": 443,
        "rxByteCnt": 623754,
        "rxMcast": 1000,
        "rxPktCnt": 3593,
        "txBcast": 0,
        "txByteCnt": 4404010,
        "txMcast": 31736,
        "txPktCnt": 33731
      },
      "status": "MORE"
    },
    {
      "show_ports_stats": {
        "dot1dTpPortInDiscards": 0,
        "dot1dTpPortInFrames": 33827,
        "dot1dTpPortMaxInfo": 1500,
        "dot1dTpPortOutFrames": 4978,
        "linkState": 1,
        "port": 2,
        "portList": "1-2",
        "portNoSnmp": 2,
        "rxBcast": 0,
        "rxByteCnt": 4432278,
        "rxMcast": 31730,
        "rxPktCnt": 33827,
        "txBcast": 443,
        "txByteCnt": 814892,
        "txMcast": 2499,
        "txPktCnt": 4978
      },
      "status": "SUCCESS"
    }
  ]
}

Formatted CLIoutput Display
********************************************************************************
Port      Link       Tx Pkt     Tx Byte      Rx Pkt     Rx Byte      Rx Pkt      Rx Pkt      Tx Pkt      Tx Pkt
          State       Count       Count       Count       Count       Bcast       Mcast       Bcast       Mcast
========= ===== =========== =========== =========== =========== =========== =========== =========== ===========
1         A           33731     4404010        3593      623754         443        1000           0       31736
2         A            4978      814892       33827     4432278           0       31730         443        2499
========= ===== =========== =========== =========== =========== =========== =========== =========== ===========
          > in Port indicates Port Display Name truncated past 8 characters
          > in Count indicates value exceeds column width. Use 'wide' option or '0' to clear.
          Link State: A-Active, R-Ready, NP-Port Not Present, L-Loopback

********************************************************************************
Enter EXOS cli: quit

```
#### Example 2
This example shows what happens when providing EXOS CLI commands that do not have a display output such as `create vlan 10-20` or `disable port 1`.

From the example below, the CLIoutput is an empty string and there are no additional JSON variables returned.
```
Enter EXOS cli: create vlan 10-20
JSONRPC Response for: create vlan 10-20
********************************************************************************
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": [
    {
      "CLIoutput": ""
    }
  ]
}

Formatted CLIoutput Display
********************************************************************************

********************************************************************************
Enter EXOS cli: disable port 1
JSONRPC Response for: disable port 1
********************************************************************************
{
  "id": 2,
  "jsonrpc": "2.0",
  "result": [
    {
      "CLIoutput": ""
    }
  ]
}

Formatted CLIoutput Display
********************************************************************************

********************************************************************************
Enter EXOS cli: quit
```
#### Example 3
This example shows the JSONRPC response to an EXOS CLI command error. The same error message that is displayed on the EXOS shell is captured in the `CLIoutput` variable.

Additionally, a separate data block with the `status` variable will have the string value "ERROR"

```
Enter EXOS cli: show prt 1000
JSONRPC Response for: show prt 1000
********************************************************************************
{
  "id": 2,
  "jsonrpc": "2.0",
  "result": [
    {
      "CLIoutput": "Run time error. Command:show prt 1000"
    },
    {
      "status": "ERROR"
    }
  ]
}

Formatted CLIoutput Display
********************************************************************************
Run time error. Command:show prt 1000
********************************************************************************
Enter EXOS cli:
```


## Disclaimer
Python Scripts provided by Extreme Networks.

This script is provided free of charge by Extreme.  We hope such scripts are
helpful when used in conjunction with Extreme products and technology;
however, scripts are provided simply as an accommodation and are not
supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME ARE
HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS
THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.

>Be Extreme
