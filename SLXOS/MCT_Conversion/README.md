# MCT configuration converter
Tool to aid in converting  Multi Chassis Trunk (MCT) CLIs in SLXOS 18r.2.00b to the new format as required by SLXOS 20.1.1.

# Description
MCT CLIs (Command Line Interface) are simplified in SLXOS 20.1.1.
When 'firmware download' command to upgrade to SLXOS 20.1.1 is executed on a system running SLXOS 18r.2.00b,
warning message will be shown indicating that MCT configuration in the system will be lost during upgrade. The warning would also indicate
that if user wants to preserve existing MCT configuration, the tool 'mct_config_convert.py' has to be run in 'exec' mode before upgrading to SLXOS 20.1.1.

The tool 'mct_config_convert.py' converts the MCT configuration present in SLXOS 18r.2.00b device's startup-config to the new format as needed by SLXOS 20.1.1. The tool needs to be copied to the 'flash' path on the device running SLXOS 18r.2.00b.
For example, below 'copy ' command can be run in 'exec' mode as shown below:

*sw# scp://\<username\>:\<password\>@hostname/\<file path of mct_config_convert.py\>  flash://*

# Files

* [The Core Python Script - mct_config_convert.py](mct_config_convert.py)
* [README.md](README.md)


# Requirements
Firmware: SLXOS 18r.2.00b

Platform(s): SLX 9540, SLX 9640

# Usage
<pre>
> mct_config_convert.py [-h] --peer_ip PEER_IP --peer_int PEER_INT [--source_ip SOURCE_IP]  

Arguments: 

  -h                      show this help message and exit 

  --peer_ip PEER_IP        MCT peer IP address 

  --peer_int PEER_INT      MCT peer interface

  --source_ip SOURCE_IP    Source IP to be configured in the peer-interface in CIDR format. This argument is optional.
  </pre>

# Example

<pre>
sw# python mct_config_convert.py --peer_ip "10.20.20.18" --peer_int "Port-Channel 64" 
</pre>

# License
Copyright© 2020, Extreme Networks. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1.Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.


2.Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Support
The software is provided as is and Extreme Networks has no obligation to provide maintenance, support, updates, enhancements or modifications. Any support provided by Extreme Networks is at its sole discretion.

Issues and/or bug fixes may be reported on The Hub.


  
