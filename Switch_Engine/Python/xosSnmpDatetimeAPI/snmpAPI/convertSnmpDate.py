from datetime import datetime

def convertSnmpDate2Std(lastChangeSNMP):
    datetime_object = datetime.strptime(lastChangeSNMP,'%a %b  %d %H:%M:%S %Y ')
    return datetime_object
