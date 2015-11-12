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
##  This is an example on how to get the details of a policy on the system.
##  It will read the switch hostname, username and password, and the policy
##  name from the command line and will display the policy details.
##
##  Example: "./getPolicy.pl 10.0.0.1 admin password policy_name"
##  
### 
######

use SOAP::Lite; 
use Data::Dumper;
$Data::Dumper::Indent = 1;
$Data::Dumper::Terse=1;

die "Usage: $0 [policy_name] [host] [username] [password]\n" 
	unless ($ARGV[0] && $ARGV[1]);

# handle empty password
my $pwd = "";
my $credentials = "";
defined($ARGV[2]) ? ($pwd = $ARGV[2]) : ($pwd = "");
defined($ARGV[2]) ? ($credentials="$ARGV[1]:$ARGV[2]") : ($credentials="$ARGV[1]:");

#init params

# set up connection
my $connection = SOAP::Lite
	-> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10)
	-> ns("urn:xapi/system/policy", "policy") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	
my $method = SOAP::Data->name('policy:getPolicy');
my @params= (SOAP::Data->name("name")->value("$ARGV[3]"));

# send request
my $result = $connection->call($method => @params);

$connection->close;

if ($result->fault) { 
    print $result->faultcode, " ", $result->faultstring, "\n"; 
} else {
   # print the policy information found
   print "Details of Policy named $ARGV[3]\n";
   print "======================================\n";

   my @policyInfo =  $result->valueof('//getPolicyResponse/reply');
   print Dumper(@policyInfo);
}

