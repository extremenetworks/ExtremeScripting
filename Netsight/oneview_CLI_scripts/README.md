# How To
## XMC version 8.0
* Import the sctript = In the Extreme Management Center -> Administration -> Scripting  -> Import...
* Execute the script = In the Extreme Management Center -> Network -> Devices -> choose group -> select more devices -> Right click -> Scripts -> ...
## XMC version 8.1.2
* Import the sctript = In the Extreme Management Center -> Tasks -> Scrips  -> Import...
* Execute the script = In the Extreme Management Center -> Network -> Devices -> choose group -> select more devices -> Right click -> Tasks -> ...


# Extreme Management Center version 8.0+ Scripts
| Script name   | Description   | Type   |
| ------------- |:-------------:| ------ |
|[Configure Vlan on the Port Cisco-Extreme](xml/Configure_Vlan_on_the_Port-Cisco-Extreme.xml)|Configure vlan on ports - tagged or untagged based on request. The script check if the VLAN exists. If the vlan does not exist then the script does create the vlan. Tested on EXOS 15.3 and newer. Tested on Catalyst 12.2|TCL|
|[Create EAPS ](xml/Create_EAPS.xml)|Creates the ring, assign selected ports as ring ports, confirue one switch as master and all other switches are transit nodes.|TCL|
|[Create EAPS control VLAN](xml/Create_EAPS_control_VLAN.xml)| If the vlan does not exist it does create the vlan, it add the vlan to the EAPS as control. Control vlan is configured as tagged on all EAPS ring ports.|TCL|
|[Create EAPS protected VLAN](xml/Create_EAPS_protected_VLAN.xml)|Add vlan to the EAPS as protected. If the vlan does not exits then it creates it. Selected ports are added as tagged or untagged. If there is only one EAPS ring then you do not need to specify the EAPS ring name. Ring ports are added as tagged automatically.|TCL|
|[Authentication EXOS](xml/Authentication_EXOS.xml)|Script does create NetLogin vlan (if does not exist) configure NetLogin on ports and Radius on EXOS devices.|TCL|
|[Automatic Fabric Creation](xml/FC_Config.xml)|Select group of switches with the same NNI portlist, specify some basic parameters.|Python|
|[Configuration of a Cluster (vIST)](xml/Fabric_Cluster_Create.xml)|Cluster is created. You need their system-id before executing the script. Script must be executed one unit at a time. This script will disable/enable ISIS = it can disrupt traffic!|Python|
|[Configuring FA Server on BEBs](xml/FAServer_Create.xml)|FA Server configuration|Python|
|[L2VSN between FA Proxy](xml/FA_L2VSN_Create.xml)|Provisioning a L2VSN between FA Proxy|Python|
|[L2VSN between BEBs](xml/L2VSN.xml)|Provisioning a L2VSN between BEBs. It can create a VLAN and associate the provided UNI port/mlt to it, making the necessary checks (FA enabled on it or not) but it doesn't create the MLT itself.|Python|

>Be Extreme
