import readSnmp 
import convertSnmpDate 
from datetime import datetime

#datetime_object = convertSnmpDate.convertSnmpDate2Std('Thu Jul  5 04:51:42 2018 ')
datetime_object = convertSnmpDate.convertSnmpDate2Std(readSnmp.getLastChangeTime());

print ("\nLast Config Update Time : " + str(datetime_object)+"\n");

