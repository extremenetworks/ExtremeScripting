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
##  This is an example on how to use DELETE XML API.
##  It will read switch ip, username and password from the command line
##
##  Example: "perl deletePrivateVlan.pl <host> <id> <password> <pvlan_name> <vlan_name> <vlan_type>"
##  
##  Copyright (c) Extreme Networks Inc.  2006,2007
##  All rights reserved 
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
print "my credentials are $credentials";

#open a session
my $sessionId = opensession($ARGV[0], $ARGV[1], $pwd);
print "Got session id $sessionId"."\n";

# set up connection
my $connection = SOAP::Lite
	-> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10)
	-> ns("http://www.extremenetworks.com/XMLSchema/xos/switch", "switch") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	
my $method = SOAP::Data->name('switch:deleteRequest');


# Parameters 
my $ns = "vlan"; # Name space of associated Object Type, in this case it is vlan
my $objectType = "PrivateVlanMemberConfig";   # Object Type


# assemble request
my @params = (  SOAP::Data->name("filter" =>
                          \SOAP::Data->value(
                                \SOAP::Data->name("vlanName" => $ARGV[4]), 
                                 SOAP::Data->name("pvlanName" => $ARGV[3]), 
                                 SOAP::Data->name("type" => $ARGV[5])))
                          ->type($ns.":".$objectType),
                SOAP::Header->name("hdr" =>
                          \SOAP::Data->value(SOAP::Data->name("sessionId" => $sessionId),
                           SOAP::Data->name("reqId" => "1")))

          );


# send request
my $response = $connection->call($method => @params);

closesession($sessionId, $ARGV[0], $ARGV[1]);

# handle error
if ($response->fault) {
        print "Error received from command - Error is:\n";
	print $response->faultcode, " ", $response->faultstring, "\n"; 
	exit();
}
print "Succesfully Deleted Private Vlan Member\n";
