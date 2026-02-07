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
import com.extremenetworks.www.XMLSchema.xos.vlan.VlanConfig;




/**
 * This is an example of a request to create a new VLAN.
 * The example is based on the operations defined in switch.wsdl
 * 
 * A VLAN with name "myVlan1" is created on VR "VR-Default". 
 * 
 * Please refer to the EXOS Reference Guide and EXOS Concepts Guide for a detailed description
 * of the VLAN feature. 
 * 
 * If a VLAN with the name already exists on the switch the operation will fail with an appropriate 
 * error message.
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 * 
 */
public class CreateExample {

    /**
     * Create new VLAN. This sends a create request to create new VLAN on the switch.
     * 
     * Since the create operation works on any object of type ExosBase, the use of
     * VlanConfig can be replaced with the object that needs to be created. For example,
     * to create a new user account use UserAccount instead of VlanConfig.
     * 
     * @param stub handle to the webservices on the switch
     * @param session webservices session on the switch
     * @param vlanName name of new VLAN
     * @param vrName name of VR for the VLAN
     */
    public void createVLAN(SwitchPortType stub, Session session, String vlanName, String vrName) {
	Utilities.log("createVLAN: VLAN Name= "+vlanName+", VR Name= "+vrName);

	try {
	    //Object of type ExosBase
	    VlanConfig filter=new VlanConfig(); 

	    filter.setName(vlanName);
	    filter.setVrName(vrName);

	    Utilities.sendCreateRequest(stub, session,filter);

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
	Utilities.log("createVLAN: DONE");
    }


    /**
     * Main execution method
     * Usage: CreateExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: CreateExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    SwitchPortType stub=Utilities.getSwitchPort(device);

	    //Open a new session
	    Session session=Utilities.openSession(stub,username,password);

	    //Execute operations
	    CreateExample createExample=new CreateExample();
	    createExample.createVLAN(stub, session,"myVlan1","VR-Default");

	    //Close session 
	    Utilities.closeSession(stub, session);	

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
