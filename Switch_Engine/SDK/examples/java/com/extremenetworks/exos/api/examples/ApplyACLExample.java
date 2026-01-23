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

import xapi.AclDirection;
import xapi.AclInsertDirection;
import xapi.PolicyAclAction;
import xapi.PolicyAclCondition;
import xapi.PolicyAclRule;
import xapi.XosPortType;



/**
 * This is an example of a request to create a dynamic ACL and apply it to an interface.
 * The example is based on the operations defined in xos.wsdl
 * 
 * A simple dynamic ACL called "mytestacl1" is created. This ACL performs a "permit" action
 * for tcp traffic going to destination port 80. This ACL is then applied to port 2:1.
 * 
 * Please refer to the EXOS Reference Guide and EXOS Concepts Guide for a detailed description
 * of the ACL feature. 
 * 
 * If an ACL with the name already exists on the switch or there is no port 2:1 the operation
 * will fail with an appropriate error message.
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 * 
 */
public class ApplyACLExample {


    /**
     * Create and apply dynamic ACL on given port.
     * 
     * 
     * @param stub handle to the webservices on the switch
     * @param port the port on which the ACL should be applied
     * 
     */
    public void createAndApplyDynamicACLOnInterface(XosPortType stub, String port) {
	Utilities.log("createAndApplyDynamicACLOnInterface: Port= "+port);

	try {

	    String aclName="mytestacl1";

	    //Create the dynamic ACL first
	    Utilities.log("Creating dynamic ACL "+aclName);

	    //Define the match condition for the ACL
	    //  - tcp traffic going to port 80
	    PolicyAclCondition aclCondition=new PolicyAclCondition();

	    aclCondition.setProtocol("tcp");
	    aclCondition.setDstPort("80");

	    //Define the action in response to the match
	    //   - allow or permit 
	    PolicyAclAction aclAction=new PolicyAclAction();
	    aclAction.setDeny(new Boolean(false));

	    //Now create the dynamic ACL rule
	    PolicyAclRule dynamicAcl=new PolicyAclRule();
	    dynamicAcl.setName(aclName);  //Name of the ACL
	    dynamicAcl.setApplicationName("Cli"); //Using "Cli" as the application name
	    dynamicAcl.setMatch(aclCondition);
	    dynamicAcl.setResponse(aclAction);


	    //Send the request to create the ACL
	    stub.setDynamicAcl(dynamicAcl);

	    //Now apply the ACL to the interface
	    Utilities.log("Applying ACL to port "+port);
	    stub.insertDynamicAclOnInterface(null, port, dynamicAcl.getName(), null, AclInsertDirection.LAST, AclDirection.INGRESS, 0, "SYSTEM", "Cli");



	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}

	Utilities.log("createAndApplyDynamicACLOnInterface: DONE");
    }


    /**
     * Main execution method
     * Usage: ApplyACLExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: ApplyACLExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    XosPortType stub=Utilities.getXosPort(device,username,password);

	    //Execute command
	    ApplyACLExample applyACLExample=new ApplyACLExample();
	    applyACLExample.createAndApplyDynamicACLOnInterface(stub,"2:1");

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
