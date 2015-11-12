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
#  Copyright (c) Extreme Networks Inc.    2010,2010
#
#
###
##
##  This is an example on how to use GET ONE XML API.
##  It will read switch ip, username and password from the command line
##
##  Example: "perl getStackInfo.pl 10.0.0.1 admin password"
##  
##  Copyright (c) Extreme Networks Inc.  2010,2010
##  All rights reserved 
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
	
my $method = SOAP::Data->name('switch:getRequest');


# Parameters 
#if you would like check more APIs, please change following values 
my $ns = "system"; #name space of associated Object Type, in this case it is system
my $objectType = "StackNode";   # Object Type, please refer SDK for list of available object types 


# assemble request
my @params = (  SOAP::Data->name("filter" => "")
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
my @stackInfo =  $response->valueof('//objects/object');;

print Dumper(@stackInfo);
