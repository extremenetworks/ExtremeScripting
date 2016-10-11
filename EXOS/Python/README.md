# Documentation
* [Python Getting Started Guide](http://www.extremenetworks.com/wp-content/uploads/2015/02/Python_Getting_Started_Guide.pdf)
* [The EXOS Python API](http://documentation.extremenetworks.com/python/)

<!---
------git_dlownload.py------
To allow git_download.py to find the scripts you need
to add the script to this list with no spaces for the table like autofsbackup does.
-->

# Python Scripts
| Script name   | Description   |
| ------------- |:-------------:|
| [GitHub Script Downloader](git_download)| Downloads python scripts located on this page directly to your switch.|
|[Automatic Backup](autofsbackuppy)|Runs automated back up on all scripts, including configuration, policy and scripts.|
|[Clean Switch](cleanswitch)|Provides a method of deleting all configuration parameters and files from an EXOS switch.|
|[Config Diff](conf_diff)|Script to compare the current running config with the last saved configuration|
|[dhcp43](dhcp43)|Script to generate option 43 configuration to use with EXOS ZTP|
| [EAPS Checker](eaps_checker)|This script will check eaps config and status from a PC/Server.|
|[EDP and port VLAN Dif](edp_and_port_vlan_check)|This Script uses EDP to check if the local and remote port have the same vlans added to the ports.|
|[Enable Features Check](enablefeaturescheckpy)|Identifies the features enabled on a switch|
|[Email event](Email_event)|This EXOS script will send an email when an event is logged|
|[FDB OUI ](fdb_oui)|Scans the FDB table and reports the vendor of the device connected.|
|[Flow Tracker](flowtracker)|Creates a dynamic ACL to count packets.|
| [IOS to Policy](IOStoPolicy)|IOS ACL to EXOS policy convertor.|
|[MLAG config check](mlag_config_check)|Checks to ensure that all VLANs on MLAG ports are also present on the ISC.|
|[NON-stacking config converter](non_stacking_config_converter)|Converts a non stacking configuration to a stacking configuration.|
|[QOS Config Wizard](qosconfigpy)|Wizard to aid in creating QoS profiles|
|[Radius mgmt config](radiusmgmtconfigpy)|Wizard for configuring an ExtremeXOS(TM) switch with RADIUS management information.|
|[Radius NetLogin config](radiusnetloginconfigpy)|Wizard for configuring an ExtremeXOS(TM) switch for RADIUS netlogin.|
|[show config clean](show_config_clean)|Hides unused config sections from the output of "show configuration"|
|[Show vlanID](show_vid)|Shows EXOS VLANs in VID order|
|[SNMPassist](snmpassist)|Wizard for deleting and configuring SNMPv3 for an ExtremeXOS(TM) switch.|
|[SNMP v1v2 config](snmpv1v2configpy)|Wizard for SNMP V1/V2 configuration for an ExtremeXOS(TM) switch.|
|[SNTP config](sntpconfigpy)|Example for Simple Network Time Protocol (SNTP) configuration for an ExtremeXOS(TM) switch.|
|[Show port vid](show_port_vid)|This script displays the VLAN assignment and tagging configuration for all ports on the switch.|
|[VLAN ELRP Check](vlan_elrp_check)|This script will run ELRP on all VLANS on an EXOS switch.|
|[VLAN Copy Port](vlan_copy_port)|This EXOS script will copy/move vlans from one port to another.|
|[Watch Command](watch)|Simple script that repeats a CLI command every *n* seconds|
| [JSONRPC CLI Example](jsoncli)| This python script is an example of how to interface with EXOS 21.1 using JSONRPC over HTTP/HTTPS.|
