#!/usr/bin/perl -w
######
#THE INFORMATION AND SPECIFICATIONS IN THIS DEVELOPER KIT ARE SUBJECT TO CHANGE WITHOUT 
#NOTICE.    ALL INFORMATION AND SPECIFICATIONS IN THIS DEVELOPER KIT ARE PRESENTED WITHOUT 
#WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.    YOU TAKE FULL RESPONSIBILITY FOR YOUR USE OF 
#THE DEVELOPER KIT. 
#
# THE DEVELOPER KIT IS LICENSED TO YOU UNDER THE THEN-CURRENT LICENSE TERMS FOR THE    
# DEVELOPER KIT IN EFFECT AT THE TIME THE DEVELOPER KIT IS PROVIDED TO YOU BY 
# EXTREME NETWORKS. PLEASE CONTACT EXTREME NETWORKS IF YOU DO NOT HAVE A COPY OF THE 
# LICENSE TERMS.    USE OF THE DEVELOPER KIT CONSTITUTES YOUR ACCEPTANCE OF THE DEVELOPER 
# KIT LICENSE TERMS.
#
#  Copyright (c) Extreme Networks Inc.    2007,2008,2009,2010
###
##
##  This is an example on how to use getAllFdb API.
##  It will read  switch ip, username and password from the command line
##	
##  Usage: "perl getAllFdb.pl <ip_address> <account> <password>
##
##  Copyright (c) Extreme Networks Inc.  2006,2007
##  All rights reserved 
##  
### 
######
###
###
######
use SOAP::Lite; 
use Data::Dumper;
$Data::Dumper::Indent = 1;
$Data::Dumper::Terse=1;


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
	
# assemble the SOAP Message
my $method = SOAP::Data->name('xos:getAllFdb');


# Assign the Result
$result = $connection->call($method);


# send request
my $response = $connection->call($method);

$connection->close();

if ($result->fault) { 
    print "Error:\n";
    print $result->faultcode, " ", $result->faultstring, "\n"; 
} else {
   my @fdbInfo =  $result->valueof('//getAllFdbResponse/reply');
   print Dumper(@fdbInfo);
}
