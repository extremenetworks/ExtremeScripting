# Documentation
* [Python Getting Started Guide](https://documentation.extremenetworks.com/pdfs/exos/Python_Getting_Started_Guide.pdf)
* [The EXOS Python API](https://www.extremenetworks.com/support/documentation-api/extremexos-software/)

<!---
------git_dlownload.py------
To allow git_download.py to find the scripts add the script to this list with no spaces for the table like autofsbackup does.
Add a space at the begining of the Description to omit the script from git_download. (see jsoncli)
-->

# Python Scripts
| Script name   | Description   |
| ------------- |:-------------:|
|[GitHub Script Downloader](git_download)|Downloads python scripts located on this page directly to your switch.|
|[Automatic Backup](autofsbackuppy)|Runs automated back up on all scripts, including configuration, policy and scripts.|
|[Clean Switch](cleanswitch)|Provides a method of deleting all configuration parameters and files from an EXOS switch.|
|[Config Diff](conf_diff)|Script to compare the current running config with the last saved configuration|
|[dhcp43](dhcp43)|Script to generate option 43 configuration to use with EXOS ZTP|
|[EAPS Checker](eaps_checker)|This script will check eaps config and status from a PC/Server.|
|[EDP and port VLAN Diff](edp_vlan_check)|This Script uses EDP to check if the local and remote port have the same vlans added to the ports.|
|[Enable Features Check](enablefeaturescheckpy)|Identifies the features enabled on a switch|
|[Email event](Email_event)|This EXOS script will send an email when an event is logged|
|[FDB OUI ](fdb_oui)|Scans the FDB table and reports the vendor of the device connected.|
|[Flow Tracker](flowtracker)|Creates a dynamic ACL to count packets.|
|[IOS to Policy](IOStoPolicy)|IOS ACL to EXOS policy converter.|
|[LAGutil](LAGUtil)|Shows the combined utilization for all ports in each loadshare/LAG.|
|[Show LAG](showlag)|Shows statistics, rxerrors, txerrors, utilization for loadshare/LAGs.|
|[List_Compress](list_compress)|This script takes a string of numerical values and compresses them into a string of condensed ranges.|
|[MIB View](mibview)|Converts a MIB view defined with asterisks to the mask notation used in EXOS configuration.|
|[MLAG config check](mlag_config_check)|Checks to ensure that all VLANs on MLAG ports are also present on the ISC.|
|[MLAG config compare](mlag_config_compare)|Check your MLAG config by comparing this script output from both MLAG peers. |
|[NON-stacking config converter](non_stacking_config_converter)|Converts a non stacking configuration to a stacking configuration.|
|[Convert Port Config](convert_port_config)| Allows you the option to translate a slot:port style config to standard port notation or to change port configs per slot.|
|[QOS Config Wizard](qosconfigpy)|Wizard to aid in creating QoS profiles|
|[Port Statistics Ssummary](portsum)|Display a consolidated port statistics table|
|[Radius mgmt config](radiusmgmtconfigpy)|Wizard for configuring an ExtremeXOS(TM) switch with RADIUS management information.|
|[Radius NetLogin config](radiusnetloginconfigpy)|Wizard for configuring an ExtremeXOS(TM) switch for RADIUS netlogin.|
|[show config clean](show_config_clean)|Hides unused config sections from the output of "show configuration"|
|[Show vlanID](show_vid)|Shows EXOS VLANs in VID order|
|[SNMPassist](snmpassist)|Wizard for deleting and configuring SNMPv3 for an ExtremeXOS(TM) switch.|
|[SNMP v1v2 config](snmpv1v2configpy)|Wizard for SNMP V1/V2 configuration for an ExtremeXOS(TM) switch.|
|[SNTP config](sntpconfigpy)|Example for Simple Network Time Protocol (SNTP) configuration for an ExtremeXOS(TM) switch.|
|[Show port vid](show_port_vid)|This script displays the VLAN assignment and tagging configuration for all ports on the switch.|
|[VLAN ELRP Check](vlan_elrp_check)|This script will run ELRP on all VLANS on an EXOS switch running 15.6 and newer.|
|[Vlan Existence Checker](vlan_existencecheck)|Reads VID and VLAN-Name as key-value-pairs from /usr/local/cfg/vlan_list.csv (delimiter: ";") and checks the Switch for existence of those VLANs.|
|[VLAN Copy Port](vlan_copy_port)|This EXOS script will copy/move vlans from one port to another.|
|[Watch Command](watch)|Simple script that repeats a CLI command every *n* seconds|
|[JSONRPC CLI Example](jsoncli)| This python script is an example of how to interface with EXOS 21.1 using JSONRPC over HTTP/HTTPS.|
|[Remote Script Example](rmtscript)| This python script is an example of how run scripts remotely on EXOS switches running 21.1 or later over HTTP/HTTPS.|
|[EXOS Snmp DatetimeAPI](xosSnmpDatetimeAPI)| Python API that can converts EXOS last config change time to python datetime format.|
|[Fabric Attach Zero Touch Client](fa-ztc)| This script implements the ERS and VSP FA ZTC functionality on XOS|
|[ZTP Convert to Fabric Engine](ztp-convert-to-fabric-engine)| Boot universal hardware out of the box directly into VOSS as Fabric Engine|

## ExtremeScripting .lst file
This .lst file includes all of the switch .py scripts at the time of the file upload.  It can be downloaded directly to the switch with the ```download url <url> <vr>``` command.  The .lst will create a folder called gtac and add all the scripts into that folder.  Note: To run the scripts you need to cd into the gtac folder.
* [gtac-v1.lst](gtac-v1.lst)
