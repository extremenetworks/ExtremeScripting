# Release notes for Workflow **NAC End System name to port alias**
### written by:   Markus Nikulski
### e-mail:       mnikulski@extremenetworks.com
### date:         20. March 2025

This workflow read the XIQ-SE Control end system table and use the IP address and hostname if given. Than try to do a DNS reverse lookup against the IP address. If a hostname determined, it will be written down to the switch port as alias used for this authentication. This workflow applies only to Fabric Engine (aka VSP).

| Build | Description |
| ------------- | ------- |
|25.2.11.23v53|*new features*<br> • first release<br><br>*maintenance*<br><br>*fixed issues*<br>|
