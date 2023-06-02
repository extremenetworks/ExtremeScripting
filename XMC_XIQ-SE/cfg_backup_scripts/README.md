# Reference Material
* [TEMPLATE FILE for creating Device Family Definition files](script_template.txt)
* [How to import this script?](https://extremeportal.force.com/ExtrArticleDetail?an=000091050&q=What-directory-do-you-put-custom-device-type-scripts-Inventory-Manger)
* [How to chose what script should be used?](https://emc.extremenetworks.com/content/oneview/docs/network/devices/docs/c_ov_at_firmware_mib_config.html)


# XIQ Site Engine - Extreme Management Center Scripts
| Script name   | Description   |
| ------------- | ------------- |
|[Avaya ERS8xxx](ERS8K-TFTP-BACKUP.txt?raw=true)|Configuration backup and restore of Nortel/Avaya ERS8000 family. Restore works only single CPU platforms.|
|[Barracuda F-Series](Barracuda-SCP.txt?raw=true)|Configuration backup/restore of Barracuda NG Firewall F-Series.|
|[Cambium cnMatrix](Cambium_TFTP.txt?raw=true)|Configuration backup for Cambium Networks cnMatrix Series device.|
|[Cisco Catalyst](CiscoCatalyst-withRestore-TFTP.txt?raw=true)|Configuration backup/restore for Cisco Catalyst.|
|[Cisco Catalyst](CiscoSG500-TFTP.txt?raw=true)|Configuration backup for Cisco SG500.|
|[Cisco Firmware 2xxx TAR](CiscoCatalyst2xxx_firmware_from_tar.txt?raw=true)|Configuration backup and restore and FW upgrade and reset for Cisco Catalyst 2xxx. TAR file not BIN. Can take 30 minutes based on platform. Be patient.|
|[Cisco Catalyst 9200](Catalyst9200.txt?raw=true)|Configuration backup and restore and FW upgrade  for Cisco Catalyst 9200.|
|[Cisco Nexus](Cisco-Nexus-TFTP.txt?raw=true)|Configuration backup and restore for Cisco Nexus.|
|[Cisco Nexus SCP](CiscoNexus_xtrm_v2.txt?raw=true)|Configuration backup and restore for Cisco Nexus through SCP.|
|[Cisco Router SCP](Cisco-Router-SCP.txt?raw=true)|config backup+restore, firmware+bootrom download, reset, timed reset, timed reset abort for Cisco Routers. See comments in script for details.|
|[Cisco Router TFTP](Cisco-Router-TFTP.txt?raw=true)|config backup+restore, firmware+bootrom download, reset, timed reset, timed reset abort for Cisco Routers. See comments in script for details.|
|[Cisco WLC 5500](Cisco_WLC_5500?raw=true)|Configuration backup of Cisco WLC 5500.|
|[Dell Blade Switch](Dell_Blade_switch.txt?raw=true)|Configuration backup of Dell Blade Switch.|
|[Dell Force10](dell-force10?raw=true)|Configuration backup of Dell Force10.|
|[Extreme BR69xx](BR69xx.txt?raw=true)|Configuration backup and restore and restart of Brocade/Extreme BR69xx.|
|[Extreme IQEngine](Extreme-Cloud-AP-TFTP.txt?raw=true)|Configuration backup for Aerohive HiveOS, Extreme IQEngine.|
|[FortiGate Firewall](FortiGate?raw=true)|Configuration backup of FortiGate.|
|[FortiWLC controller](FortiWLC-FTP.txt?raw=true)|Configuration backup/restore over FTP of FortiWLC / Meru wireless controller. If your FTP server does support chroot then you may need to change %ABSOLUTE_TARGET_FILE_PATH% with %RELATIVE_TARGET_FILE_PATH%.|
|[HP Aruba Comware](Hewlett_Packard_Comware-TFTP?raw=true)|Configuration backup/restore & firmware upgrade of Comware 5100.|
|[HP Aruba Comware](HPE_H3C_Comware_5_Switch.txt?raw=true)|Backup and restore HPE H3C Comware 5.x switches.|
|[HP Aruba Comware](HPE_H3C_Comware_7_Switch.txt?raw=true)|Backup and restore HPE H3C Comware 7.x switches.|
|[HP Aruba ArubaOS-CX](Hewlett_Packard_ArubaOS-CX-TFTP-MGMT.txt?raw=true)|Backup and restore HPE ArubaOS-CX through MGMT vrf. Reboot is also supported.|
|[HP Aruba ArubaOS-CX](Hewlett_Packard_ArubaOS-CX-TFTP-Default.txt?raw=true)|Backup and restore HPE ArubaOS-CX through Default vrf. Reboot is also supported.|
|[HP Aruba](Hewlett_Packard-SFTP.txt?raw=true)|Backup and restore, firmware upgrade and reboot for [HPE switches](Hewlett_Packard-SFTP-info.txt).|
|[Juniper EX SCP](juniper_EX-SCP?raw=true)|Configuration backup/restore of Juniper EX over SCP.|
|[Juniper EX TFTP](juniper_EX-TFTP?raw=true)|Configuration backup/restore of Juniper EX over TFTP.|
|[Microsens G6](Microsens_G6-TFTP.txt?raw=true)|Configuration backup/restore over TFTP, firmware upgrade & reboot of Microsens G6.|
|[Palo Alto firewalls](Palo_Alto_SCP_Script?raw=true)|Configuration backup of Palo Alto firewall over SCP. PanOS 8|
|[Palo Alto firewalls](Palo_Alto_SCP_Script_PanOS9?raw=true)|Configuration backup of Palo Alto firewall over SCP. PanOS 9|
|[Ubiquiti EdgeRouter](EdgOS?raw=true)|Configuration backup of Ubiquiti EdgeRouter over TFTP.|
|[Zyxel switch](Zyxel-TFTP.txt?raw=true)|Configuration backup/restore of Zyxel switch over TFTP. CLI and SNMP credentials are not part of the backup, update the script with your credentials.|

# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com/).
>Be Extreme
