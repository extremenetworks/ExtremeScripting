import readSnmp
import convertSnmpDate
from datetime import datetime

#datetime_object = convertSnmpDate.convertSnmpDate2Std('Thu Jul  5 04:51:42 2018 ')
datetime_object = convertSnmpDate.convertSnmpDate2Std(readSnmp.getLastChangeTime())

print ("\nLast Config Update Time : " + str(datetime_object))

currentdate = datetime.now()

print ("Current time            : " + str(currentdate))

diff = currentdate - datetime_object 

print ("\nConfiguration not Updated for last " + str(diff)+"\n")
