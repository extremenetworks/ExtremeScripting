# How To
## XMC version 8.0
* Import the sctript = In the Extreme Management Center -> Administration -> Scripting  -> Import...
* Execute the script = In the Extreme Management Center -> Network -> Devices -> choose group -> select more devices -> Right click -> Scripts -> ...
## XMC version 8.1.2 and 8.1.3
* Import the sctript = In the Extreme Management Center -> Tasks -> Scrips  -> Import...
* Execute the script = In the Extreme Management Center -> Network -> Devices -> choose group -> select more devices -> Right click -> Tasks -> ...

## Prompt handling
Some devices do answer with unexpected prompt. For such devices you can create `appdata/scripting/myCLIRules.xml` (no reboot is required). The myCLIRules.xml "Rule name" must match the Vendor Profiles -> CLI Rules File Name variable. Vendor Profiles are inherited, you can configure the variable for whole family.

| Device        | myCLIRules.xml | CLI Rules File Name |
|:-------------:| -------------- | ------------------- |
|HPE Comware/H3C|[myCLIRules.xml](xml/comware/myCLIRules.xml?raw=true)|[comware](xml/comware/VendorProfilesComware.png?raw=true)|

# Extreme Management Center version 8.0+ Scripts
| OS | Script name   | Description   | Type   |
| -- | ------------- | ------------- |:------:|
| EXOS, IOS |[Configure Vlan on the Port Cisco-Extreme](xml/Configure_Vlan_on_the_Port-Cisco-Extreme.xml?raw=true)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script does create the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2|TCL|
| EXOS, IOS, Comware OS |[Configure Vlan on the Port Extreme-Cisco-Comware](xml/Configure_Vlan_on_the_Port-Extreme-Cisco-Comware.xml?raw=true)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script does create the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2. Tested on Comware 7.1.045|TCL|
| EXOS |[Create EAPS ](xml/Create_EAPS.xml?raw=true)|Creates the ring, assign selected ports as ring ports, confirue one switch as master and all other switches are transit nodes.|TCL|
| EXOS |[Create EAPS control VLAN](xml/Create_EAPS_control_VLAN.xml?raw=true)| If the vlan does not exist it does create the vlan, it add the vlan to the EAPS as control. Control vlan is configured as tagged on all EAPS ring ports.|TCL|
| EXOS |[Create EAPS protected VLAN](xml/Create_EAPS_protected_VLAN.xml?raw=true)|Add vlan to the EAPS as protected. If the vlan does not exits then it creates it. Selected ports are added as tagged or untagged. If there is only one EAPS ring then you do not need to specify the EAPS ring name. Ring ports are added as tagged automatically.|TCL|
| EXOS |[Authentication EXOS](xml/Authentication_EXOS.xml?raw=true)|Script does create NetLogin vlan (if does not exist), configure NetLogin on ports and configure Radius on EXOS devices.|TCL|
| IOS |[Authentication Catalyst](xml/Authentication_Catalyst.xml?raw=true)|Script will configure Radius and authentication on Catalyst devices & ports.|TCL|
| IOS |[Authentication Catalyst - unconfigure](xml/Authentication_Catalyst_unconfigure.xml?raw=true)|Script will UNconfigure Radius and authentication on Catalyst devices & ports.|TCL|
| BOSS |[Authentication BOSS](xml/Authentication_BOSS.xml?raw=true)|Script does configure authentication on ports and configure Radius on BOSS based devices (ERS family). [Details](Authentication_BOSS.md)|TCL|
| VOSS |[(almost) Zero Touch Fabric](xml/aZTF.xml?raw=true)|It finds automatically the NNI ports, Creates & configures the Fabric dynamically, No user input necessary, all automated, Takes ~1mn to execute (30’’ are spent for LLDP).|Python|
| VOSS |[Automatic Fabric Creation](xml/FC_Config.xml?raw=true)|Select group of switches with the same NNI portlist, specify some basic parameters.|Python|
| VOSS |[Configuration of a Cluster (vIST)](xml/Fabric_Cluster_Create.xml?raw=true)|Cluster is created. You need their system-id before executing the script. Script must be executed one unit at a time. This script will disable/enable ISIS = it can disrupt traffic!|Python|
| VOSS |[Configuring FA Server on BEBs](xml/FAServer_Create.xml?raw=true)|FA Server configuration|Python|
| BOSS, EXOS |[L2VSN between FA Proxy](xml/FA_L2VSN_Create.xml?raw=true)|Provisioning a L2VSN between FA Proxy|Python|
| VOSS |[L2VSN between BEBs](xml/L2VSN.xml?raw=true)|Provisioning a L2VSN between BEBs. It can create a VLAN and associate the provided UNI port/mlt to it, making the necessary checks (FA enabled on it or not) but it doesn't create the MLT itself.|Python|

# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/extreme).
>Be Extreme
