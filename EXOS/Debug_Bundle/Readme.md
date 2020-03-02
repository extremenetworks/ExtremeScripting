# Debug Bundle

## Description

The debug bundle aims to solve the problem of incomplete debug collection by creating predefined modules to common problems that can be executed when an issue occurs and can be used by all users including customers /GTAC etc.
The person just needs to have a brief idea on the issue, he/she can then search and execute a relevant bundle that matches the problem statement, the bundle would in turn assure that all the debugs are collected for the problem.
It also provides a debug infrastructure independent of EXOS releases, so that an EXOS upgrade or reboot is not needed to make use of new debug bundles that are available. Additionaly, we could also create customized debug bundles or
modify existing ones easily and dynamically for all EXOS users. 

Note: This file should be used along with the show-tech support command on EXOS. For more info on usages excute the "show tech-support help" command on EXOS.

### Files

* [Example debug_bundle.json](debug_bundle.json)
* [README.md](README.md)

### Requirements

ExtremeXOS 30.6 and later

Note: This command executes the BCM and shell debug commands only when debug-mode is enabled.

#### Download

Copy debug_bundle.json to a tftp server. tftp the file to your switch using the EXOS tftp command
Transfer the file to your PC, then use the Chalet switch web interface File Manager application to transfer the file to your switch.

#### Usage
1) first tftp the debug_bundle.json file to your switch.

`Switch.3 # tftp get 10.120.89.96 debug_bundle.json`

`Downloading debug_bundle.json to switch... done!`

2) option to see the bundles available.

sh tech-support help

***List of Bundles:***

```L2-Vpn , AAA , GPTP , MLAG , Optics , Vlan , Mpls , L2-Multicast , Netlogin , L3_Ipv4 , VRRP , LAG , L2 , Eaps , Policy , STP , ACL , OSPF , Link-issues , VPEX```
        EXAMPLE:"show tech-support bundle l2" to collect debug commands for a l2 forwarding problem

3) Execute the bundle as per your need.

sh tech-support bundle <bundle_name>

***Example:***

Switch.1 # sh tech-support bundle vlan
Bundle option might dump huge set of ouputs and should be used only for debugging purposes.
Do you want to continue? (y/N) Yes
Debug mode is not enabled. Linux shell and BCM shell commands will not be executed

Execution No:0 for module vlan

***EXOS Commands***

```
->show vlan detail
VLAN Interface with name Default created by user
    Admin State:         Enabled     Tagging:   802.1Q Tag 1
    Description:         None
    Virtual router:      VR-Default
    IP Anycast:          Disabled
    IPv4 Forwarding:     Disabled
    IPv4 MC Forwarding:  Disabled
    IPv6 Forwarding:     Enabled
    IPv6 MC Forwarding:  Disabled
    IPv6:                None
    STPD:                s0(Enabled,Auto-bind)
    Protocol:            Match all unfiltered protocols```

