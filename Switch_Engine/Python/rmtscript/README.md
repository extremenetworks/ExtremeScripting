# rmtscript Example
## Description
rmtscript.py is an example of how to interface with EXOS 21.1 to run scripts remotely on EXOS switches.
rmtscript.py runs on a server communicating with a remote EXOS switch using the JSONRPC interface.
rmtscript.py does not run on an EXOS switch. 

The JSONRPC interface provides a means of running EXOS scripts by encoding, transporting, extracting and running the script on the switch.

### BENEFIT
Customers that have a central storage of EXOS scripts can run them on a switch without downloading/installing them on each switch. By maintaining scripts centrally, the task of script version control is simplified. The operator may run scripts on remote switches when the need arrises. It is not necessary to download a script to a switch before running it.

### FEATURE
This capability allows any EXOS script to be sent and run on a switch providing a programmatic way to manage switches and collect information.
The script follows the same conventions as if it were download to a switch and started using the EXOS CLI command:

_run script \<scriptname\>_

The stdout and stderr from the script is returned to the server.

#### rmtscript.py example script
The rmtscript.py example script is intended to show a Python programmer how to interface their own Python applications with the EXOS JSONRPC `runscript` method. Python developers may use parts of this script, specifically the JsonRPC class, as a guide when developing their applications.

### Files
* [rmtscript.py](rmtscript.py)
* [sample.py](sample.py)
* [README.md](README.md)
* [JSONRPC Release Notes](http://documentation.extremenetworks.com/app_notes/MMI/121152_MMI_Application_Release_Notes.pdf)

### Requirements
- A python 2 environment on the server
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
```
is the same as:
```
# python rmtscript.py -i 10.68.65.80 -u admin
```

The rmtscript.py starts running and prompts. In the example below, our script name is sample.py. sample.py does not take any command line arguments.

```
run script \<file\> [args]: sample.py
```
   sample.py is sent to the switch
   It would be the same as transfering sample.py to a switch and running the following command
       run script sample.py
   The sample.py stdout and stderr are captured and returned to the server

### Example 2:

The rmtscript.py starts running and prompts. In the example below, our script name is sample.py. sample.py takes command line arguments -a -b def.

```
run script <file> [args]: sample.py -a -b def
```
   sample.py is sent to the switch with the command line args -a -b def
   It would be the same as transfering sample.py to a switch and running the following command
       run script sample.py -a -b def
   The sample.py stdout and stderr are captured and returned to the server


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
