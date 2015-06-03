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
##  This is an example on how to create a dynamic acl and bind it to a specific port.
##  It will read the port, switch hostname, acl name, username and password from the 
##  command line and will create an ACL to block tcp port 25 of the given switch port.
##
##  Example: "perl setDynAcl.pl 10.0.0.1 admin password"
##  
### 
######

use SOAP::Lite; 

die "Usage: $0 [host] [username] [password]\n" 
	unless ($ARGV[0] && $ARGV[1]);

# handle empty password
my $pwd = "";
my $credentials = "";
defined($ARGV[2]) ? ($pwd = $ARGV[2]) : ($pwd = "");
defined($ARGV[2]) ? ($credentials="$ARGV[1]:$ARGV[2]") : ($credentials="$ARGV[1]:");

#init params
my $port = "1:1"; #Please check switch platform for PortId format
my $aclName = "testAcl3";

# set up connection
my $connection = SOAP::Lite
	-> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10)
	-> ns("urn:xapi/l2protocol/acl", "acl") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	
my $createACL = SOAP::Data->name('acl:setDynamicAcl');
my $bindACL = SOAP::Data->name('acl:insertDynamicAclOnInterface');

# assemble acl
my @params1 = (	SOAP::Data->name("rule" => SOAP::Data->name("rule" =>
                         \SOAP::Data->value(SOAP::Data->name("name" => $aclName),
	                                    SOAP::Data->name("applicationName" => "Cli"),
	                                    SOAP::Data->name("match" =>
	                                        \SOAP::Data->value(SOAP::Data->name("dstPort" => "25"),
			                                           SOAP::Data->name("protocol" => "TCP"))),
			                    SOAP::Data->name("response" => 
                                                \SOAP::Data->name("deny" => "true")))))
	      );
			
# assemble acl binding
my @params2 = ( SOAP::Data->name("port" => $port),
	        SOAP::Data->name("newRule" => $aclName),
                SOAP::Data->name("applicationName" => "Cli"),
	        SOAP::Data->name("direction" => "BEFORE"));
		
# send acl request
my $result1 = $connection->call($createACL => @params1);
handleError($result1);

# send acl binding
my $result2 = $connection->call($bindACL => @params2);
handleError($result2);

sub handleError {
	my $res = shift;
	if ($res->fault) { 
                print "Got error:\n";
		print $res->faultcode, " ", $res->faultstring, "\n"; 
		exit();
	}
}
