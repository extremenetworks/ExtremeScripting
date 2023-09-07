# How To
## XMC version 8.0
* Import the sctript = Open the web GUI -> Administration -> Scripting  -> Import...
* Execute the script = Open the web GUI -> Network -> Devices -> choose group -> select more devices -> Right click -> Scripts -> ...
## XIQ Site Engine and XMC version 8.1.2 - 8.5.2
* Import the sctript = Open the web GUI -> Tasks -> Scrips  -> Import...
* Execute the script = Open the web GUI -> Network -> Devices -> choose group -> select more devices -> Right click -> Tasks -> ...

## Prompt handling
Some devices do answer with unexpected prompt. For such devices you can create `appdata/scripting/myCLIRules.xml` (no reboot is required). The myCLIRules.xml "Rule name" must match the Vendor Profiles -> CLI Rules File Name variable. Vendor Profiles are inherited, you can configure the variable for whole family.

| Device        | myCLIRules.xml | CLI Rules File Name |
|:-------------:| -------------- | ------------------- |
|HPE Comware/H3C|[myCLIRules.xml](xml/comware/myCLIRules.xml)|[comware](xml/comware/VendorProfilesComware.png)|


# XIQ Site Engine and Extreme Management Center version 8.0+ Scripts
## XMC scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| n/a |[Retrieve Script Log](xml/Retrieve_Script_Log.xml)| This script does for XMC scripts what Workflow Dashboard does for workflows. Once the script window is closed, it is hard to go back and see the script output (one has to go and look to XMC's Linux file system). To find a past script log, simply run this script against the switch (or switches) where the seeked script was previously executed. If no inputs are provided the script will list all script logs which were executed against the same switch IP, together with the relative timestamp. Once spotted the desired log, simply hit Back, enter the script name and timestamp and run again. If only 1 matching script log is found, then the script log is dumped in the script window. If no sript logs are found then this script intentionally raises an exception so as to get a red cross next to the device indicating no hit|Python|
| n/a |[CLI Custom Action script](xml/CLI_Custom_Action_script.xml)| A simple CLI script cannot be assigned to Site Actions tab Custom Actions table. This Python script allows a simple list of CLI commands, provided at the very beginning of this script file, to be executed, and this script can be assigned to Site Actions tab Custom Actions table because it is a Python script. Optionally a flag can be set (True or False) to determine what to do if a command produces an error on the switch. If set to False, all remaining commands will be sent anyway; if set to True, then remaining commands will not be sent. The CLI script can include references to site custom variables using syntax ${<site-custom-variable>}. The site of the selected switch will apply. If a variable is not found in the site of the switch, then the variable is looked up in the parent sites all the way up to /World. If it is not found in any of the parent sites then the global version of the variable will be used; and if the variable is not found anywhere then the script will error|Python|
## EXOS scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| EXOS |[Create EAPS ](xml/Create_EAPS.xml)|Creates the ring, assign selected ports as ring ports, confirue one switch as master and all other switches are transit nodes.|TCL|
| EXOS |[Create EAPS control VLAN](xml/Create_EAPS_control_VLAN.xml)| If the vlan does not exist it creates the vlan, it add the vlan to the EAPS as control. Control vlan is configured as tagged on all EAPS ring ports.|TCL|
| EXOS |[Create EAPS protected VLAN](xml/Create_EAPS_protected_VLAN.xml)|Add vlan to the EAPS as protected. If the vlan does not exits then it creates it. Selected ports are added as tagged or untagged. If there is only one EAPS ring then you do not need to specify the EAPS ring name. Ring ports are added as tagged automatically.|TCL|
| EXOS |[Authentication EXOS](xml/Authentication_EXOS.xml)|Script creates NetLogin vlan (if does not exist), configure NetLogin on ports and configure Radius on EXOS devices.|TCL|
| EXOS |[ZTP+ Remove Redundant IPs](xml/Remove_redundant_IPs.xml)|During the ZTP+ process the switch can learn multip IPs from the DHCP server. This script can be executed after the EXOS device is onboarded and it removes IPs from EXOS not registered in XMC. Configure Site Actions to execute this script as part of ZTP+ process.|Python|
| EXOS |[Password change](xml/Exos_Password_Change.xml)|Script changes password on EXOS switches. Enter the username, current password and new password.|Python|
## VOSS scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| VOSS |[Move to CLIP Mgmt IP](xml/Move_to_CLIP_Mgmt_IP.xml)| Given a switch already in XMC, this script will ask user to provide a CLIP IP and VRF which will then be configured as mgmt clip on the VSP. If the VSP already had a mgmt clip the existing mgmt clip will be deleted and replaced with the new one. If the switch had a mgmt vlan IP, this can also be deleted, based on script input. At the same time, the switch can be renamed, both under SNMP and ISIS. Finally the switch is deleted from XMC's database as well as XMC Control if there, and re-added to the same site with the new mgmt IP address. Before attempting to change the IP on the switch, the script will first of all make sure that the new IP address provided is not already known by XMC and that it does not exist on the network (does not reply to ping). v1.9|Python|
| VOSS |[SMLT Pair Enforce](xml/SMLT_Pair_Enforce.xml)| This script provisions and enforces SMLT vIST clustering on VSP devices including if these are operating in DVR Leaf mode both via inband and OOB management|Python|
| VOSS |[read license](xml/read_VOSS_license.xml)| This script read the license currently active on the switch. Select only one device, doesn’t mater witch one, the script will take all VOSS switches part of the inventory and read teh data by SNMP. The result is presented like a CSV on the end of the output. |Python|
| VOSS |[deliver license](xml/deliver_VOSS_license.xml)| This script will deliver all licenses stored in /root/VOSS-Licenses/ to the corresponding switch using the bas MAC address witch have to be part of the file name. This applies to the universal VOSS only. |Python|
## ERS scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| BOSS |[Enable/Disable remote access through EDM](xml/Enable-Disable_Remote_Access_through_EDM.xml)|Script generate HTTP(s) call to EDM to Enable/Disable access to the ERS through telnet/ssh|Python|


## Fabric Connect and Fabric Attach scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| VOSS |[Configuration of a Cluster (vIST)](xml/Fabric_Cluster_Create.xml)|Cluster is created. You need their system-id before executing the script. Script must be executed one unit at a time. This script will disable/enable ISIS = it can disrupt traffic!|Python|
| VOSS |[Configuring FA Server on BEBs](xml/FAServer_Create.xml)|FA Server configuration|Python|
| VOSS, EXOS, BOSS |[L2VSN](xml/L2VSN.xml)|This script provisions a L2VSN between several BEBs running VOSS (VSP switches) and/or FA switches (EXOS/BOSS). It can create a VLAN and associate the provided UNI port/mlt to it, making the necessary checks (FA enabled on it or not) but it doesn't create the MLT itself.|Python|
| VOSS, EXOS, BOSS |[Create L2VSN](xml/Create_L2VSN.xml)|This script provisions a L2VSN between any Fabric Connect or Fabric Attach switch. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS, EXOS, BOSS |[Delete L2VSN](xml/Delete_L2VSN.xml)|This script deletes existing L2VSN services. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS, EXOS, BOSS |[Create L2VSN port context](xml/Create_L2VSN-port_context.xml)|This script provisions a L2VSN between any Fabric Connect or Fabric Attach switch. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS, EXOS, BOSS |[Delete L2VSN port context](xml/Delete_L2VSN-port_context.xml)|This script deletes a L2VSN between any Fabric Connect or Fabric Attach switch. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS |[Create L2VSN range](xml/Create_L2VSN_Range.xml)|This script provisions a range of L2VSNs on Fabric Connect VSPs using Switched-UNI.|Python|
| VOSS |[Delete L2VSN range](xml/Delete_L2VSN_Range.xml)|This script deletes existing L2VSN services. It works with VOSS VSPs in Switched-UNI mode only.|Python|
| VOSS |[Create L3VSN](xml/Create_L3VSN.xml)|This script provisions a L3VSN, which includes VRF,IPVPN,VLAN,IP configuration.|Python|
| VOSS |[Delete L3VSN](xml/Delete_L3VSN.xml)|This script deletes a L3VSN, which includes VRF,IPVPN,VLAN,IP configuration.|Python|

## Multivendor scripts and others
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| EXOS, IOS |[Configure Vlan on the Port Cisco-Extreme](xml/Configure_Vlan_on_the_Port-Cisco-Extreme.xml)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script creates the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2|TCL|
| EXOS, IOS, Comware OS, Procurve |[Configure Vlan on the Port Extreme-Cisco-Comware-Procurve](xml/Configure_Vlan_on_the_Port-Extreme-Cisco-Comware-Procurve.xml)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script creates the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2. Tested on Comware 7.1.045. Tested on Procurve H.10.119|TCL|
| IOS |[Authentication Catalyst](xml/Authentication_Catalyst.xml)|Script will configure Radius and authentication on Catalyst devices & ports.|TCL|
| IOS |[Authentication Catalyst - unconfigure](xml/Authentication_Catalyst_unconfigure.xml)|Script will UNconfigure Radius and authentication on Catalyst devices & ports.|TCL|
| BOSS |[Authentication BOSS](xml/Authentication_BOSS.xml)|Script does configure authentication on ports and configure Radius on BOSS based devices (ERS family). [Details](Authentication_BOSS.md)|TCL|
| BOSS |[VLAN Provisioning BOSS](xml/VLAN_Provisioning_BOSS.xml)|Script creates vlans on  BOSS based devices (ERS family).|Python|
| BOSS |[ERS NAC Enforce](xml/ERS_NAC_Enforce.xml)|This script allows the XMC operator to easily configure an ERS switch based on the ExtremeControl NAC configuration. The script will automatically configure all of the following: Primary and Secondary RADIUS Servers, including shared secret.RADIUS accounting, if enabled in XMC switch config. RADIUS dynamic-client (RFC3576 Change-of-Authorization). NTP or SNTP configuration to match that of the XMC Server, including the right timezone. (RFC3576 Change-of-Authorization requires the switch and server to have the same time). RADIUS reachability, if specified by user. EAPoL global and port level configuration. If the port selection included FA Client ports and these are to be filtered out, these ports will have EAPoL expressly disabled on them. Fabric Attach is always enabled on the ports. Spanning Tree FastStart or Edge configuration is always set on the ports|Python|
| VOSS |[Automatic Fabric Creation](xml/FC_Config.xml)|Select group of switches with the same NNI portlist, specify some basic parameters.|Python|
| VOSS |[Authentication VOSS](xml/Authentication_VOSS.xml)|Configure radius server and accounting for management access.|TCL|
| VOSS |[VSP EPT Enforce](xml/VSP_EPT_Enforce.xml)|This script allows the XMC operator to easily configure a VSP switch for Endpoint-Tracking (EPT) based on the ExtremeControl NAC configuration.|Python|
| VOSS |[VSP PreUpgrade CleanUp](xml/VOSS_PreUpgrade_CleanUp.xml)|Script prepares a VSP or XA1400 for an XMC upgrade, by removing old software versions from the software archive. v1.1|Python|
| Procurve |[Authentication Procurve](xml/Authentication_Procurve.xml)|Script will configure Radius and authentication on Procurve devices & ports.|TCL|
| Linux |[NAC Daemon Commands](xml/NAC_Daemon_Control.xml)|Script does stop - start - restart - status the nacctl.|TCL|

## Integrated Application Hosting (Insight VM) scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| VOSS, EXOS |[Delete Insight VMs](xml/Delete_Insight_VMs.xml)|Given an insight capable VOSS or EXOS switch, removes all insight VMs from it. The VMs, if any, are stopped and deleted from the switch config file. The VM files (OVA/QCOW) are also deleted if the pull down to this effect is enabled. v1.2|Python|


# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).
>Be Extreme
