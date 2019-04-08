# How To
## Workflows are available from XMC version 8.1.5 as beta feature. Fully supported in XMC version 8.2 GA
* Import the sctript = In the Extreme Management Center OneView -> Tasks -> Workflow -> Import...

# Extreme Management Center Workflows
| Workflow name   | Description   | Comment |
| ------------- | ------------- | ------ |
|[Send System Time by Email](xwf/Send_SystemTime_by_Email-8.2.1.56v22.xwf?raw=true)|Gather system time from group of EXOS devices sequentially and aggregated result is sent by email.|Configure the email recipients before executing.|
|[Investigate End-System history](xwf/Investigate_End-System_history-8.2.4.55v46.xwf?raw=true)|Prompt for MAC or Username and for time range. Workflow does create table of end-system events in the database and send it by email.|Configure the email recipients before executing. Variable InstallDirectory is referring to the XMC installation path.|
|[Uptime and Tech Support](xwf/Uptime_and_Tech_Support-8.2.3.67v84.xwf?raw=true)|Does check the uptime of each device. If the uptime is lower then configured value and the device is not in maintenance then the workflow does gather tech support information and send email|Configure the variable and email destination.|
|[Gather Show Support based on alarm](xwf/Gather_Show_Support-8.2.3.67v11.xwf?raw=true)|Gather show support information based on information from alarm. Generate alarm with details|Configure the email destination. Create Alarm to execute this workflow|
|[Update Device Notes - Group Membership](xwf/Update_Device_Notes-Group_Membership-8.2.4.24v13.xwf?raw=true)|The workflow does modify device property to reflect groups the device belong to.|Modify the Inputs to define what property you want to modify and what prefix you want to use. Run the workflow and save it as task. Schedule the task for periodic execution.|
|[GDPR - Delete end-system from ExtremeControl](xwf/GDPR-Delete_End-System-8.2.4.41v6.xwf?raw=true)|This workflow does delete End-System with specified MAC from the database.|Various MAC address formats are accepted: lowercase, uppercase, dot delimited, colon delimited, dash delimited, not delimited|
|[GDPR - Delete from ExtremeControl](xwf/GDPR-Delete-8.2.4.41v4.xwf?raw=true)|This workflow does delete End-System with specified MAC or Username from the database.|Various MAC address formats are accepted: lowercase, uppercase, dot delimited, colon delimited, dash delimited, not delimited. Domain is not mandatory in the username.|


# Support
_The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

Issues and/or bug fixes may be reported on [The Hub](https://community.extremenetworks.com).
>Be Extreme
