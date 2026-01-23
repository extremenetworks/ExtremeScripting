from easysnmp import Session

def getLastChangeTime():
    session = Session(hostname='IP address', community='community', version=2)
    lChange = session.get('.1.3.6.1.4.1.1916.1.42.1.1.1.2.1')
    return(lChange.value)

