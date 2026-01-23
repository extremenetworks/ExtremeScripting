# POST DOM data

## Description
This Python script collects DOM (Digital Optical Monitoring) data and sends
it (as an example) to a server using HTTP POST at the address
`http://192.168.0.1/script`.

It illustrates how to perform HTTP communication using the Python `requests`
module (which ships with XOS) via different VRs (virtual routers) on XOS.

### Files
* [post_dom_data.py](post_dom_data.py)
* [README.md](README.md)

### Requirements
* Firmware: ExtremeXOS(TM) 21+
* Platform(s): Any ExtremeXOS switch

Tested on X450G2 with ExtremeXOS 22.7 and X460G2 with ExtremeXOS 30.3.

Example
```
# run script post_dom_data.py
DOM data stored
```
