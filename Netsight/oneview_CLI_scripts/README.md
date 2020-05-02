# How To
## XMC version 8.0
* Import the sctript = In the Extreme Management Center -> Administration -> Scripting  -> Import...
* Execute the script = In the Extreme Management Center -> Network -> Devices -> choose group -> select more devices -> Right click -> Scripts -> ...
## XMC version 8.1.2 and newer
* Import the sctript = In the Extreme Management Center -> Tasks -> Scrips  -> Import...
* Execute the script = In the Extreme Management Center -> Network -> Devices -> choose group -> select more devices -> Right click -> Tasks -> ...

## Prompt handling
Some devices do answer with unexpected prompt. For such devices you can create `appdata/scripting/myCLIRules.xml` (no reboot is required). The myCLIRules.xml "Rule name" must match the Vendor Profiles -> CLI Rules File Name variable. Vendor Profiles are inherited, you can configure the variable for whole family.

| Device        | myCLIRules.xml | CLI Rules File Name |
|:-------------:| -------------- | ------------------- |
|HPE Comware/H3C|[myCLIRules.xml](xml/comware/myCLIRules.xml?raw=true)|[comware](xml/comware/VendorProfilesComware.png?raw=true)|


# Extreme Management Center version 8.0+ Scripts
## EXOS scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| EXOS |[Create EAPS ](xml/Create_EAPS.xml?raw=true)|Creates the ring, assign selected ports as ring ports, confirue one switch as master and all other switches are transit nodes.|TCL|
| EXOS |[Create EAPS control VLAN](xml/Create_EAPS_control_VLAN.xml?raw=true)| If the vlan does not exist it does create the vlan, it add the vlan to the EAPS as control. Control vlan is configured as tagged on all EAPS ring ports.|TCL|
| EXOS |[Create EAPS protected VLAN](xml/Create_EAPS_protected_VLAN.xml?raw=true)|Add vlan to the EAPS as protected. If the vlan does not exits then it creates it. Selected ports are added as tagged or untagged. If there is only one EAPS ring then you do not need to specify the EAPS ring name. Ring ports are added as tagged automatically.|TCL|
| EXOS |[Authentication EXOS](xml/Authentication_EXOS.xml?raw=true)|Script does create NetLogin vlan (if does not exist), configure NetLogin on ports and configure Radius on EXOS devices.|TCL|
| EXOS |[ZTP+ Remove Redundant IPs](xml/Remove_redundant_IPs.xml?raw=true)|During the ZTP+ process the switch can learn multip IPs from the DHCP server. This script can be executed after the EXOS device is onboarded and it does remove IPs from EXOS not registered in XMC. Configure Site Actions to execute this script as part of ZTP+ process.|Python|

## Fabric Connect and Fabric Attach scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| VOSS |[Configuration of a Cluster (vIST)](xml/Fabric_Cluster_Create.xml?raw=true)|Cluster is created. You need their system-id before executing the script. Script must be executed one unit at a time. This script will disable/enable ISIS = it can disrupt traffic!|Python|
| VOSS |[Configuring FA Server on BEBs](xml/FAServer_Create.xml?raw=true)|FA Server configuration|Python|
| VOSS, EXOS, BOSS |[L2VSN](xml/L2VSN.xml?raw=true)|This script provisions a L2VSN between several BEBs running VOSS (VSP switches) and/or FA switches (EXOS/BOSS). It can create a VLAN and associate the provided UNI port/mlt to it, making the necessary checks (FA enabled on it or not) but it doesn't create the MLT itself.|Python|
| VOSS, EXOS, BOSS |[Create L2VSN](xml/Create_L2VSN.xml?raw=true)|This script provisions a L2VSN between any Fabric Connect or Fabric Attach switch. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS, EXOS, BOSS |[Delete L2VSN](xml/Delete_L2VSN.xml?raw=true)|This script deletes existing L2VSN services. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS, EXOS, BOSS |[Create L2VSN port context](xml/Create_L2VSN-port_context.xml?raw=true)|This script provisions a L2VSN between any Fabric Connect or Fabric Attach switch. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS, EXOS, BOSS |[Delete L2VSN port context](xml/Delete_L2VSN-port_context.xml?raw=true)|This script deletes a L2VSN between any Fabric Connect or Fabric Attach switch. It works across all of VOSS VSPs (including in DVR Leaf mode), BOSS ERS and EXOS.|Python|
| VOSS |[Create L2VSN range](xml/Create_L2VSN_Range.xml?raw=true)|This script provisions a range of L2VSNs on Fabric Connect VSPs using Switched-UNI.|Python|
| VOSS |[Delete L2VSN range](xml/Delete_L2VSN_Range.xml?raw=true)|This script deletes existing L2VSN services. It works with VOSS VSPs in Switched-UNI mode only.|Python|
| VOSS |[Create L3VSN](xml/Create_L3VSN.xml?raw=true)|This script provisions a L3VSN, which includes VRF,IPVPN,VLAN,IP configuration.|Python|
| VOSS |[Delete L3VSN](xml/Delete_L3VSN.xml?raw=true)|This script deletes a L3VSN, which includes VRF,IPVPN,VLAN,IP configuration.|Python|
## Multivendor scripts and others
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| EXOS, IOS |[Configure Vlan on the Port Cisco-Extreme](xml/Configure_Vlan_on_the_Port-Cisco-Extreme.xml?raw=true)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script does create the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2|TCL|
| EXOS, IOS, Comware OS, Procurve |[Configure Vlan on the Port Extreme-Cisco-Comware-Procurve](xml/Configure_Vlan_on_the_Port-Extreme-Cisco-Comware-Procurve.xml?raw=true)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script does create the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2. Tested on Comware 7.1.045. Tested on Procurve H.10.119|TCL|
| IOS |[Authentication Catalyst](xml/Authentication_Catalyst.xml?raw=true)|Script will configure Radius and authentication on Catalyst devices & ports.|TCL|
| IOS |[Authentication Catalyst - unconfigure](xml/Authentication_Catalyst_unconfigure.xml?raw=true)|Script will UNconfigure Radius and authentication on Catalyst devices & ports.|TCL|
| BOSS |[Authentication BOSS](xml/Authentication_BOSS.xml?raw=true)|Script does configure authentication on ports and configure Radius on BOSS based devices (ERS family). [Details](Authentication_BOSS.md)|TCL|
| BOSS |[VLAN Provisioning BOSS](xml/VLAN_Provisioning_BOSS.xml?raw=true)|Script does create vlans on  BOSS based devices (ERS family).|Python|
| BOSS |[ERS NAC Enforce](xml/ERS_NAC_Enforce.xml?raw=true)|This script allows the XMC operator to easily configure an ERS switch based on the ExtremeControl NAC configuration. The script will automatically configure all of the following: Primary and Secondary RADIUS Servers, including shared secret.RADIUS accounting, if enabled in XMC switch config. RADIUS dynamic-client (RFC3576 Change-of-Authorization). NTP or SNTP configuration to match that of the XMC Server, including the right timezone. (RFC3576 Change-of-Authorization requires the switch and server to have the same time). RADIUS reachability, if specified by user. EAPoL global and port level configuration. If the port selection included FA Client ports and these are to be filtered out, these ports will have EAPoL expressly disabled on them. Fabric Attach is always enabled on the ports. Spanning Tree FastStart or Edge configuration is always set on the ports|Python|
| VOSS |[Automatic Fabric Creation](xml/FC_Config.xml?raw=true)|Select group of switches with the same NNI portlist, specify some basic parameters.|Python|
| VOSS |[Authentication VOSS](xml/Authentication_VOSS.xml?raw=true)|Configure radius server and accounting for management access.|TCL|
| VOSS |[VSP EPT Enforce](xml/VSP_EPT_Enforce.xml?raw=true)|This script allows the XMC operator to easily configure a VSP switch for Endpoint-Tracking (EPT) based on the ExtremeControl NAC configuration.|Python|
| Procurve |[Authentication Procurve](xml/Authentication_Procurve.xml?raw=true)|Script will configure Radius and authentication on Procurve devices & ports.|TCL|
| Linux |[NAC Daemon Commands](xml/NAC_Daemon_Control.xml?raw=true)|Script does stop - start - restart - status the nacctl.|TCL|

# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).
>Be Extreme
