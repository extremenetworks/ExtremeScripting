# Release notes for Workflow **XIQ AP import**
### written by:   Markus Nikulski
### e-mail:       mnikulski@extremenetworks.com
### date:         06. August 2025

Import APs from XIQ to XIQ-SE and integrat the AD devicese in to Control to serve 802.1x

| Build | Description |
| ------------- | ------- |
|25.8.11.12v409|*new features*<br>	• <br><br>*maintenance*<br>	• catch any exception and redirect to the LOG file<br>	• <br><br>*fixed issues*<br> • support policy reading with paging to cover 100 instade of 10 policies<br> • delete IP from NAC failed<br> • if serial number for XIQ-SE devices not given, device will be ignored|
|25.5.12.6v393|*new features*<br>	• <br><br>*maintenance*<br>	• catch any exception and redirect to the LOG file<br>	• <br><br>*fixed issues*<br> • |
|25.5.12.6v391|*new features*<br>	• <br><br>*maintenance*<br>	• add SSL exception handler for more clear message if no trust to XIQ exists<br>	• improve XIQ reading performance<br><br>*fixed issues*<br> • |
|25.5.12.3v356|*new features*<br>	• Allow to provide different Site Access Control setting used in example for switches. The Workflow will overwrite the required attributes fitting to the cloud AP. Details please read the documentation. <br><br>*maintenance*<br>	• <br><br>*fixed issues*<br> • |
|25.5.12.3v356|*new features*<br>	• <br><br>*maintenance*<br>	• <br><br>*fixed issues*<br> • If a AP is not assigned to a location, it was causing an issue.|
|25.5.12.3v354|*new features*<br>	• Concept change using the native NAC integration. Please read the documentation for more details.<br><br>*maintenance*<br>	• Update the common Python class to 0.2.0 for performance improvements.<br><br>*fixed issues*<br>	• |
|25.2.10.83v319|*new features*<br>	• Filter for limiting AP import from XIQ.<br><br>*maintenance*<br>	• update common Python classes<br><br>*fixed issues*<br>	• |
