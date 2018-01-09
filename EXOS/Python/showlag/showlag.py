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
'''
After downloading to an EXOS switch, the help command shows the different options available

# run script showlag.py -h
usage: showlag [-h] [-d] [cmd [cmd ...]]

positional arguments:
  cmd          statistics, rxerrors, txerrors, utilization, all
               Use the same format as the "show port" EXOS commands

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Show debug information

The 'all' command displays the output for:
    statistics
    rxerrors
    txerrors
    utilization

# run script showlag.py statistics
    LAG  Tx Pkt Tx Byte  Rx Pkt Rx Byte  Rx Pkt  Rx Pkt  Tx Pkt  Tx Pkt
          Count   Count   Count   Count   Bcast   Mcast   Bcast   Mcast
------- ------- ------- ------- ------- ------- ------- ------- -------
   lag1       0       0       0       0       0       0       0       0
  lag10       0       0       0       0       0       0       0       0
  lag20       0       0       0       0       0       0       0       0
------- ------- ------- ------- ------- ------- ------- ------- -------
(Private) X460G2-24t-10G4.48 # run script showlag.py rxerrors
   LAG     Rx     Rx     Rx     Rx     Rx     Rx     Rx
          Crc   Over  Under   Frag Jabber  Align   Lost
------ ------ ------ ------ ------ ------ ------ ------
  lag1      0      0      0      0      0      0      0
 lag10      0      0      0      0      0      0      0
 lag20      0      0      0      0      0      0      0
------ ------ ------ ------ ------ ------ ------ ------
(Private) X460G2-24t-10G4.49 # run script showlag.py -h
usage: showlag [-h] [-d] [cmd [cmd ...]]

positional arguments:
  cmd          statistics, rxerrors, txerrors, utilization, all
               Use the same format as the "show port" EXOS commands

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Show debug information
(Private) X460G2-24t-10G4.50 # run script showlag.py all
      LAG        Tx        Tx        Tx        Tx        Tx        Tx
               Coll Late coll  Deferred    Errors      Lost    Parity
--------- --------- --------- --------- --------- --------- ---------
     lag1         0         0         0         0         0         0
    lag10         0         0         0         0         0         0
    lag20         0         0         0         0         0         0
--------- --------- --------- --------- --------- --------- ---------


        LAG        Link          Rx     Peak Rx          Tx     Peak Tx
                  Speed % bandwidth % bandwidth % bandwidth % bandwidth
----------- ----------- ----------- ----------- ----------- -----------
       lag1        None     0.00000     0.00000     0.00000     0.00000
      lag10        None     0.00000     0.00000     0.00000     0.00000
      lag20        None     0.00000     0.00000     0.00000     0.00000
----------- ----------- ----------- ----------- ----------- -----------


    LAG  Tx Pkt Tx Byte  Rx Pkt Rx Byte  Rx Pkt  Rx Pkt  Tx Pkt  Tx Pkt
          Count   Count   Count   Count   Bcast   Mcast   Bcast   Mcast
------- ------- ------- ------- ------- ------- ------- ------- -------
   lag1       0       0       0       0       0       0       0       0
  lag10       0       0       0       0       0       0       0       0
  lag20       0       0       0       0       0       0       0       0
------- ------- ------- ------- ------- ------- ------- ------- -------


   LAG     Rx     Rx     Rx     Rx     Rx     Rx     Rx
          Crc   Over  Under   Frag Jabber  Align   Lost
------ ------ ------ ------ ------ ------ ------ ------
  lag1      0      0      0      0      0      0      0
 lag10      0      0      0      0      0      0      0
 lag20      0      0      0      0      0      0      0
------ ------ ------ ------ ------ ------ ------ ------

'''

import sys
import exsh
import argparse
import json
import logging
from argparse import (
    ArgumentParser
    )
from os.path import (
    basename,
    splitext,
    )

__version__ = '1.0.0.1'

PROCESS_NAME = splitext(basename(__file__))[0]


class ShowLag(object):
    def __init__(self):
        self.args = None
        self.cmdb = {}
        self.lagdb = {}
        self.lagnamedb = {}
        self.handler = logging.StreamHandler(sys.stderr)
        self.handler.setLevel(logging.INFO)
        self.handler.setFormatter(logging.Formatter(
            '%(levelname)s:%(threadName)s:%(name)s:%(funcName)s:%(lineno)s:: '
            '%(message)s'))
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)
        if not len(self.log.handlers):
            self.log.addHandler(self.handler)
        self.REPORT_STATS = 'statistics'
        self.REPORT_RXERR = 'rxerrors'
        self.REPORT_TXERR = 'txerrors'
        self.REPORT_UTIL = 'utilization'
        self.REPORT_ALL = 'all'
        self.REPORT_TYPES = [
                self.REPORT_STATS,
                self.REPORT_RXERR,
                self.REPORT_TXERR,
                self.REPORT_UTIL,
                self.REPORT_ALL
                ]
        self.report_func_dict = {
                self.REPORT_STATS: self.lag_statistics,
                self.REPORT_RXERR: self.lag_rxerrors,
                self.REPORT_TXERR: self.lag_txerrors,
                self.REPORT_UTIL: self.lag_utilization,
                self.REPORT_ALL: self.lag_all,
                }
        self.report_type = None
        self.report_lagnames = []

    def __call__(self, args, **kwargs):
        self.args = args
        if args.debug is True:
            self.handler.setLevel(logging.DEBUG)
            self.log.setLevel(logging.DEBUG)
        self.log.debug(args)
        self.build_db()
        self.get_params()
        if self.report_type is None:
            print 'No report type specified'
            print 'Report types are: {}'.format(', '.join(self.REPORT_TYPES))
            return
        func = self.report_func_dict.get(self.report_type[0])
        if func:
            func()
        else:
            print 'Program error. No support for {} report'.format(self.report_type)

    def get_params(self):
        for word in self.args.cmd:
            match_word = [s for s in self.REPORT_TYPES + self.lagnamedb.keys() if s.startswith(word)]
            if not match_word:
                print 'Unknown input {}'.format(word)
                return

        # look for report type
        for word in self.args.cmd:
            self.report_type = [s for s in self.REPORT_TYPES if s.startswith(word)]
            if self.report_type:
                self.args.cmd.remove(word)
                break

        # look for lag names
        for word in self.args.cmd:
            self.report_lagnames += [s for s in self.lagnamedb.keys() if s.startswith(word)]
            self.log.debug('word={}, report_type={}, report_lagnames={}'.format(
                word, self.report_type, self.report_lagnames))

        # report all lags
        if not self.report_lagnames:
            self.report_lagnames = sorted(self.lagnamedb.keys())
        self.log.debug('lag list {}'.format(self.report_lagnames))
        self.log.debug('report type {}'.format(self.report_type))

    def json_clicmd(self, cmd):
        # issue debug cfgmgr CLI command to EXOS and return the JSON data
        self.log.debug(cmd)
        json_result = exsh.clicmd(cmd, capture=True)

        try:
            json_dict = json.loads(json_result)
        except Exception:
            self.log.debug('JSON format error')
            return None, None
        # extract and return the data list
        return (json_dict.get("class"), json_dict.get("data"))

    def build_db(self):
        # build up CM data for LAGs and ports
        for cmd in [
                'debug cfgmgr show next vlan.ls_ports_show',
                'debug cfgmgr show next vlan.show_ports_info portList=* port=None',
                'debug cfgmgr show next vlan.show_ports_config portList=* port=None',
                'debug cfgmgr show next vlan.show_ports_utilization portList=* port=None',
                'debug cfgmgr show next vlan.show_ports_stats portList=* port=None',
                'debug cfgmgr show next vlan.show_ports_rxerrors portList=* port=None',
                'debug cfgmgr show next vlan.show_ports_txerrors portList=* port=None',
                ]:
            cm_class, cm_list = self.json_clicmd(cmd)
            db_list = self.cmdb.setdefault(cm_class, [])
            db_list += cm_list
        self.log.debug(json.dumps(self.cmdb, indent=2))

        # build lag membership dict
        for cm_row in self.cmdb.get('ls_ports_show'):
            if cm_row.get("status") not in ["MORE", "SUCCESS"]:
                continue
            loadShareMaster = cm_row.get("loadShareMaster")
            lag_list = self.lagdb.setdefault(loadShareMaster, [])
            lag_list.append(cm_row.get("port"))
        self.log.debug(json.dumps(self.lagdb, indent=2))

        # build lag name to port dict
        # lag name is the master port display string
        # when no display string is present, 'lagnn' where nn is the port number
        for cm_row in self.cmdb.get('show_ports_info'):
            if cm_row.get("status") not in ["MORE", "SUCCESS"]:
                continue
            port = cm_row.get('port')
            if port in self.lagdb:
                lag_name = cm_row.get("displayString")
                if lag_name is None:
                    lag_name = 'lag{}'.format(port)
                self.lagnamedb[lag_name] = port
        self.log.debug(json.dumps(self.lagnamedb, indent=2))

    def compute_total(self, data_type, port_field_name, port_list):
        sum_dict = {}
        cm_data_list = self.cmdb.get(data_type)
        if cm_data_list is None:
            print 'Program error. Unknown data structure {}. Contact Extreme'.format(data_type)
            return None
        for cm_row in cm_data_list:
            port = cm_row.get(port_field_name)
            if str(port) not in port_list:
                continue
            for k, v in cm_row.items():
                try:
                    num = int(v)
                    ttl = sum_dict.setdefault(k, 0)
                    ttl += num
                    sum_dict[k] = ttl
                    continue
                except Exception:
                    pass
                try:
                    num = float(v)
                    ttl = sum_dict.setdefault(k, 0.0)
                    ttl += num
                    sum_dict[k] = ttl
                    continue
                except Exception:
                    pass
        return sum_dict

    def summarize_lag_data(self, data_type, port_field_name):
        self.log.debug('Called ')
        sum_list = []
        for lagname in self.report_lagnames:
            master_port = self.lagnamedb.get(lagname)
            port_list = self.lagdb.get(master_port)
            sum_dict = self.compute_total(data_type, port_field_name,  port_list)
            sum_list.append({lagname: sum_dict})
        self.log.debug(json.dumps(sum_list, indent=2))
        return sum_list

    def create_report(self, lag_summary_list, report_spec, report_footer):
        # go through all of the data fields to determine the longest value

        # set a minimum width
        max_width = 6
        for hdg1, hdg2, data_field_name in report_spec:
            for hdg in [hdg1, hdg2]:
                if len(hdg) > max_width:
                    max_width = len(hdg)
        for lag_summary_row in lag_summary_list:
            for lagname, sum_dict in lag_summary_row.items():
                if len(lagname) > max_width:
                    max_width = len(lagname)
                for field_name, field_value in sum_dict.items():
                    if len(str(field_value)) > max_width:
                        max_width = len(str(field_value))
        # max_width is now set to the widest field value
        # print field headings
        line = ''
        for hdg1, hdg2, data_field_name in report_spec:
            line += '{x:>{width}} '.format(x=hdg1, width=max_width)
        print line
        line = ''
        for hdg1, hdg2, data_field_name in report_spec:
            line += '{x:>{width}} '.format(x=hdg2, width=max_width)
        print line
        line = ''
        for hdg1, hdg2, data_field_name in report_spec:
            line += '{x:>{width}} '.format(x='-' * max_width, width=max_width)
        print line
        for lag_summary_row in lag_summary_list:
            line = ''
            for k, v in lag_summary_row.items():
                for hdg1, hdg2, data_field_name in report_spec:
                    if data_field_name == '<key>':
                        line += '{x:>{width}} '.format(x=k, width=max_width)
                    else:
                        line += '{x:>{width}} '.format(x=v.get(data_field_name), width=max_width)
            print line
        line = ''
        for hdg1, hdg2, data_field_name in report_spec:
            line += '{x:>{width}} '.format(x='-' * max_width, width=max_width)
        print line
        line = ''
        for line in report_footer:
            print line

    def lag_all(self):
        for report_type, func in self.report_func_dict.items():
            if report_type == self.REPORT_ALL:
                continue
            func()
            print '\n'

    def lag_statistics(self):
        self.log.debug('Called')
        lag_summary_list = self.summarize_lag_data('show_ports_stats', 'port')
        # report spec is (hdg1, hdg2, data field name)
        report_spec = [
                ('LAG', '', '<key>'),  # use the data structure key
                ('Tx Pkt', 'Count', 'txPktCnt'),
                ('Tx Byte', 'Count', 'txByteCnt'),
                ('Rx Pkt', 'Count', 'rxPktCnt'),
                ('Rx Byte', 'Count', 'rxByteCnt'),
                ('Rx Pkt', 'Bcast', 'rxBcast'),
                ('Rx Pkt', 'Mcast', 'rxMcast'),
                ('Tx Pkt', 'Bcast', 'txBcast'),
                ('Tx Pkt', 'Mcast', 'txMcast'),
            ]
        report_footer = []
        self.create_report(lag_summary_list, report_spec, report_footer)
        return

    def lag_rxerrors(self):
        self.log.debug('Called')
        lag_summary_list = self.summarize_lag_data('show_ports_rxerrors', 'port')
        # report spec is (hdg1, hdg2, data field name)
        report_spec = [
                ('LAG', '', '<key>'),  # use the data structure key
                ('Rx', 'Crc', 'rxCrc'),
                ('Rx', 'Over', 'rxOver'),
                ('Rx', 'Under', 'rxUnder'),
                ('Rx', 'Frag', 'rxFrag'),
                ('Rx', 'Jabber', 'rxJabber'),
                ('Rx', 'Align', 'rxAlign'),
                ('Rx', 'Lost', 'rxLost'),
            ]
        report_footer = []
        self.create_report(lag_summary_list, report_spec, report_footer)
        return

    def lag_txerrors(self):
        self.log.debug('Called')
        lag_summary_list = self.summarize_lag_data('show_ports_txerrors', 'port')
        # report spec is (hdg1, hdg2, data field name)
        report_spec = [
                ('LAG', '', '<key>'),  # use the data structure key
                ('Tx', 'Coll', 'txCollisions'),
                ('Tx', 'Late coll', 'txLateCollisions'),
                ('Tx', 'Deferred', 'txDeferred'),
                ('Tx', 'Errors', 'txErrors'),
                ('Tx', 'Lost', 'txLost'),
                ('Tx', 'Parity', 'txParity'),
            ]
        report_footer = []
        self.create_report(lag_summary_list, report_spec, report_footer)
        return

    def percent(self, bytes_per_sec, link_speed):
        try:
            return '{:>.5f}'.format(((float(bytes_per_sec)/float(link_speed))*100)/125000)
        except Exception:
            return '{:>.5f}'.format(0.0)

    def lag_utilization(self):
        self.log.debug('Called')
        port_config_summary_list = self.summarize_lag_data('show_ports_config', 'port')
        lag_summary_list = self.summarize_lag_data('show_ports_utilization', 'port')
        for lag_summary_row in lag_summary_list:
            for lagname, lag_dict in lag_summary_row.items():
                # find the matching lag in port_config_summary_list
                for port_row in port_config_summary_list:
                    for port_lagname, port_dict in port_row.items():
                        if lagname == port_lagname:
                            lag_dict['linkSpeed'] = port_dict.get('speedActual')
                            break

                lag_dict['rxBwPercent'] = self.percent(
                        lag_dict.get('rxBytesPerSec'),
                        lag_dict.get('linkSpeed'),
                        )
                lag_dict['rxBwPeakPercent'] = self.percent(
                        lag_dict.get('rxPeakBytesPerSec'),
                        lag_dict.get('linkSpeed'),
                        )
                lag_dict['txBwPercent'] = self.percent(
                        lag_dict.get('rxBytesPerSec'),
                        lag_dict.get('linkSpeed'),
                        )
                lag_dict['txBwPeakPercent'] = self.percent(
                        lag_dict.get('txPeakBytesPerSec'),
                        lag_dict.get('linkSpeed'),
                        )

        report_spec = [
                ('LAG', '', '<key>'),  # use the data structure key
                ('Link', 'Speed', 'linkSpeed'),
                ('Rx', '% bandwidth', 'rxBwPercent'),
                ('Peak Rx', '% bandwidth', 'rxBwPeakPercent'),
                ('Tx', '% bandwidth', 'txBwPercent'),
                ('Peak Tx', '% bandwidth', 'txBwPeakPercent'),
            ]
        report_footer = []
        self.create_report(lag_summary_list, report_spec, report_footer)
        return


def get_params():
    # These are the command line options for clone
    # Both master and client options are evalated here
    parser = ArgumentParser(
            prog=PROCESS_NAME,
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-d', '--debug',
                        help='Show debug information',
                        action='store_true',
                        default=False)

    parser.add_argument('cmd',
                        help='statistics, rxerrors, txerrors, utilization, all\n'
                        'Use the same format as the "show port" EXOS commands',
                        nargs='*',
                        default=None)

    return parser.parse_args()


if __name__ == '__main__':
    args = get_params()
    showlag = ShowLag()
    try:
        showlag(args)
    except SystemExit, KeyboardInterrupt:
        pass
