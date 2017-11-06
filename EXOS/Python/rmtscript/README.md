# JSONRPC 'runscript' Example
## Description
This python script is an example of how to interface with EXOS 21.1 using JSONRPC over HTTP/HTTPS.
The script runs on a server communicating with a remote EXOS switch. The script does not run on an EXOS switch. 

JSONRPC offers a means of running scripts on switches without the need to transfer the script to the switch first.

### BENEFIT
Customers that have their own automation system have a programmatic interface into EXOS. The method='runscript' option of EXOS JSONRPC enables administrators to maintain scripts on a central server and run them on remote switches when the need arrises. It is not necessary to download a script to a switch before running it.

### FEATURE
JSONRPC is a standardized handshake over HTTP/HTTPS that allows any script to be sent and run on an EXOS switch providing a programmatic way to manage switches and collect information.

Over the JSONRPC HTTP/HTTPS interface, the same EXOS 'runscript' interface returns the stdout and stderr from the script running on a switch.

#### rmtscript.py example script
The rmtscript.py example script is intended to show a Python programmer how to interface their own Python applications with the EXOS JSONRPC `runscript` method. Python developers may use parts of this script, specifically the JsonRPC class, as a guide when developing their applications.

### rmtscript.py
EXOS JSONRPC offers a number of 'methods' as described in JSONRPC release notes.
The `runscript` method is illustrated in the rmtscript.py script.

### Files
* [rmtscript.py](rmtscript.py)
* [sample.py](sample.py)
* [README.md](README.md)
* [JSONRPC Release Notes](http://documentation.extremenetworks.com/app_notes/MMI/121152_MMI_Application_Release_Notes.pdf)

### Requirements
- A python environment
- The requests python module installed
- ExtremeXOS 21.1.1.4 and later.
- The web interface is enabled (default for EXOS 21.1 and later).
- if HTTPS is desired, the EXOS ssl module is configured

### Usage
`python rmtscript.py [-h] [-i IPADDRESS] [-u USERNAME] [-p PASSWORD]`

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
If the command line parameters are not specified, rmtscript.py will prompt for the information:
```
# python rmtscript.py
Enter remote system IP address: 10.68.65.80
Enter remote system username: admin
Remote system password: <enter>
Enter EXOS cli:
```
is the same as:
```
# python rmtscript.py -i 10.68.65.80 -u admin
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
