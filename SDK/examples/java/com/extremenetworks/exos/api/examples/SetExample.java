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

import com.extremenetworks.www.XMLSchema.xos._switch.SwitchPortType;
import com.extremenetworks.www.XMLSchema.xos.common.Session;
import com.extremenetworks.www.XMLSchema.xos.port.PortConfig;



/**
 * This is an example of a request to set the display string of a port.
 * The example is based on the operations defined in switch.wsdl
 * 
 * The display string for port 2:1 is set to "My test port".
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
public class SetExample {


    /**
     * Set port display string. This sends a set request to modify the port.
     * 
     * Since the set operation works on any object of type ExosBase, the use of
     * PortConfig can be replaced with the object that needs to be modified. For example,
     * to modify a VLAN use VlanConfig instead of PortConfig.
     * 
     * @param stub handle to the webservices on the switch
     * @param session webservices session on the switch
     * @param portNumber port to modify
     * @param displayString display string for the port
     */
    public void setPortDisplayString(SwitchPortType stub, Session session, String portNumber, String displayString) {
	Utilities.log("setPortDisplayString: Port number= "+portNumber+", Display string= "+displayString);

	try {
	    //Object of type ExosBase
	    PortConfig filter=new PortConfig(); 

	    filter.setPortList(portNumber);
	    filter.setDisplayString(displayString);


	    Utilities.sendSetRequest(stub, session,filter);


	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}

	Utilities.log("setPortDisplayString: DONE");
    }


    /**
     * Main execution method
     * Usage: SetExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: SetExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    SwitchPortType stub=Utilities.getSwitchPort(device);

	    //Open a new session
	    Session session=Utilities.openSession(stub,username,password);

	    //Execute operations
	    SetExample setExample=new SetExample();
	    setExample.setPortDisplayString(stub, session,"2:1","My test port");

	    //Close session 
	    Utilities.closeSession(stub, session);	

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
