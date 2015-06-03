#!/usr/bin/perl -w
######
#THE INFORMATION AND SPECIFICATIONS IN THIS DEVELOPER KIT ARE SUBJECT TO CHANGE WITHOUT 
#
#NOTICE.    ALL INFORMATION AND SPECIFICATIONS IN THIS DEVELOPER KIT ARE PRESENTED WITHOUT 
#
#WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.    YOU TAKE FULL RESPONSIBILITY FOR YOUR USE OF 
#
#THE DEVELOPER KIT. 
#
# 
#
# THE DEVELOPER KIT IS LICENSED TO YOU UNDER THE THEN-CURRENT LICENSE TERMS FOR THE    
#
# DEVELOPER KIT IN EFFECT AT THE TIME THE DEVELOPER KIT IS PROVIDED TO YOU BY 
#
# EXTREME NETWORKS. PLEASE CONTACT EXTREME NETWORKS IF YOU DO NOT HAVE A COPY OF THE 
#
# LICENSE TERMS.    USE OF THE DEVELOPER KIT CONSTITUTES YOUR ACCEPTANCE OF THE DEVELOPER 
#
# KIT LICENSE TERMS.
#
#  
#
#  Copyright (c) Extreme Networks Inc.    2007,2010
#
#
###
##
##  This is an example on how to use SET XML API.
##  It will read switch hostname, username and password from the command line
##
##  Example: "perl setOne.pl 10.0.0.1 admin password"
##  
### 
######

use SOAP::Lite; 
require 'sessionManage.pl';

die "Usage: $0 [host] [username] [password]\n"
	unless ($ARGV[0] && $ARGV[1]);

# handle empty password
my $pwd = "";
my $credentials = "";
defined($ARGV[2]) ? ($pwd = $ARGV[2]) : ($pwd = "");
defined($ARGV[2]) ? ($credentials="$ARGV[1]:$ARGV[2]") : ($credentials="$ARGV[1]:");

#open a session
my $sessionId = opensession($ARGV[0], $ARGV[1], $pwd);
print "Got session id $sessionId"."\n";

# set up connection
my $connection = SOAP::Lite
	-> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10)
	-> ns("http://www.extremenetworks.com/XMLSchema/xos/switch", "switch") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	
my $method = SOAP::Data->name('switch:setRequest');


#PortConfig Parameters 
#if you would like check more APIs, please change following values 
my $ns = "ipfix"; #name space of associated Object Type, in this case it is Port
my $objectType = "IpfixPortData";   # Object Type, please refer SDK for list of available object types 
my $indexParam ="portList";  #This is the Index Paramater for PortConfig, please refer SDK for the meaning of Index Param
my $indeParamValue ="3:1, 3:2";   # This is the Index Parameter Value
my $setParam = "ipfixPortEnabled"; # Parameter Name to be set, Please check SDK for PortConfig parameters
my $setParamValue = "enabled"; # Parameter Value, please check SDK for Parameter value type


# assemble request
my @params = (  SOAP::Data->name("filter" =>
                                            \SOAP::Data->value(SOAP::Data->name("$indexParam" => $indeParamValue), SOAP::Data->name("$setParam" => $setParamValue)))->type($ns.":".$objectType),
                SOAP::Header->name("hdr" =>
                                 \SOAP::Data->value(SOAP::Data->name("sessionId" => $sessionId),
                                 SOAP::Data->name("reqId" => "1")))

          );


# send request
my $response = $connection->call($method => @params);

# close the session
closesession($sessionId, $ARGV[0], $ARGV[1]);

# handle error
if ($response->fault) { 
	print $response->faultcode, " ", $response->faultstring, "\n"; 
	exit();
}
print "Succesfully Set\n";
