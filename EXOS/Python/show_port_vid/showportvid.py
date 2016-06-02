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

from operator import itemgetter
class ExosDb(object):
    def __init__(self):
        self.port_list = None
        self.port_list_detail = None

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

    def show_ports_info(self, portlist):
        # extract the entire portlist
        cmd = 'debug cfgmgr show next vlan.show_ports_info port=None portList={plist}'.format(plist=portlist)
        self.port_list = self.get_exos_json_data(cmd)
        return self.port_list

    def show_ports_info_detail_vlans(self, port):
        # extract the entire portlist
        cmd = 'debug cfgmgr show next vlan.show_ports_info_detail_vlans port={port} vlanIfInstance=None'.format(port=port)
        self.port_list_detail = self.get_exos_json_data(cmd)
        return self.port_list_detail

    def vlan(self, vname):
        # a single vlan by name to get the description
        cmd = 'debug cfgmgr show one vlan.vlan name={vname}'.format(vname=vname)
        result = self.get_exos_json_data(cmd)
        if len(result):
            return result[0]
        return result


class ShowPortsVid(object):
    class Constants(object):
        PROCESS_NAME = 'showportvid'

        # CLI constants
        class Cli(object):
            PORT_LIST = '<port_list>'
            ALL_PORTS = 'all'
            ALL_PORTS_STAR = '*'
            VID = 'vid'
            VLAN = 'vlan'
            DESC = 'description'
            PORTS_ONLY = 'port-number'
        CLI = Cli()

        class Head(object):
            PORT = 'Port'
            TAGGED = 'Tagged'
            UNTAGGED = 'Untagged'

        class Heading(Head):
            VID = 'VID(s)'
            NAME = 'VLAN Name(s)'
        HDR = Heading()

        class PrintLine(object):
            FMT = '{port:<{port_len}} {vtype:<{vtype_len}}  {vids}\n'
            PORT_LEN = 8
            VTYPE_LEN = 8
            VID_LEN = 60
            NONE = 'None'
        PL = PrintLine()

        class Heading2(Head):
            VID = 'VID'
            NAME = 'VLAN Name'
            DESC = 'VLAN Description'
        HDR2 = Heading2()

        class PrintLine2(object):
            VID_FMT = '{port:<{port_len}} {vtype:<{vtype_len}} {vid:>{vid_len}} {vname:<{vname_len}} {vdesc:<{vdesc_len}}\n'
            NAME_FMT = '{port:<{port_len}} {vtype:<{vtype_len}} {vname:<{vname_len}} {vid:>{vid_len}} {vdesc:<{vdesc_len}}\n'
            PORT_LEN = 8
            VTYPE_LEN = 8
            VID_LEN = 4
            VNAME_LEN = 20
            VDESC_LEN = 36
            NONE = 'None'
        PL2 = PrintLine2()



    def __init__(self):
        # display formatting

        # init the class
        self.C = ShowPortsVid.Constants()
        self.db = ExosDb()
        self.fmt2 = None
        self.port_list = None
        self.show_vlan_names = False
        self.include_description = False
        self.port_numbers_only = False
        self.print_header = True


    def __call__(self):
        try:
            args = self.get_params()
        except:
            return

        # vid order or vlan name order?
        if args.names is True:
            self.show_vlan_names = True

        # vlan description format?
        if args.description is True:
            self.include_description = True

        # display port numbers only?
        if args.port_numbers is True:
            self.port_numbers_only = True

        try:
            self.collect_port()
        except:
            pass

    def get_params(self):
        import argparse
        parser = argparse.ArgumentParser(prog=self.C.PROCESS_NAME)
        parser.add_argument('-p', '--ports',
                help='Ports to display. Default is all ports',
                default='*')
        parser.add_argument('-P', '--port_numbers',
                help='Only show port numbers. Default: show port display string',
                action='store_true',
                default=False)
        parser.add_argument('-n', '--names',
                help='VLANs are displayed in name order. Default: VID order',
                action='store_true',
                default=False)
        parser.add_argument('-d', '--description',
                help='Show VLAN description',
                action='store_true',
                default=False)
        self.args = parser.parse_args()
        return self.args


    def collect_port(self):
        # now collect the port data from EXOS
        # use show_ports_info objects for this CLI

        # loop through the ports in portList
        for reply in self.db.show_ports_info(self.args.ports):
            if reply['status'] not in ['MORE', 'SUCCESS']:
                return
            # for each port, collect the VIDs
            self.collect_port_vlan(reply)


    def collect_port_vlan(self, p):
        # collect the untagged and tagged vids for a port
        taggedVlan = []
        untaggedVlan = []

        # loop through the vids for a port and collect then as untagged/tagged
        for reply in self.db.show_ports_info_detail_vlans(p['port']):
            if reply['status'] not in ['MORE', 'SUCCESS']:
                break
            if reply['vlanId'] is None:
                break

            # get vlan object to extract the vlan description
            vlan_reply = self.db.vlan(reply['vlanName'])

            # build an element from VID, Name and VLAN desc
            ventry = (int(reply['vlanId']), reply['vlanName'], vlan_reply['description'])

            self.include_description
            if reply['tagStatus'] == '1':
                taggedVlan.append(ventry)
            else:
                untaggedVlan.append(ventry)

        # print ports as they are collected
        # control output of vids
        if self.port_numbers_only is False:
            port = p['port'] if p['displayString'] is None else p['displayString']
        else:
            # port-number cli options specified
            port = p['port']

        if len(untaggedVlan) == 0 and len(taggedVlan) == 0:
            self.print_port_vlan(port, self.C.PL.NONE, [])
            return

        # always print the untagged line if there are any vids
        self.print_port_vlan(port, self.C.HDR.UNTAGGED, untaggedVlan)

        # print tagged vids if there are any
        if len(taggedVlan):
            self.print_port_vlan('', self.C.HDR.TAGGED, taggedVlan)


    def print_port_vlan(self, port, vtype, vid_list):
        # sort the list into the proper order
        if self.show_vlan_names is True:
            # sort in name order
            vid_list = sorted(vid_list, key=itemgetter(1))
        else:
            # sort in vid order
            vid_list = sorted(vid_list, key=itemgetter(0))

        if self.include_description is True:
            self.print_port_vlan_fmt2(port, vtype, vid_list)
        else:
            self.print_port_vlan_fmt1(port, vtype, vid_list)

# show a quick summary of VIDs on a port
#         Untagged
#Port     /Tagged   VID(s)
#-------- --------  ------------------------------------------------------------
#GiantPortDisplayStri
#         Untagged  1
#         Tagged    30, 31, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
#                   50, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
#                   111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 1000
#2        None      None
#3        Untagged  1
#         Tagged    30, 31, 32, 33, 34, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
#                   50, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
#                   111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 1000
#
# show a quick summary of vlan names on a port
#         Untagged
#Port     /Tagged   VLAN Name(s)
#-------- --------  ------------------------------------------------------------
#davesGiantString
#         Untagged  Default
#         Tagged    BigData, VLAN_0030, VLAN_0031, VLAN_0032, VLAN_0033,
#                   VLAN_0034, VLAN_0040, VLAN_0041, VLAN_0042, VLAN_0043,
#                   VLAN_0044, VLAN_0045, VLAN_0046, VLAN_0047, VLAN_0048,
#                   VLAN_0049, VLAN_0050, VLAN_0100, VLAN_0101, VLAN_0102,
#                   VLAN_0103, VLAN_0104, VLAN_0105, VLAN_0106, VLAN_0107,
#                   VLAN_0108, VLAN_0109, VLAN_0110, VLAN_0111, VLAN_0112,
#                   VLAN_0113, VLAN_0114, VLAN_0115, VLAN_0116, VLAN_0117,
#                   VLAN_0118, VLAN_0119, VLAN_0120
#2        None      None
#3        Untagged  Default
#         Tagged    BigData, VLAN_0030, VLAN_0031, VLAN_0032, VLAN_0033,
#                   VLAN_0034, VLAN_0040, VLAN_0041, VLAN_0042, VLAN_0043,
#                   VLAN_0044, VLAN_0045, VLAN_0046, VLAN_0047, VLAN_0048,
#                   VLAN_0049, VLAN_0050, VLAN_0100, VLAN_0101, VLAN_0102,
#                   VLAN_0103, VLAN_0104, VLAN_0105, VLAN_0106, VLAN_0107,
#                   VLAN_0108, VLAN_0109, VLAN_0110, VLAN_0111, VLAN_0112,
#                   VLAN_0113, VLAN_0114, VLAN_0115, VLAN_0116, VLAN_0117,
#                   VLAN_0118, VLAN_0119, VLAN_0120
#
    def print_port_vlan_fmt1(self, port, vtype, vid_list):
        if len(vid_list):
            disp_list = []
            for vid, vname, vdesc in vid_list:
                if self.show_vlan_names is True:
                    disp_list.append(vname)
                else:
                    disp_list.append('{0:d}'.format(vid))

            # vids contains the entire formated vid list
            vids = ', '.join(disp_list)
        else:
            vids = self.C.PL.NONE

        # max len for vid segments
        max_len = self.C.PL.VID_LEN

        # look for a blank somewhere around where the segment should end
        # then extract that segment for printing
        # then remove that segment from the front of the list
        # keep going as long as there are characters in the vid list
        while len(vids):
            # entire segment fits on the line
            if len(vids) < max_len:
                vid_string = vids
                vids = ''
            else:
                # look for a blank somewhere near the end of the segment
                # then extract the segment from the beginning to that blank
                idx = vids[0:max_len].rfind(' ')
                if idx == -1:
                    # no trailing blank, just use the whole line
                    vid_string = vids
                    vids = ''
                else:
                    # extract the segment and remove it from the list
                    vid_string = vids[0:idx + 1]
                    vids = vids[idx + 1:]

            self.print_fmt1(port=port, vtype=vtype, vids=vid_string)
            port = ''
            vtype = ''


    def print_fmt1(self, port='', vtype='', vids=''):
        if self.print_header is True:
            self.print_heading_fmt1()
        self.output_fmt1(port, vtype, vids)


    def print_heading_fmt1(self):
        # heading
        self.print_header = False
        if self.show_vlan_names is True:
            vid_col_hdr = self.C.HDR.NAME
        else:
            vid_col_hdr = self.C.HDR.VID

        #hdg line 1
        self.output_fmt1(vtype=self.C.HDR.UNTAGGED)

        #hdg line 2
        self.output_fmt1(port=self.C.HDR.PORT,
            vtype='/' + self.C.HDR.TAGGED,
            vids=vid_col_hdr)

        #hdg line 3
        self.output_fmt1(port='-' * self.C.PL.PORT_LEN,
            vtype='-' * self.C.PL.VTYPE_LEN,
            vids='-' * self.C.PL.VID_LEN)


    def output_fmt1(self, port='', vtype='', vids=''):
        fmt = self.C.PL.FMT
        if len(port) > self.C.PL.PORT_LEN:
            line = fmt.format(port=port,
                port_len = self.C.PL.PORT_LEN,
                vtype='',
                vtype_len=self.C.PL.VTYPE_LEN,
                vids='')
            self.show(line)
            port = ''
        line = fmt.format(port=port,
            port_len = self.C.PL.PORT_LEN,
            vtype=vtype,
            vtype_len=self.C.PL.VTYPE_LEN,
            vids=vids)
        self.show(line)


    ################################################################################
    # DISPLAY FORMAT 2
    def print_port_vlan_fmt2(self, port, vtype, vid_list):
        if len(vid_list) == 0:
            self.print_fmt2(port=port, vtype=vtype, vname=self.C.PL2.NONE)
            return

        # max len for vdesc segments
        max_len = self.C.PL2.VDESC_LEN
        for vid, vname, vdesc in vid_list:
            # look for a blank in vdesc somewhere around where the segment should end
            # then extract that segment for printing
            # then remove that segment from the front of the list
            # keep going as long as there are characters in the vid list
            if vdesc is None or len(vdesc) == 0:
                vdesc = ' '
            while len(vdesc):
                # entire segment fits on the line
                if len(vdesc) < max_len:
                    vdesc_string = vdesc
                    vdesc = ''
                else:
                    # look for a blank somewhere near the end of the segment
                    # then extract the segment from the beginning to that blank
                    idx = vdesc[0:max_len].rfind(' ')
                    if idx == -1:
                        # no trailing blank, chop off vdesc at the field len
                        idx = max_len - 1
                    # extract the segment and remove it from the list
                    vdesc_string = vdesc[0:idx + 1]
                    vdesc = vdesc[idx + 1:]

                self.print_fmt2(port=port, vtype=vtype, vid=vid, vname=vname, vdesc=vdesc_string)
                port = ''
                vtype = ''
                vid = ''
                vname = ''


    def print_fmt2(self, port='', vtype='', vid='', vname='', vdesc=''):
        if self.show_vlan_names is True:
            fmt = self.C.PL2.NAME_FMT
        else:
            fmt = self.C.PL2.VID_FMT

        if self.print_header is True:
            self.print_heading_fmt2(fmt)
        self.output_fmt2(fmt, port, vtype, vid, vname, vdesc)


    def print_heading_fmt2(self, fmt):
        # heading
        self.print_header = False

        #hdg line 1
        self.output_fmt2(fmt=fmt, vtype=self.C.HDR2.UNTAGGED)

        #hdg line 2
        self.output_fmt2(fmt=fmt,
            port=self.C.HDR2.PORT,
            vtype='/' + self.C.HDR2.TAGGED,
            vid=self.C.HDR2.VID,
            vname=self.C.HDR2.NAME,
            vdesc=self.C.HDR2.DESC)

        #hdg line 3
        self.output_fmt2(fmt=fmt,
            port='-' * self.C.PL.PORT_LEN,
            vtype='-' * self.C.PL.VTYPE_LEN,
            vid='-' * self.C.PL2.VID_LEN,
            vname='-' * self.C.PL2.VNAME_LEN,
            vdesc='-' * self.C.PL2.VDESC_LEN)


    def output_fmt2(self, fmt='', port='', vtype='', vid='', vname='', vdesc=''):
        if len(port) > self.C.PL.PORT_LEN:
            line = fmt.format(
                port=port,
                port_len=self.C.PL2.PORT_LEN,
                vtype='',
                vtype_len=0,
                vid='',
                vid_len=0,
                vname='',
                vname_len=0,
                vdesc='',
                vdesc_len=0)
            self.show(line)
            port = ''
        line = fmt.format(port=port,
            port_len = self.C.PL2.PORT_LEN,
            vtype=vtype,
            vtype_len=self.C.PL2.VTYPE_LEN,
            vid=vid,
            vid_len=self.C.PL2.VID_LEN,
            vname=vname,
            vname_len=self.C.PL2.VNAME_LEN,
            vdesc=vdesc,
            vdesc_len= self.C.PL2.VDESC_LEN)
        self.show(line)

    def show(self, display_string, force=False):
        # send single line to display. return exception if user enters 'Q'
        print display_string,

c = ShowPortsVid()
c()
