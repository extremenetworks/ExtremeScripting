#!/usr/bin/env python
# This script connect to the switch and checks the eaps config
# Update 1.02 Added look_for_keys=false for paramiko

__version__ = '1.02'

import telnetlib
import re
import argparse
import sys
import paramiko
import time


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

    def cmd(self,cmd,timeout=30):
        self._tn.write(cmd + "\n")
        s=self._tn.expect([self.prompt],timeout)[2].lstrip(cmd).lstrip('\n\r')
        if s.count('\n')>1:
            return s[:s.rfind('\n')]
        else:
            return "OK"

    def cmdFast(self,cmd,timeout=30):
        self._tn.write(cmd+"\n")
        output=""
        go = True
        while go:
            time.sleep(0.5)
            newoutput = self._tn.read_very_eager()
            if len(newoutput) == 0:
                lastline = output.splitlines()[-1]
                if re.search(self.prompt,lastline):
                    go = False
            else:
                output += newoutput
        return output

class SSH2EXOS:
    def __init__(self, switch, user='admin',password=''):
        self.connected = True
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(switch,username=user,password=password,look_for_keys=False)
        stdin, stdout, stderr = self.client.exec_command("disable clipaging")
        stdin.close()

    def cmdFast(self,cmd,timeout=30):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdin.close()
        return stdout.read()

    def cmd(self,cmd,timeout=30):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdin.close()
        return stdout.read()

    def exit(self):
        self.client.close()
        self.connected = False

    def isConnected(self):
        if self.connected:
            return True
        else:
            return False


def checkIP(address):
    m = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',address)
    if m:
        return m.group(1)
    else:
        return None

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
    # eapsport[domain][primary,secondary,enable/disable]
    eapsports = {}
    eapsvlans = {}
    problems = ""
    for line in data.splitlines():
        m = re.search(r'create eaps (\S+).*',line)
        if m and m.group(1)!="shared-port":
            eapsports[m.group(1)] = ["","","","",""]
        m = re.search(r'configure\seaps\s(\S+)\ssecondary\sport\s(\S+)',line)
        if m and m.group(1)!="shared-port":
            eapsports[m.group(1)][1] = (m.group(2))
        m = re.search(r'configure\seaps\s(\S+)\sprimary\sport\s(\S+)',line)
        if m  and m.group(1)!="shared-port":
            eapsports[m.group(1)][0] = (m.group(2))
        m = re.search(r'(enable|disable)\seaps\s(\S+)',line)
        if m  and m.group(2)!="shared-port":
            eapsports[m.group(2)][2] = (m.group(1))

        m = re.search(r'configure\seaps\s(\S+)\smode\s(transit|master)',line)
        if m:
            eapsports[m.group(1)][3] = (m.group(2))

        # assuming pri/sec ports are always defined before the add of protected eaps vlans we start immediately
        # for search of control/protected vlans
        m3 = re.search(r'configure eaps (\S+) add protected \S+\s(\S+)',line)
        if m3 and "enable" in eapsports[m3.group(1)]:
            if m3.group(1) not in eapsvlans.keys():
                eapsvlans[m3.group(1)]=[]
            eapsvlans[m3.group(1)].append(m3.group(2))
            # Check if primary and secondary port are added to the vlan
            if eapsports[m3.group(1)][0] not in vlanports.get(m3.group(2),[]):
                problems += " - Protected vlan "+m3.group(2)+" ports not added to EAPS "+m3.group(1)
                problems += " port "+eapsports[m3.group(1)][0]+"\n"
            if eapsports[m3.group(1)][1] not in vlanports.get(m3.group(2),[]):
                problems += " - Protected vlan "+m3.group(2)+" ports not added to EAPS "+m3.group(1)
                problems += " port "+eapsports[m3.group(1)][1]+"\n"

        m3 = re.search(r'configure eaps (\S+) add control \S+\s(\S+)',line)
        if m3 and "enable" in eapsports[m3.group(1)]:
            eapsports[m3.group(1)][4] = m3.group(2)
            if m3.group(1) not in eapsvlans.keys():
                eapsvlans[m3.group(1)]=[]
            eapsvlans[m3.group(1)].append(m3.group(2))

            # Check if primary and secondary port are added to the vlan
            if eapsports[m3.group(1)][0] not in vlanports.get(m3.group(2),[]):
                problems += " - Control vlan "+m3.group(2)+" ports not added to EAPS "+m3.group(1)
                problems += " port "+eapsports[m3.group(1)][0]+"\n"
            if eapsports[m3.group(1)][1] not in vlanports.get(m3.group(2),[]):
                problems += " - Control vlan "+m3.group(2)+" ports not added to EAPS "+m3.group(1)
                problems += " port "+eapsports[m3.group(1)][1]+"\n"


    print "Vlan check.."
    sys.stdout.flush()
    for vlan in vlanports.keys():
        for domain in eapsports.keys():
            if eapsports[domain][1] in vlanports[vlan] and eapsports[domain][0] in vlanports[vlan]:
                #both eaps ports in vlan
                if vlan not in eapsvlans[domain]:
                    problems += " - Vlan "+vlan+" added to ringports of eaps domain "+domain+" but not protected by it.\n"

    if len(problems) == 0:
        print "\n[+] No Eaps config problems detected"
    else:
        print "\n[-] Eaps config problems found : "
        print problems
    return eapsports,eapsvlans

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
    masterdomains = []
    for line in data.splitlines():
        m = re.search(r'(\S+)\s+(\S+)\s+(T|M|-)\s+(Y|N).*',line)
        if m:
            domains += 1
            if m.group(3) == "M":
                if m.group(2) == "Complete":
                    masterdomains.append(m.group(1))
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
    if domains == 0:
        print "[-] No Eaps domains found"
    return masterdomains

def vpifcheck(port,vlans,MySess,domain,eapsports):
    print "\n[+] Checking vpif state for eaps domain "+domain+" blocked port "+port
    print "    This can take some time on large vlan/eaps configs."
    problem = False
    for vlan in vlans:
        if vlan != eapsports[domain][4]:
            cmd = "debug vlan show vpif "+vlan+" "+port
            vpifoutput = MySess.cmd(cmd)
            for line in vpifoutput.splitlines():
                m = re.search(r'\s*Ingress:(0x\d+),\s*Egress:\s*(0x\d+).*',line)
                if m:
                    if m.group(1) != "0x22":
                        problem = True
                        print " - Vlan "+vlan+" vpif Ingress state is not Blocking (0x2) on port "+port
                    if m.group(2) != "0x2":
                        problem = True
                        print " - Vlan "+vlan+" vpif Egress state is not Blocking (0x22) on port "+port
    if not problem:
        print " -  All vpif states are correct on port "+port+" for domain "+domain

def main():
    parser = argparse.ArgumentParser(description='Connect to switch and check Eaps config')
    parser.add_argument("-s", dest="switch", default=None, help="Switch IP")
    parser.add_argument("-u", dest="user", default="admin", help="Username")
    parser.add_argument("-p", dest="password", default="", help="Password, leave out for none")
    parser.add_argument("-f", dest="file", default=None, help="File containing switch IP addresses")
    parser.add_argument("--ssh", dest="SSH", action='store_true', help="Use SSH to access switches instead of telnet")
    parser.add_argument("--vpif", dest="vpifcheck", action='store_true', help="Check VPIF state on sec port master")

    args = parser.parse_args()

    switches = []
    vlanports = {}
    validInput = True

    print "\n[Eaps checker version "+__version__+"]\n"
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
                switches.append(checkIP(line))
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
            print "\n[+] Checking switch: "+switch,
            sys.stdout.flush()
            if args.SSH:
                MySess = SSH2EXOS(switch,args.user,args.password)
            else:
                MySess = ExosClass(switch,args.user,args.password)

            if MySess.isConnected():
                vlanports.clear()
                shswitch = MySess.cmdFast("show switch")
                switch = switchData(shswitch)
                print "-SysName: "+switch['Name'], "-HW Type: "+switch['Type']

                vlconf = MySess.cmdFast("show config vlan",60)
                checkconfig(vlconf,vlanports)

                eapsconf = MySess.cmdFast("show config eaps",60)
                eapsports,eapsvlans = eapsCheck(eapsconf,vlanports)


                sheaps = MySess.cmdFast("show eaps")
                masterdomains = eapsStatus(sheaps)

                if args.vpifcheck:
                    #Check vpif state on master secondary port
                    if len(masterdomains) == 0:
                        print "[+] vpif check, no Master domains found, no vpif check needed."
                    for domain in masterdomains:
                        vpifcheck(eapsports[domain][1],eapsvlans[domain],MySess,domain,eapsports)

                print "\n[-] Closing connection"
                print "\n######################\n"
                MySess.exit()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
