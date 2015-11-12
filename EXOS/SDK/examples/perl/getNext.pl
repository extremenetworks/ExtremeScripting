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
##  This is an example to demonstarte XML API Paging Support
##  
##  It will read  switch ip, username and password from the command line
##  and will give back the Next available objects provided Size and Index Parameter Value, if index is not passed first 'n' number of objects returned.
##
##  Example: "perl getNext.pl 10.0.0.1 admin password"
##  
### 
######

use SOAP::Lite; 
require 'sessionManage.pl';
use Data::Dumper;
$Data::Dumper::Indent = 1;
$Data::Dumper::Terse=1;

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
	


#Get Next API Parameters
#if you would like check more APIs, please change following values 
my $ns = "port"; #name space of associated Object Type, in this case it is Port
my $objectType = "PortConfig";   # Object Type, please refer SDK for list of available object types 
my $indexParam ="portList";  #This is the Index Paramater for PortConfig, please refer SDK for the menaing of Index Param; 
                             #If the index attribute is not set, first $nextSize will be returned provided $actionType="next"
my $indeParamValue ="1:1";   # This is the Index Parameter Value
my $actionType = "next";  # Only action supported is "next"
my $nextSize = "5";   # Number of objects to be retrieved, if this  value is not passed EXOS sets to 1 

my $method = SOAP::Data->name("switch:getRequest")
                       ->attr({"action" => $actionType, "maxSize" => $nextSize});

# assemble request
my @params = (  SOAP::Data->name("filter" =>
                                \SOAP::Data->value(SOAP::Data->name("$indexParam" => $indeParamValue)))
                          ->type($ns.":".$objectType),
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

# get values from response and dump on the screen
my @portInfo =  $response->valueof('//objects/object');;

print Dumper(@portInfo);

