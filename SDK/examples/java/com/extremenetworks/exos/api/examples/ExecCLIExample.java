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

import xapi.XosPortType;



/**
 * This is an example of a request to execute a CLI command.
 * The example is based on the operations defined in xos.wsdl
 * 
 * The "show switch" command is executed using execCLI and the output is printed. 
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 * 
 */
public class ExecCLIExample {


    /**
     * Execute CLI command. This sends a execCLI request to execute the command.
     * 
     * The result is the command ouptut as seen from a CLI session.
     * 
     * @param stub handle to the webservices on the switch
     * @param cliCommand CLI command to execute
     * 
     */
    public void execCLI(XosPortType stub, String cliCommand) {
	Utilities.log("execCLI: CLI command= "+cliCommand);

	try {
	    String result=stub.execCli(cliCommand);
	    Utilities.log(result);

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
	Utilities.log("execCLI: DONE");
    }


    /**
     * Main execution method
     * Usage: ExecCLIExample switch=<switch> username=<username> password=<password>
     * 
     * @param args command line arguments
     */
    public static void main(String[] args) {

	Map arguments=Utilities.parseCommandLineArgs(args);

	String device=(String)arguments.get("switch");
	String username=(String)arguments.get("username");
	String password=(String)arguments.get("password");

	if(device==null || username==null) {
	    System.out.println("Usage: ExecCLIExample switch=<switch> username=<username> password=<password>");
	    System.exit(1);
	}

	try {
	    //Get handle to switch web service
	    XosPortType stub=Utilities.getXosPort(device,username,password);

	    //Execute command
	    ExecCLIExample execCLIExample=new ExecCLIExample();
	    execCLIExample.execCLI(stub,"show switch");

	} catch(Exception ex) {
	    Utilities.log("ERROR : "+ex.getMessage());
	}
    }
}
