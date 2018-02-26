# Python Scripts provided by Extreme Networks.

# This script is provided free of charge by Extreme.  We hope such scripts are
# helpful when used in conjunction with Extreme products and technology;
# however, scripts are provided simply as an accommodation and are not
# supported nor maintained by Extreme.  ANY SCRIPTS PROVIDED BY EXTREME ARE
# HEREBY PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL EXTREME OR ITS
# THIRD PARTY LICENSORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE USE OR DISTRIBUTION OF SUCH SCRIPTS.

# This script produces a port summary output for selected ports

import argparse
import json
from collections import OrderedDict
from os.path import (
    basename,
    splitext,
    )
import exsh

_version_ = '1.0.0.2'


class ExosDb(object):
    def __init__(self):
        self.port_stats = OrderedDict()
        self.port_rxerr = {}
        self.port_txerr = {}
        self.port_congestion = {}
        self.port_qos = {}
        self.proc_name = splitext(basename(__file__))[0]

    def get_exos_json_data(self, cmd):
        # run the command that returns JSON results
        result = exsh.clicmd(cmd, True)

        # convert the results to JSON
        try:
            json_result = json.loads(result)
        except Exception as e:
            print e
            return []

        # return the list of dictionaries
        return json_result.get('data', [])

    def get_port_statistics(self, portlist):
        # did the first command succeed?
        if self.show_ports_stats(portlist) is False:
            return False
        self.show_ports_txerrors()
        self.show_ports_rxerrors()
        self.show_ports_congestion()
        self.show_ports_qos_monitor()
        return True

    def show_ports_stats(self, portlist):
        cmd = 'debug cfgmgr show next vlan.show_ports_stats port=None portList={plist}'.format(
                plist=portlist)
        port_list = self.get_exos_json_data(cmd)
        for row in port_list:
            msg = row.get('message')
            if msg:
                print msg
                return False
            port = row.get('port')
            if port:
                self.port_stats[port] = row
        return True

    def show_ports_rxerrors(self):
        # for each port, collect the rxerror coungers
        for portlist in self.port_stats.keys():
            cmd = 'debug cfgmgr show next vlan.show_ports_rxerrors port=None portList={plist}'.format(
                    plist=portlist)
            port_list = self.get_exos_json_data(cmd)
            for row in port_list:
                port = row.get('port')
                if port:
                    self.port_rxerr[port] = row

    def show_ports_txerrors(self):
        # for each port, collect the txerror coungers
        for portlist in self.port_stats.keys():
            cmd = 'debug cfgmgr show one vlan.show_ports_txerrors port=None portList={plist}'.format(
                    plist=portlist)
            port_list = self.get_exos_json_data(cmd)
            for row in port_list:
                port = row.get('port')
                if port:
                    self.port_txerr[port] = row

    def show_ports_congestion(self):
        # for each port, collect the txerror coungers
        for portlist in self.port_stats.keys():
            cmd = 'debug cfgmgr show one vlan.show_ports_congestion port=None portList={plist}'.format(
                    plist=portlist)
            port_list = self.get_exos_json_data(cmd)
            for row in port_list:
                port = row.get('port')
                if port:
                    self.port_congestion[port] = row

    def show_ports_qos_monitor(self):
        # for each port, collect the txerror coungers
        for portlist in self.port_stats.keys():
            cmd = 'debug cfgmgr show next vlan.show_ports_qos_monitor port=None countType=1 ingress=1 portList={plist}'.format(
                    plist=portlist)
            port_list = self.get_exos_json_data(cmd)
            for row in port_list:
                port = row.get('port')
                if port:
                    self.port_qos[port] = row


class PortSummary(ExosDb):
    def __init__(self):
        super(PortSummary, self).__init__()

    def __call__(self):
        self.get_params()
        if self.args.version is True:
            print self.proc_name, "Version:", _version_
            return
        if self.get_port_statistics(self.args.ports) is False:
            return
        self.build_report()

    def get_params(self):
        parser = argparse.ArgumentParser(prog=self.proc_name)
        parser.add_argument(
                'ports',
                help='Ports to display. Default is all ports',
                nargs='?',
                default='*')
        parser.add_argument(
                '-v', '--version',
                help='Display version',
                action='store_true',
                default=False)

        self.args = parser.parse_args()
        return self.args

    def build_report(self):
        hdg = [
                [
                    '',
                    'In',
                    'Out',
                    'In',
                    'Out',
                    'In',
                    'Out',
                    'In',
                    'Out',
                    'In',
                    'Out',
                    'In',
                    'Out',
                    'In'
                ],
                [
                    'Port',
                    'Octets',
                    'Octets',
                    'Ucasts',
                    'Ucasts',
                    'Mcasts',
                    'Mcasts',
                    'Bcasts',
                    'Bcasts',
                    'Discards',
                    'Discards',
                    'Errors',
                    'Errors',
                    'Unknowns'
                ]
            ]

        try:
            exsh.clicmd('show time')
            print exsh.clicmd('show time', True),
        except RuntimeError:
            pass

        rows = []
        for port, port_stat in self.port_stats.items():
            port_rxerr = self.port_rxerr.get(port)
            port_txerr = self.port_txerr.get(port)
            port_congestion = self.port_congestion.get(port)
            port_qos = self.port_qos.get(port)

            cols = []
            # Port
            cols.append(port)

            # In Octets
            cols.append(port_stat.get('rxByteCnt'))

            # Out Octets
            cols.append(port_stat.get('txByteCnt'))

            # In Ucasts
            cols.append(port_stat.get('rxPktCnt'))

            # Out Ucasts
            cols.append(port_stat.get('txPktCnt'))

            # In Mcasts
            cols.append(port_stat.get('rxMcast'))

            # Out Mcasts
            cols.append(port_stat.get('txMcast'))

            # In Bcasts
            cols.append(port_stat.get('rxBcast'))

            # Out Bcasts
            cols.append(port_stat.get('txBcast'))

            # In Discards
            cnt = 0
            for fld in [
                      "q0congPkts",
                      "q1congPkts",
                      "q2congPkts",
                      "q3congPkts",
                      "q4congPkts",
                      "q5congPkts",
                      "q6congPkts",
                      "q7congPkts"]:
                cnt += int(port_qos.get(fld), 0)
            cols.append(cnt)

            # OutDiscards
            cols.append(port_congestion.get('dropPkts'))

            # In Errors
            cnt = 0
            for fld in [
                      "rxAlign",
                      "rxCrc",
                      "rxFrag",
                      "rxJabber",
                      "rxLost",
                      "rxOver",
                      "rxUnder"]:
                cnt += int(port_rxerr.get(fld), 0)
            cols.append(cnt)

            # Out Errors
            cnt = 0
            for fld in [
                    "txCollisions",
                    "txDeferred",
                    "txErrors",
                    "txLateCollisions",
                    "txLost",
                    "txParity"]:
                cnt += int(port_txerr.get(fld), 0)
            cols.append(cnt)

            # In Unknowns
            # TODO
            cols.append(0)

            rows.append(cols)

        # determine the max width of data fields
        max_width = 0
        for row in hdg:
            for entry in row:
                if len(str(entry)) > max_width:
                    max_width = len(str(entry))
        for row_entry in rows:
            for entry in row_entry:
                if len(str(entry)) > max_width:
                    max_width = len(str(entry))
        # leave room for a space
        max_width += 1

        # print headings
        row = hdg[0]
        print_line = ''
        for idx in range(len(row)):
            if idx:
                print_line += '{:^{}}'.format(row[idx], max_width)
            else:
                print_line += '{:<{}}'.format(row[idx], max_width)
        print print_line

        row = hdg[1]
        print_line = ''
        for idx in range(len(row)):
            if idx:
                print_line += '{:>{}}'.format(row[idx], max_width)
            else:
                print_line += '{:<{}}'.format(row[idx], max_width)
        print print_line

        # print heading separator
        print_line = ''
        for idx in range(len(hdg[0])):
            if idx:
                print_line += ' {}'.format('-' * (max_width - 1))
            else:
                print_line += '{} '.format('-' * (max_width - 1))
        print print_line

        # print ports stats
        for row in rows:
            cnt = 0
            print_line = ''
            for idx in range(len(row)):
                if idx:
                    print_line += '{:>{}}'.format(row[idx], max_width)
                else:
                    print_line += '{:<{}}'.format(row[idx], max_width)
            print print_line


try:
    a = PortSummary()
    a()
except (KeyboardInterrupt, SystemExit, TypeError):
    pass
