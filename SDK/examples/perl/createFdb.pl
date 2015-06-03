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
#  Copyright (c) Extreme Networks Inc.    2007,2008
#
#
###
##
##  This is an example on how to use CREATE XML API.
##  It will read switch ip, username and password from the command line
##
##  Example: "perl createFdb.pl 10.0.0.1 admin password mac-address vlan port"
##  
##  Copyright (c) Extreme Networks Inc.  2006,2007
##  All rights reserved 
##  
### 
######

use SOAP::Lite; 

die "Usage: $0 [host] [username] [password] [mac-address] [vlan] [port]\n"
	unless ($ARGV[0] && $ARGV[1]);

# handle empty password
my $pwd = "";
my $credentials = "";
defined($ARGV[2]) ? ($pwd = $ARGV[2]) : ($pwd = "");
defined($ARGV[2]) ? ($credentials="$ARGV[1]:$ARGV[2]") : ($credentials="$ARGV[1]:");


# set up connection
my $connection = SOAP::Lite
	-> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10)
	-> ns("urn:xapi/l2protocol/fdb", "xos") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	
my $method = SOAP::Data->name('xos:createFdb');
my @params= (SOAP::Data->name("macAddress")->value("$ARGV[3]"),
             SOAP::Data->name("vlan")->value("$ARGV[4]"),
             SOAP::Data->name("port")->value("$ARGV[5]"));


# send request
my $response = $connection->call($method => @params);

$connection->close;

# handle error
if ($response->fault) { 
	print $response->faultcode, " ", $response->faultstring, "\n"; 
	exit();
}
print "Succesfully Created\n";
