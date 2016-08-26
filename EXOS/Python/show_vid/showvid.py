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

import exsh
import sys
import collections
import json

def expand_number_string(number_string, min_limit, max_limit):
    '''create a set() of unique numbers from comma and hyphen separated values
    e.g, 1,3,5,7-10 = [1,3,5,7,8,9,10]
    Verify that each expanded value is in the range: min_limit <= value <= max_limit
    '''
    expanded_list = list()
    tokens = number_string.split(',')
    for token in tokens:
        # simple number
        if token.isdigit():
            expanded_list.append(int(token))
            continue
        # validate n-m format
        minVal, sep, maxVal = token.partition('-')
        if len(sep) == 0:
            raise ValueError('range has a bad value: ' + token + '\n')
        if not minVal.isdigit():
            raise ValueError(' '.join(['range error:', token + ':', minVal, 'is not a number\n']))
        if not maxVal.isdigit():
            raise ValueError(' '.join(['range error:', token + ':', maxVal, 'is not a number\n']))
        if int(minVal) >= int(maxVal):
            raise ValueError(' '.join(['range error:', token + ':', minVal, 'is not less than', maxVal, '\n']))
        try:
            # expand m-n range into individual values
            expanded_list += range(int(minVal), int(maxVal) + 1)
        except:
            raise ValueError('range has a bad format: ' + token + '\n')

    # test the individual values to verify they are in the range provided
    if min_limit is not None or max_limit is not None:
        for num in expanded_list:
            if min_limit is not None and num < min_limit:
                raise OverflowError(' '.join(['range error:', 'value =',str(num), 'is less than', str(min_limit), '\n']))
            if max_limit is not None and num > max_limit:
                raise OverflowError(' '.join(['range error:', 'value =',str(num), 'is greater than', str(max_limit), '\n']))
    return set(expanded_list)

class ExosDb(object):
    def __init__(self):
        self.vlan_map = None
        self.vnames = []

    def get_exos_json_data(self, cmd):
        # run the command that returns JSON results
        result = exsh.clicmd(cmd, True)

        # convert the results to JSON
        try:
            json_result = json.loads(result)
        except:
            return []

        # return the list of dictionaries
        return json_result.get('data', [])

    def get_vlan_map(self):
        self.vlan_map = collections.OrderedDict()
        vnames = []

        # extract the entire vlan map
        cmd = 'debug cfgmgr show next vlan.vlanMap vlanList=1-4094'
        json_data = self.get_exos_json_data(cmd)
        if len(json_data) == 0:
            # the length tells us that the vlanMap is not available
            # use the older slower way of building a vlan maps
            cmd = 'debug cfgmgr show next vlan.vlan'
            json_data = self.get_exos_json_data(cmd)
            vmap = {}
            for vlan in json_data:
                vid = int(vlan.get('tag'))
                vname = vlan.get('name')
                vtype = int(vlan.get('type'))
                vmap[vid] = (vname, vtype)
                vnames.append(vname)
            for vid in sorted(vmap.keys()):
                self.vlan_map[vid] = vmap[vid]
        else:
            # walk the list and extract the fields to form the map
            for vmap in json_data:
                status = vmap.get('status')
                if status == 'ERROR':
                    break
                try:
                    vid = int(vmap.get('vlanId'))
                except:
                    pass
                if vid is None:
                    continue
                vname = vmap.get('vlanName')
                vtype = int(vmap.get('vlanType'))
                self.vlan_map[vid] = (vname, vtype)
                vnames.append(vname)
        vnames.append('Mgmt')
        self.vlan_map[4095] = ('Mgmt', 2)

        # need a sorted vnames for flag lookups
        self.vnames = sorted(vnames)
        return self.vlan_map

    def get_vlan_proc_name(self, vname):
        if self.vlan_map is None:
            self.get_vlan_map()

        cmd = 'debug cfgmgr show one vlan.vlanProc action=SHOW_VLAN_NAME name1={vname}'.format(vname=vname)
        json_data = self.get_exos_json_data(cmd)
        if len(json_data):
            return json_data[0]
        return None

    def get_vlan_proc_flags(self, vname):
        if self.vlan_map is None:
            self.get_vlan_map()

        cmd = 'debug cfgmgr show one vlan.vlanProc action=SHOW_VLAN name1={vname}'.format(vname=vname)
        json_data = self.get_exos_json_data(cmd)
        if len(json_data):
            return json_data[0]
        return None


class ShowVid(object):
    class Constants(object):
        PROCESS_NAME = 'showvid'

        # CLI constants
        VLAN_LIST = '<vlan_list>'
        VLAN_DETAIL = 'detail'

        # CM object constants
        ACTION = 'SHOW_VLAN_NAME'
        FLAGS_ACTION = 'SHOW_VLAN'
        VLAN_TYPE = 3
        VMAN_TYPE = 5

        # vlan constants
        MGMT = 'Mgmt'

        class PrintLine(object):
            FMT = '{vid:>{vid_len}}{sep:1.1}{name:<{name_len}}{sep:1.1}{addr:<{addr_len}}{sep:1.1}{sep:1.1}{flags:<{flags_len}}{sep:1.1}{sep:1.1}{proto:<{proto_len}}{sep:1.1}{ports:{proto_len}}{sep:1.1}{vr:<{vr_len}}'
            VID_LEN = 4
            NAME_LEN = 15
            ADDR_LEN = 18
            FLAGS_LEN = 28
            PROTO_LEN = 6
            PORTS_LEN = 6
            VR_LEN = 10
        PL = PrintLine()


    def __init__(self):
        # init the class
        self.C = ShowVid.Constants()
        self.db = ExosDb()
        self.vid_list = None

        # display formatting
        self.fmt = self.C.PL.FMT
        self.footing = [
                "Flags : (B) BFD Enabled, (c) 802.1ad customer VLAN, (C) EAPS Control VLAN,\n"
                "        (d) Dynamically created VLAN, (D) VLAN Admin Disabled,\n"
                "        (e) CES Configured, (E) ESRP Enabled, (f) IP Forwarding Enabled,\n"
                "        (F) Learning Disabled, (h) TRILL Enabled, (i) ISIS Enabled,\n"
                "        (I) Inter-Switch Connection VLAN for MLAG, (k) PTP Configured,\n"
                "        (l) MPLS Enabled, (L) Loopback Enabled, (m) IPmc Forwarding Enabled,\n"
                "        (M) Translation Member VLAN or Subscriber VLAN, (n) IP Multinetting Enabled,\n"
                "        (N) Network Login VLAN, (o) OSPF Enabled, (O) Flooding Disabled,\n"
                "        (p) PIM Enabled, (P) EAPS protected VLAN, (r) RIP Enabled,\n"
                "        (R) Sub-VLAN IP Range Configured, (s) Sub-VLAN, (S) Super-VLAN,\n"
                "        (t) Translation VLAN or Network VLAN, (T) Member of STP Domain,\n"
                "        (v) VRRP Enabled, (V) VPLS Enabled, (W) VPWS Enabled, (Z) OpenFlow Enabled\n"
            ]

    def __call__(self):
        # get command line args
        try:
            args = self.get_params()
        except:
            return
        if args.vlan is not None:
            try:
                self.vid_list = expand_number_string(args.vlan, 1, 4095)
            except OverflowError:
                print 'Error: (-v) VID {0} is outside the range of {1}'.format(args.vlan, '1-4095')
                return
            except Exception as msg:
                print 'Error: (-v) VIDs can only be defined using single numbers with commas or <start>-<end> range ("1", "1,2,3", "1-5", "1,2,3-5,6-8", etc)'
                print msg
                return

        print 'Collecting information. This may take a moment'

        # load vlan id to vlan name map
        self.db.get_vlan_map()

        if len(self.db.vlan_map) == 0:
            exoslib.show('Error: There are no VIDs to display\n',True)
            return

        # display the heading
        self.print_heading_fmt1()

        # display the VLAN lines ordered by VID
        for vid, (vname, vtype) in self.db.vlan_map.items():
            if self.vid_list is not None and int(vid) not in self.vid_list:
                continue
            # skip VMANs
            if vtype == 5:
                continue
            # print the detail line for the VLAN
            try:
                self.print_summary_line(self.db.get_vlan_proc_name(vname))
            except:
                break

        # either the user escaped out or the list ended. Display the footer
        self.print_dash_line()
        self.show_list(self.footing)

    def get_params(self):
        import argparse
        parser = argparse.ArgumentParser(prog=self.C.PROCESS_NAME)
        parser.add_argument('-v', '--vlan',
                help='VLAN ID range 1,2 or 1-5',
                default=None)
        args = parser.parse_args()
        return args


    def get_flags(self, v):
        # The form of vlanProc object that returns the flags is SHOW_VLAN action
        # The behavior of this action is to return the next VLAN
        # so to spoof vlanProc, we trim the trailing character off of the
        # name so it gets the next one higher
        vname = v.get('name1')
        vname_prev = vname[0:-1] + chr(ord(vname[-1]) - 1)


        while True:
            reply = self.db.get_vlan_proc_flags(vname_prev)
            if reply.get('status') in ['ERROR'] or reply.get('name1') is None:
                # ran off the end of all VLANs
                return ''

            if reply.get('name1').lower > vname.lower():
                # returned name is past the one we are looking for
                return ''

            if reply.get('name1') == vname:
                # matched the name we are looking for
                return '' if reply.get('flags') is None else reply.get('flags')

            # find the next VLAN name
            vname_prev = reply.get('name1')


    def print_summary_line(self, v):
        # send a single vlan summary line to the display
        if v['tag'] is None:
            return
        if v['ipStatus'] == '1':
            addr_string = '{0}/{1}'.format(v['ipAddress'],v['maskForDisplay'])
        else:
            addr_string = '-' * self.C.PL.ADDR_LEN

        vdesc_string = v.get('description')
        if vdesc_string is None or len(vdesc_string) == 0:
            vdesc_string = v['name1']

        if len(vdesc_string) > self.C.PL.NAME_LEN:
            # split line into 2 parts
            self.output_fmt1(vid=v['tag'], name=vdesc_string)
            self.output_fmt1(addr=addr_string,
                flags=self.get_flags(v),
                proto=v['filter'],
                ports='{0}/{1}'.format(str(v['activePorts']), str(v['count1'])),
                vr=v['name2'])
        else:
            self.output_fmt1(vid=v['tag'],
                name=vdesc_string,
                addr=addr_string,
                flags=self.get_flags(v),
                proto=v['filter'],
                ports='{0}/{1}'.format(str(v['activePorts']), str(v['count1'])),
                vr=v['name2'])
        return

    def show_list(self, display_list):
        # output a constant list to the display
        for dl in display_list:
            try:
                self.show(dl + '\n', True)
            except KeyboardInterrupt:
                break

    def print_heading_fmt1(self):
        self.print_dash_line()
        self.output_fmt1(
            vid='VID',
            #name='Name',
            name='Description',
            addr='Protocol Addr',
            flags='Flags',
            proto='Proto',
            ports='Ports',
            vr='Virtual')
        self.output_fmt1(
            name='/VLAN Name',
            ports='Active',
            vr='Router'),
        self.output_fmt1(
            ports='/Total')
        self.print_dash_line(sep='')

    def print_dash_line(self, sep='-'):
        self.output_fmt1(
            vid='-' * self.C.PL.VID_LEN,
            name='-' * self.C.PL.NAME_LEN,
            addr='-' * self.C.PL.ADDR_LEN,
            flags='-' * self.C.PL.FLAGS_LEN,
            proto='-' * self.C.PL.PROTO_LEN,
            ports='-' * self.C.PL.PORTS_LEN,
            vr='-' * self.C.PL.VR_LEN,
            sep=sep,
            force=True)

    def output_fmt1(self, vid='', name='', addr='', flags='', proto='', ports='', vr='', sep='', force=False):
        line = self.fmt.format(
            vid=vid,
            vid_len = self.C.PL.VID_LEN,
            name=name,
            name_len = self.C.PL.NAME_LEN,
            addr=addr,
            addr_len = self.C.PL.ADDR_LEN,
            flags=flags,
            flags_len = self.C.PL.FLAGS_LEN,
            proto=proto,
            proto_len = self.C.PL.PROTO_LEN,
            ports=ports,
            ports_len = self.C.PL.PORTS_LEN,
            vr=vr,
            vr_len = self.C.PL.VR_LEN,
            sep=sep)
        self.show(line.rstrip() + '\n', force=force)


    def show(self, display_string, force=False):
        # send single line to display. return exception if user enters 'Q'
        print display_string,
        '''
        if exoslib.show(display_string, 0 if force is False else 1) == -1:
            if force is False:
                raise KeyboardInterrupt
        '''


c = ShowVid()
c()
