#!/usr/bin/env python
# This script connect to the switch and checks the eaps config

import telnetlib
import re
import argparse
import sys

class ExosClass:
    def __init__(self, host, user='admin',password=''):
        self.host=host
        self.user=user
        self.password=password
        self.prompt=re.compile(r'\S+\d+\s[#>]\s')
        self.loginprompt=r"login"
        self.passwordprompt=r"assword"
        self.failedlogin = r"Login incorrect"
        self.connected = True
        try:
            self._tn = telnetlib.Telnet(self.host)
            self._tn.set_debuglevel(0)
            self._tn.read_until(self.loginprompt,10)
            self._tn.write(self.user + "\n")
            self._tn.expect([self.passwordprompt],10)
            self._tn.write(self.password + "\n")
            loginresponse = self._tn.expect([self.prompt,self.failedlogin])
            if loginresponse[0] == 1:
                print "Login failed"
                self.connected = False
                self._tn.close()
            else:
                self._tn.write("disable clipaging\n")
                self._tn.expect([self.prompt])
        except:
            print "Could not connect to switch "+host
            self.connected = False

    def exit(self):
        self._tn.close()

    def isConnected(self):
        if self.connected:
            return True
        else:
            return False

    def cmd(self,cmd):
        self._tn.write(cmd + "\n")
        s=self._tn.expect([self.prompt])[2].lstrip(cmd).lstrip('\n\r')
        if s.count('\n')>1:
            return s[:s.rfind('\n')]
        else:
            return "OK"

def checkIP(address):
    if re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',address):
        return True
    else:
        return False

def insert_vport(vlanports, vlan, port):
    if vlan not in vlanports.keys():
        vlanports[vlan] = []
    vlanports[vlan].append(port)

def checkconfig(config,vlanports):
    print "Checking config..",
    sys.stdout.flush()
    for line in config.splitlines():
        vp = re.search(r'configure\sv[l|m]an\s(\S+)\sadd\sports\s(.*)',line)
        if vp:
            ports = re.sub('[private-vlan|translated|tagged|untagged|\s]','',vp.group(2))
            if ports.count(':') > 0:
                for prt in ports.split(','):
                    if prt.count('-') == 0:
                        insert_vport(vlanports,vp.group(1),prt)
                    else:
                        modport = prt.split(':')
                        prts = modport[1].split('-')
                        startport = int(prts[0])
                        endport = int(prts[1])
                        while startport <= endport:
                           vlanprt = modport[0]+":"+str(startport)
                           insert_vport(vlanports,vp.group(1),vlanprt)
                           startport += 1
            else:
                for prt in ports.split(','):
                    if prt.count('-') == 0:
                        insert_vport(vlanports,vp.group(1),prt)
                    else:
                        prts = prt.split('-')
                        try:
                           startport = int(prts[0])
                           endport = int(prts[1])
                           while startport <= endport:
                              insert_vport(vlanports,vp.group(1),str(startport))
                              startport += 1
                        except:
                           print "Error on ports, value is :",
                           print prts
                           print line

def eapsCheck(data,vlanports):
    print "Eaps Check start..",
    sys.stdout.flush()
    eapsports = {}
    eapsvlans = {}
    problems = ""
    for line in data.splitlines():
        m = re.search(r'create eaps (\S+).*',line)
        if m and m.group(1)!="shared-port":
            eapsports[m.group(1)] = []
        m1 = re.search(r'configure\seaps\s(\S+)\ssecondary\sport\s(\S+)',line)
        if m1 and m1.group(1)!="shared-port":
            eapsports[m1.group(1)].append(m1.group(2))
        m2 = re.search(r'configure\seaps\s(\S+)\sprimary\sport\s(\S+)',line)
        if m2  and m2.group(1)!="shared-port":
            eapsports[m2.group(1)].append(m2.group(2))
        m2 = re.search(r'(enable|disable)\seaps\s(\S+)',line)
        if m2  and m2.group(2)!="shared-port":
            eapsports[m2.group(2)].append(m2.group(1))
        # assuming pri/sec ports are always defined before the add of protected eaps vlans we start immediately
        # for search of control/protected vlans
        m3 = re.search(r'configure eaps (\S+) add protected \S+\s(\S+)',line)
        if m3 and "enable" in eapsports[m3.group(1)]:
            if m3.group(1) not in eapsvlans.keys():
                eapsvlans[m3.group(1)]=[]
            eapsvlans[m3.group(1)].append(m3.group(2))
            # Check if primary and secondary port are added to the vlan
            for vport in eapsports[m3.group(1)]:
                if vport !=  "enable" and vport != "disable":
                    if vport not in vlanports.get(m3.group(2),[]):
                        #print vport, m3.group(1), vlanports.get(m3.group(2),[]), "<br>"
                        problems += " - Protected vlan "+m3.group(2)+" ports not added to EAPS "+m3.group(1)
                        problems += " port "+vport+"\n"
        m3 = re.search(r'configure eaps (\S+) add control \S+\s(\S+)',line)
        if m3 and "enable" in eapsports[m3.group(1)]:
            if m3.group(1) not in eapsvlans.keys():
                eapsvlans[m3.group(1)]=[]
            eapsvlans[m3.group(1)].append(m3.group(2))

            # Check if primary and secondary port are added to the vlan
            for vport in eapsports[m3.group(1)]:
                if vport !=  "enable" and vport != "disable" and vport not in vlanports.get(m3.group(2),[]):
                    problems += " - Control vlan "+m3.group(2)+" ports not added to EAPS "+m3.group(1)
                    problems += " port "+vport+"\n"

    print "Vlan check.."
    sys.stdout.flush()
    for vlan in vlanports.keys():
        for domain in eapsports.keys():
            if eapsports[domain][1] in vlanports[vlan] and eapsports[domain][0] in vlanports[vlan]:
                #both eaps ports in vlan
                if vlan not in eapsvlans[domain]:
                    problems += " - Vlan "+vlan+" added to ringports of eaps domain "+domain+" but not protected by it.\n"

    if len(problems) == 0:
        print "[+] No Eaps config problems detected"
    else:
        print "[-] Eaps config problems found : "
        print problems

def switchData(data):
    switch = {}
    for line in data.splitlines():
        m = re.search(r'SysName:\s+(\S+)',line)
        if m:
            switch['Name'] = m.group(1)
        m = re.search(r'System Type:\s+(\S+)',line)
        if m:
            switch['Type'] = m.group(1)
    return switch

def eapsStatus(data):
    problems = ""
    domains = 0
    for line in data.splitlines():
        m = re.search(r'(\S+)\s+(\S+)\s+(T|M|-)\s+(Y|N).*',line)
        if m:
            domains += 1
            if m.group(3) == "M":
                if m.group(2) == "Complete":
                    continue
                elif m.group(4) == "N":
                    problems += " - "+m.group(1)+" domain not enabled.\n"
                else:
                    problems += " - "+m.group(1)+" Status "+m.group(2)+".\n"
            if m.group(3) == "T":
                if m.group(2) == "Links-Up":
                    continue
                elif m.group(4) == "N":
                    problems += " - "+m.group(1)+" domain not enabled.\n"
                else:
                    problems += " - "+m.group(1)+" Status "+m.group(2)+".\n"
    if len(problems) > 1:
        print "[-] Problem eaps domains status found."
        print problems
    else:
        print "[+] Eaps status for all "+str(domains)+" domains OK"


def main():
    parser = argparse.ArgumentParser(description='Connect to switch and check Eaps config')
    parser.add_argument("-s", dest="switch", default=None, help="Switch IP")
    parser.add_argument("-u", dest="user", default="admin", help="Username")
    parser.add_argument("-p", dest="password", default="", help="Password, leave out for none")
    parser.add_argument("-f", dest="file", default=None, help="File containing switch IP addresses")

    args = parser.parse_args()

    switches = []
    vlanports = {}
    validInput = True

    if args.switch:
        if checkIP(args.switch):
            switches.append(args.switch)
        else:
            print "No Valid IP address specified with -s"
            validInput = False
    elif args.file:
        try:
            f = open(args.file,'r')
            for line in f.read().splitlines():
                if checkIP(line):
                    switches.append(line)
            f.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Something wrong with opening the file"
            validInput = False
    else:
        print "No valid option -s or -f specified"
        validInput = False

    if validInput:
        for switch in switches:
            print "Checking switch "+switch,
            sys.stdout.flush()
            MySess = ExosClass(switch,args.user,args.password)
            if MySess.isConnected():
                shswitch = MySess.cmd("show switch")
                switch = switchData(shswitch)
                print switch['Name'], switch['Type']

                vlconf = MySess.cmd("show config vlan")
                checkconfig(vlconf,vlanports)

                eapsconf = MySess.cmd("show config eaps")
                eapsCheck(eapsconf,vlanports)

                sheaps = MySess.cmd("show eaps")
                eapsStatus(sheaps)

                MySess.exit()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass