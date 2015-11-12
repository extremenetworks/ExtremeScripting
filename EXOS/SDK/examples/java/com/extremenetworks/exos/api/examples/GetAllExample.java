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
import com.extremenetworks.www.XMLSchema.xos.system.SlotInfo;



/**
 * This is an example of a request to get all slots.
 * The example is based on the operations defined in switch.wsdl
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 * 
 */
public class GetAllExample {

    /**
     * Fetch all slots. This sends a request to get all slots from the switch
     * and prints the information.
     * 
     * Since the get operation works on any object of type ExosBase, the use of
     * SlotInfo can be replaced with the object that needs to be fetched. For example,
     * to fetch all ports from the switch use PortConfig object instead of
     * SlotInfo.
     * 
     * @param stub handle to webservices on the switch
     * @param session webservices session on the switch
     * 
     * @return slots returned from the switch
     */
    public void fetchAllSlots(SwitchPortType stub, Session session) {
	Utilities.log("fetchAllSlots:");

	try {
	    //Object of type ExosBase
	    SlotInfo filter=new SlotInfo(); 


	    GetResponse response=Utilities.sendGetRequest(stub, session,filter);

	    //Response is an array of ExosBase objects
	    for(int i=0;i<response.getObjects().length;i++) {
		SlotInfo slotInfo=(SlotInfo)response.getObjects()[i];
		Utilities.log("Slot: "+slotInfo.getSlotNumber()+" Type: "+slotInfo.getCardType());
	    }



	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
	Utilities.log("fetchAllSlots: DONE");
    }


    /**
     * Main execution method
     * Usage: GetAllExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: GetAllExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    SwitchPortType stub=Utilities.getSwitchPort(device);

	    //Open a new session
	    Session session=Utilities.openSession(stub,username,password);

	    //Execute operations
	    GetAllExample getAllExample=new GetAllExample();
	    getAllExample.fetchAllSlots(stub, session);

	    //Close session 
	    Utilities.closeSession(stub, session);	

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
