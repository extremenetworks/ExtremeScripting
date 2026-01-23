# Script created 2020 by Christoph Faber <christoph.faber@tuwien.ac.at> and Ondrej Hosek <ondrej.hosek@tuwien.ac.at>
# This Script is provided "as is" without any warranty and free of charge. We're not providing support for this script.
# As the official documentation for XOS 30+ is incorrect we only providing this script for saving others the time in finding
# a solution on how to use VRs and requests in XOS 30+.
# For this example we're using an http-Post, but can be changed as needed

import exsh
import json
import requests
import socket

SO_BINDTODEVICE = 25

# For creating an request-Session in the correct environement we need a custom class
# We're calling it HTTPAdapterWithSocketOptions here
# Can be customized if needed
class HTTPAdapterWithSocketOptions(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapterWithSocketOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapterWithSocketOptions, self).init_poolmanager(*args, **kwargs)

def def_vr(vr):
    # /proc/self/ns_id throws an IO-Error in XOS 30+ but is needed to define the VR in other XOS-Versions
    # The easiest Way is a try / except on the IO-Error. Otherwise it would be necessary to check the XOS-Version
    try:
        # "Old" Way for XOS below 30, we only need to switch VR and create a standard request-session
        f = open('/proc/self/ns_id', 'w')
        f.write(vr+'\n')
        f.close()
        return requests.session()
    except IOError:
        # New way for XOS 30 and greater
        # XOS 30+ requires an option "SO_BINDTODEVICE"
        # As it is a lot easier to use the standard request-class instead of a pure socket communication
        # we're creating an adapter for the request, so we can simplify this process like in XOS-versions below 30
        vrf_id = str(256+vr)
        adapter = HTTPAdapterWithSocketOptions(socket_options=[(socket.SOL_SOCKET, SO_BINDTODEVICE, "vrf_"+vrf_id)])
        req_session = requests.session()
        # Register http and https for the adapter
        # Can be extended if needed
        req_session.mount("http://", adapter)
        req_session.mount("https://", adapter)
        return req_session

# create the request environement
req_session = def_vr(2)

# send the data
dom_data = json.loads(exsh.clicmd('debug cfgmgr show next vlan.show_ports_transceiver portList=* port=None', True))
endpoint = "https://192.168.0.1/script"
r = req_session.post(endpoint, json=dom_data)
print(r.text)
