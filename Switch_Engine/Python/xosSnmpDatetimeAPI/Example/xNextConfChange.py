import readSnmp
import convertSnmpDate
from datetime import timedelta
from datetime import datetime


#datetime_object = convertSnmpDate.convertSnmpDate2Std('Thu Jul  5 04:51:42 2018 ')
datetime_object = convertSnmpDate.convertSnmpDate2Std(readSnmp.getLastChangeTime())

print ("\nLast Config Update Time : " + str(datetime_object))

print ("\nNext Update after 60 days. ");

afterHow = timedelta(days=60);

nextUpdate = datetime_object + afterHow

print ("\nConfiguration will be Updated on : " + str(nextUpdate)+"\n")
