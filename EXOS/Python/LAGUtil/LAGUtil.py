import sys, select         
import re
import xml.etree.cElementTree as ElementTree
import datetime
import time

__version__ = "0.1"

def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

def cmd2data(clicmd):
    re_reply = re.compile(r'<reply>.+?</reply>', re.DOTALL)
    xmlout = exsh.clicmd(clicmd, capture=False, xml=True)
    data = []
    for reply in re.finditer(re_reply, xmlout):
        if reply:
            reply_xml = reply.group()
            root = ElementTree.fromstring(reply_xml)
            for message in root.iter('message'):
                for element in message:
                    mdata = {}
                    edata = {}
                    for e in element:
                        text = int(e.text) if e.text is not None and e.text.isdigit() else e.text
                        edata[e.tag] = text
                    mdata[element.tag] = edata
                    data.append(mdata)
    return data

def percent(bytes,max):
    usage = ((float(bytes)/float(max))*100)/125000
    return "%0.2f" % usage

 
def TimedInput(waittime): 
    i, o, e = select.select( [sys.stdin], [], [], waittime )
    if (i):                                                     
        return sys.stdin.readline().strip()            
    else:                                                       
        return False

def main():
    print chr(27) + "[2J"
    sharing = cmd2data("show ports sharing")  
    sharports = {}                          
    sharportsspeed = {}                     
    for e in sharing:                       
        if 'ls_ports_show' in e.keys():     
            masterport = e['ls_ports_show']['loadShareMaster']
            memberport = e['ls_ports_show']['port']        
            if masterport in sharports.keys():             
                sharports[masterport].append(memberport) 
            else:                                   
                sharports[masterport] = []          
                sharportsspeed[masterport] = []         
                sharports[masterport].append(memberport)
                                                    
    for mport in sorted(sharports):                                             
        speed = 0                                                               
        for port in sharports[mport]:                                           
            cmd = "show port "+str(port)+" conf no-refresh"                          
            portinfo = cmd2data(cmd)                                            
            if portinfo[0]['show_ports_config']['speedActual']:                 
                speed += portinfo[0]['show_ports_config']['speedActual']
        sharportsspeed[mport] = speed         

    print_there(2,2,"Lag total utilization %")
    print_there(2,35,datetime.datetime.now().strftime(" %b %d %Y %H:%M:%S"))
    print_there(5,2,"LAG (Total Speed)")             
    print_there(5,28,"Rx (%)")
    print_there(5,43,"Tx (%)")
    print_there(6,1,"=======================================================")
    linenum = 8

    for lag in sharports.keys():
        lagspeed = str(sharportsspeed[lag]/1000)+"Gb"
        print_there(linenum,2,str(lag))
        print_there(linenum,15-len(lagspeed),lagspeed)
        linenum += 1

    
    print_there(linenum+1,1,"=======================================================")
    print_there(linenum+2,36,"Hit q<enter> to quit")

    poll = 0
    keystroke = False
    while not keystroke:
        linenum = 8
        print_there(2,35,datetime.datetime.now().strftime(" %b %d %Y %H:%M:%S"))
        for lag in sharports.keys():
            plist = ','.join(str(x) for x in sharports[lag])
            util = cmd2data("show ports "+plist+" util bytes")  
            rx = 0
            tx = 0
            for prt in util:
                rx += prt['show_ports_utilization']['rxBytesPerSec']
                tx += prt['show_ports_utilization']['txBytesPerSec']
            rx_percent = percent(rx,sharportsspeed[lag])
            tx_percent = percent(tx,sharportsspeed[lag])
            print_there(linenum,33-len(rx_percent),rx_percent)
            print_there(linenum,48-len(tx_percent),tx_percent)
            linenum += 1
        poll += 1
        keystroke = TimedInput(1)
 
if __name__ == "__main__":                  
    try:                                                      
        main()                                                
    except SystemExit:                                     
        pass
