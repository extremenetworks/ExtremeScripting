# Release notes for Workflow **Sync_PVI_to_Policy_Mappings**
### written by:   Markus Nikulski
### e-mail:       mnikulski@extremenetworks.com
### date:         03. February 2025

| Build | Description |
| ------------- | ------- |
|24.10.13.5v342|
new features
	• add non VLAN/I-SID support, no VLAN Islands required anymore
	• remove Debug LOG form user input dialog, keep it true by defaulr
maintenance
	• optimise common rutines using copression, fix issue with version tracking
	• cleanup debug messages across the workflow
	• dump emc_vars to debug folder
	• update documentation
fixed issues
	• compare existing policy mappings with indetned config faild if policy mapping are empty|
|24.10.13.5v319|
new features
	• support now multible NAC engine groups
	• enable/disable enforec NAC
maintenance
	• expand Debug LOG messages
fixed issues
|

|24.10.11.15v311|
new features
	• add multicast support
	• enable/disable enforec NAC
maintenance
	expand Debug LOG messages
	• update documentation
fixed issues
	• default NAC Radius Config Attribute support multiple records comma-separated 
	• enforcement fails under some circumstances
	• empty VLAN Policy location causes issues
	• private VLAN support
	• multiple VLAN, I-SID bindis (REGEX issue in update Policy Mappings)
	• I-SID name not working
|