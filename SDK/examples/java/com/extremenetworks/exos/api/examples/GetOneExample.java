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
import com.extremenetworks.www.XMLSchema.xos.port.PortConfig;




/**
 * This is an example of a request to get the details of a port.
 * The example is based on the operations defined in switch.wsdl
 * 
 * The switch is queried for details of port 1:2. 
 * 
 * Please refer to the EXOS Reference Guide and EXOS Concepts Guide for a detailed description
 * of port configuration. 
 * 
 * If the port does not exist on the switch the operation will fail with an appropriate 
 * error message.
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 * 
 */
public class GetOneExample {

    /**
     * Fetch port details. This sends a request to get details of a port from the switch
     * and prints the information. The port number is set in portList which is the index
     * attribute for the PortConfig object. 
     * 
     * Since the get operation works on any object of type ExosBase, the use of
     * PortConfig can be replaced with the object that needs to be fetched. For example,
     * to fetch a VLAN from the switch use VlanConfig object instead of PortConfig.
     * 
     * @param stub
     * @param session 
     * @param portNumber port to be fetched
     * 
     * @return port returned from the switch
     */
    public void fetchPort(SwitchPortType stub, Session session, String portNumber) {
	Utilities.log("fetchPort: Port= "+portNumber);

	try {
	    //Object of type ExosBase
	    PortConfig filter=new PortConfig();
	    filter.setPortList(portNumber);

	    GetResponse response=Utilities.sendGetRequest(stub, session,filter);

	    //Response is an array of ExosBase objects
	    //Since query is for specific object this will be an array
	    //of size 1 (or size 0 if object is not found).
	    for(int i=0;i<response.getObjects().length;i++) {
		PortConfig portConfig=(PortConfig)response.getObjects()[i];
		Utilities.log("Port: "+portConfig.getPortList()+" Link State: "+portConfig.getLinkState());
	    }

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
	Utilities.log("fetchPort: DONE");
    }


    /**
     * Main execution method
     * Usage: GetOneExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: GetOneExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    SwitchPortType stub=Utilities.getSwitchPort(device);

	    //Open a new session
	    Session session=Utilities.openSession(stub,username,password);

	    //Execute operations
	    GetOneExample getOneExample=new GetOneExample();
	    getOneExample.fetchPort(stub, session,"1:2");

	    //Close session 
	    Utilities.closeSession(stub, session);	

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
