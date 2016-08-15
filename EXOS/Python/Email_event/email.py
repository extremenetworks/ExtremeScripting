import smtplib
import sys
import re
import datetime
from email.mime.text import MIMEText

def sendemail(txt,me,to,smtp):
    msg = {}
    msg['From'] = me
    s = smtplib.SMTP(smtp)
    s.sendmail(me, [to], txt)
    s.quit()

def switchData():
    data = exsh.clicmd("show switch",capture=True)
    switch = {}
    for line in data.splitlines():
        m = re.search(r'SysName:\s+(\S+)',line)
        if m:
            switch['Name'] = m.group(1)
    return switch

def LogLines(minutes=10):
    now = datetime.datetime.now()
    logstart = now - datetime.timedelta(minutes=minutes)
    cmd = "show log starting time " + logstart.strftime('%H:%M:%S')
    log = exsh.clicmd(cmd,capture=True)
    return log

def ChgVR(vr):                                                     
    try:                                                           
        f = open('/proc/self/ns_id', 'w')                          
        f.write(vr+'\n')                                           
        f.close()                                                  
        return True                                                
    except:                                                        
        return False                                               
                                                                   
                                                                   
def main():                                                        
    ###################################                            
    # Start User changeable parameters                             
    ###################################                            
    # Change below myVirtualRouter to the VR used to reach the smtp server
    # 2 Vr-Default                                                        
    # 0 VR-Mgmt                                                           
    # Any other number the number of your user created VR.                
                                                                          
    myVirtualRouter = 2                                                   
                                                                          
    FromDomain = "okoot@extremenetworks.com"                              
    to = 'okoot@extremenetworks.com'                                      
    smtp = 'smtp.extremenetworks.com'                                     
                                                                          
    ###################################                                   
    # End User changeable parameters                                      
    ###################################                                   
                                                                          
    if ChgVR(str(myVirtualRouter)):                                       
        exsh.clicmd("disable clipaging")                                  
        switch = switchData()                                             
        msg = "Port Status change on "+switch['Name']+"\n\n"              
        if sys.argv[2] == "down":                                         
            msg += "Port "+sys.argv[1]+" went down"+"\n"    
        else:                                               
            msg += "Port "+sys.argv[1]+" UP, speed "+sys.argv[2]+" "+sys.argv[3]+"\n"
                                                                                     
        msg += "\nLast 10 minutes log"+"\n"                                          
        msg += LogLines(minutes=10)                                                  
        me = switch['Name']+FromDomain                                               
        sendemail(msg,me,to,smtp)                                                    
    else:                                                                            
        exsh.clicmd("create log message \"Unable to send Email on log event\"")     

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
