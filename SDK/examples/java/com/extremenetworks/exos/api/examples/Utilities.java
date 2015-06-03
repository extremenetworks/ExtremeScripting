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

import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import org.apache.axis.types.UnsignedInt;

import xapi.XosLocator;
import xapi.XosPortType;



import com.extremenetworks.www.XMLSchema.xos._switch.CreateRequest;
import com.extremenetworks.www.XMLSchema.xos._switch.CreateResponse;
import com.extremenetworks.www.XMLSchema.xos._switch.DeleteRequest;
import com.extremenetworks.www.XMLSchema.xos._switch.DeleteResponse;
import com.extremenetworks.www.XMLSchema.xos._switch.GetRequest;
import com.extremenetworks.www.XMLSchema.xos._switch.GetResponse;
import com.extremenetworks.www.XMLSchema.xos._switch.SetRequest;
import com.extremenetworks.www.XMLSchema.xos._switch.SetResponse;
import com.extremenetworks.www.XMLSchema.xos._switch.SwitchPortType;
import com.extremenetworks.www.XMLSchema.xos._switch._switchLocator;
import com.extremenetworks.www.XMLSchema.xos.common.ClientHeader;
import com.extremenetworks.www.XMLSchema.xos.common.CloseSessionReply;
import com.extremenetworks.www.XMLSchema.xos.common.CloseSessionRequest;
import com.extremenetworks.www.XMLSchema.xos.common.ExosBase;
import com.extremenetworks.www.XMLSchema.xos.common.OpenSessionReply;
import com.extremenetworks.www.XMLSchema.xos.common.OpenSessionRequest;
import com.extremenetworks.www.XMLSchema.xos.common.Session;
import com.extremenetworks.www.XMLSchema.xos.common.holders.ClientHeaderHolder;



/**
 * Some convenience methods used across various examples.
 * 
 * NOTE: This example code is for illustration purposes only. 
 * The choice of attributes, values and error handling is simplified to emphasis the API functionality.
 */

public class Utilities {

    /**
     * Convenience method to log messages to stdout
     * 
     * @param message the message to be logged
     */
    public static void log(String message) {
	System.out.println(Calendar.getInstance().getTime() + ": " + message);
    }

    /**
     * Get a handle to the webservice on the switch. This provides the binding
     * for switch.wsdl
     * 
     * @param device switch to talk to
     * @param protocol protocol to use. Can be HTTP or HTTPS.
     * @return handle to the webservice on the switch.
     * @throws Exception
     */
    public static SwitchPortType getSwitchPort(String device) throws Exception {
	_switchLocator xl = new _switchLocator();
	java.net.URL url;

	url = new java.net.URL("http://" + device + "/xmlService");

	log("Binding to service at " + url);

	SwitchPortType stub = xl.getswitchPort(url);


	return stub;
    }

    /**
     * Get a handle to the webservice on the switch. This provides the binding
     * for xos.wsdl
     * 
     * @param device switch to talk to
     * @param protocol protocol to use. Can be HTTP or HTTPS.
     * @return handle to the webservice on the switch.
     * @throws Exception
     */
    public static XosPortType getXosPort(String device, String username, String password) throws Exception {
	XosLocator xl=new XosLocator();
	java.net.URL url=new java.net.URL("http://"+device+"/xmlService");

	log("Binding to service at "+url);

	XosPortType stub=xl.getXosPort(url);

	if(username!=null) ((org.apache.axis.client.Stub)stub).setUsername(username);
	if(password!=null) ((org.apache.axis.client.Stub)stub).setPassword(password);

	return stub;
    }	

    /**
     * Open a webservice session on the webservice.
     * 
     * @param stub handle to the webservice on the switch
     * @param username username to login to the switch
     * @param password 
     * 
     * @return session
     * @throws Exception
     */
    public static Session openSession(SwitchPortType stub, String username, String password) throws Exception {
	log("Open session request: username=" + username);

	Session session = new Session();

	session.setUsername(username);
	session.setPassword(password);

	session.setAppName("API Test Client");


	OpenSessionRequest request = new OpenSessionRequest();
	request.setSession(session);

	OpenSessionReply reply = stub.openSession(request);

	log("Session id: " + reply.getSession().getSessionId());
	return reply.getSession();
    }

    /**
     * Close a webservice session on the switch.
     * 
     * @param stub handle to the webservice on the switch
     * @param session to close
     * 
     * @return response with confirmation of close session
     * @throws Exception
     */
    public static CloseSessionReply closeSession(SwitchPortType stub, Session session) throws Exception {
	log("closeSession:");

	CloseSessionRequest request = new CloseSessionRequest();
	request.setSessionId(session.getSessionId());

	return stub.closeSession(request);
    }

    /**
     * Send get request. 
     * 
     * @param stub handle to webservice on the switch
     * @param session webservice session on the switch
     * @param exosBase filter for the get request
     * 
     * @return response with data for the get request
     * @throws Exception
     */
    public static GetResponse sendGetRequest(SwitchPortType stub, Session session, ExosBase exosBase) throws Exception { 

	return sendGetRequest(stub,session,exosBase, 0);
    }

    /**
     * Send get request and specify maximum number of objects to be returned.
     * 
     * @param stub handle to webservice on the switch
     * @param session webservice session on the switch
     * @param exosBase filter for the get request
     * @param maxSize maximum number of objects to return, 0 indicates return all objects
     * 
     * @return response with data for the get request
     * @throws Exception
     */
    public static GetResponse sendGetRequest(SwitchPortType stub, Session session, ExosBase exosBase, int maxSize) throws Exception {
	ClientHeader header = new ClientHeader();
	header.setReqId(new UnsignedInt(1)); 
	header.setSessionId(session.getSessionId());

	ClientHeaderHolder headerHolder = new ClientHeaderHolder(header);


	GetRequest request = new GetRequest();
	request.setFilter(exosBase);

	if(maxSize>0) {
	    request.setAction("next");
	    request.setMaxSize(maxSize);
	}

	return stub.get(headerHolder, request);
    }


    /**
     * Send set request
     * 
     * @param stub handle to webservice on the switch
     * @param session webservice session on the switch
     * @param exosBase object for the set request
     * 
     * @return response with data for the get request
     */
    public static SetResponse sendSetRequest(SwitchPortType stub, Session session, ExosBase exosBase) throws Exception {
	ClientHeader header = new ClientHeader();
	header.setReqId(new UnsignedInt(1)); 
	header.setSessionId(session.getSessionId());

	ClientHeaderHolder headerHolder = new ClientHeaderHolder(header);

	SetRequest request = new SetRequest();

	request.setFilter(exosBase);

	return stub.set(headerHolder,request);
    }

    /**
     * Send create request
     * 
     * @param stub handled to webservice on the switch
     * @param session webservice session on the switch
     * @param exosBase object for the create request
     * 
     * @return response with data for the create request
     */
    public static CreateResponse sendCreateRequest(SwitchPortType stub, Session session, ExosBase exosBase) throws Exception {
	ClientHeader header = new ClientHeader();
	header.setReqId(new UnsignedInt(1)); 
	header.setSessionId(session.getSessionId());

	ClientHeaderHolder headerHolder = new ClientHeaderHolder(header);

	CreateRequest request = new CreateRequest();

	request.setFilter(exosBase);

	return stub.create(headerHolder,request);
    }

    /**
     * Send delete request
     * 
     * @param stub handle to webservice on the switch
     * @param session webservice session on the switch
     * @param exosBase object for the delete request
     * 
     * @return response with data for the delete request
     */
    public static DeleteResponse sendDeleteRequest(SwitchPortType stub, Session session, ExosBase exosBase) throws Exception {
	ClientHeader header = new ClientHeader();
	header.setReqId(new UnsignedInt(1)); 
	header.setSessionId(session.getSessionId());

	ClientHeaderHolder headerHolder = new ClientHeaderHolder(header);

	DeleteRequest request = new DeleteRequest();

	request.setFilter(exosBase);

	return stub.delete(headerHolder,request);
    }


    /**
     * Convenience method to parse values passed through command line arguments.
     * Supports arguments of the formats "arg1=val1" and "arg2". In the first case
     * it is parsed as a key-value pair with "arg1" as the key and "val1" as the value.
     * In the second case "arg2" is the key with null as the value. 
     * 
     * @param args command line arguments
     * @return map containing key-value pairs
     */
    public static Map parseCommandLineArgs(String[] args) {
	Map keyValues=new HashMap();

	for(int i=0;i<args.length;i++) {
	    String[] tmp=args[i].split("=");

	    if(tmp.length==2) keyValues.put(tmp[0],tmp[1]);
	    else if(tmp.length==1) keyValues.put(tmp[0],null);

	}

	return keyValues;
    }
}
