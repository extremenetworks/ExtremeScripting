/**
 * THE INFORMATION AND SPECIFICATIONS IN THIS DEVELOPER KIT ARE SUBJECT TO CHANGE WITHOUT NOTICE.
 * ALL INFORMATION AND SPECIFICATIONS IN THIS DEVELOPER KIT ARE PRESENTED WITHOUT WARRANTY OF ANY 
 * KIND, EXPRESS OR IMPLIED.  YOU TAKE FULL RESPONSIBILITY FOR YOUR USE OF THE DEVELOPER KIT. 
 * THE DEVELOPER KIT IS LICENSED TO YOU UNDER THE THEN-CURRENT LICENSE TERMS FOR THE  DEVELOPER 
 * KIT IN EFFECT AT THE TIME THE DEVELOPER KIT IS PROVIDED TO YOU BY EXTREME NETWORKS. 
 * PLEASE CONTACT EXTREME NETWORKS IF YOU DO NOT HAVE A COPY OF THE LICENSE TERMS.  USE OF THE 
 * DEVELOPER KIT CONSTITUTES YOUR ACCEPTANCE OF THE DEVELOPER KIT LICENSE TERMS.
 * 
 * Copyright (c) Extreme Networks Inc.  2007,2008
 */
package com.extremenetworks.exos.api.examples;



import java.util.Map;

import com.extremenetworks.www.XMLSchema.xos._switch.GetResponse;
import com.extremenetworks.www.XMLSchema.xos._switch.SwitchPortType;
import com.extremenetworks.www.XMLSchema.xos.common.Session;
import com.extremenetworks.www.XMLSchema.xos.port.PortUtilizationStats;



/**
 * This is an example of using paging with to get utilization statistics for all ports on a switch.
 * The example is based on the operations defined in switch.wsdl
 * 
 * Please refer to the EXOS Reference Guide and EXOS Concepts Guide for a detailed description
 * of the port statistics and monitoring feature. 
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 * 
 */
public class PortUtilizationExample {

    /**
     * Fetch all port utilization statistics. This sends a request to get all port utilization statistics
     * from the switch using paging
     * 
     * @param stub
     * @param session 
     */
    public void fetchAllPortUtilizationStats(SwitchPortType stub, Session session) {
	Utilities.log("fetchAllPortUtilizationStats:");

	try {
	    //Object of type ExosBase
	    PortUtilizationStats filter=new PortUtilizationStats(); 

	    //number of objects to return in each batch or page
	    int batchSize=10; 

	    //First get request
	    GetResponse response=Utilities.sendGetRequest(stub, session,filter,batchSize);

	    //actual number of objects returned
	    int numberOfObjectsReturned=response.getObjects().length; //

	    while(numberOfObjectsReturned>0) {

		//Response is an array of ExosBase objects
		for(int i=0;i<numberOfObjectsReturned;i++) {
		    PortUtilizationStats portUtilizationStats=(PortUtilizationStats)response.getObjects()[i];
		    Utilities.log("Port: "+portUtilizationStats.getPortList()+" TX BW(%): "+portUtilizationStats.getTransmitBWPercent()+" RX BW(%): "+portUtilizationStats.getReceiveBWPercent());
		}

		//Next batch is retrieved by sending index of last row
		//The index for a PortConfig is the port number (portList attribute)
		PortUtilizationStats lastPort=(PortUtilizationStats)response.getObjects()[numberOfObjectsReturned-1];
		filter.setPortList(lastPort.getPortList());

		//Get next requests
		response=Utilities.sendGetRequest(stub, session,filter,batchSize);
		numberOfObjectsReturned=response.getObjects().length;
	    }


	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}

    }


    /**
     * Main execution method
     * Usage: PortUtilizationExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: PortUtilizationExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    SwitchPortType stub=Utilities.getSwitchPort(device);

	    //Open a new session
	    Session session=Utilities.openSession(stub,username,password);

	    //Execute operations
	    PortUtilizationExample portUtilizationExample=new PortUtilizationExample();
	    portUtilizationExample.fetchAllPortUtilizationStats(stub, session);

	    //Close session 
	    Utilities.closeSession(stub, session);	

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
