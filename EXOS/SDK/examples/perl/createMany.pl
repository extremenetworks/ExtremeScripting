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
##  This is an example on how to use SET XML API.
##  It will read switch hostname, username and password from the command line
##
##  Example: "perl createMany.pl 10.0.0.1 admin password"
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
	
my $method = SOAP::Data->name('switch:createRequest');


#VlanConfig Parameters 
#if you would like check more APIs, please change following values 
my $ns = "vlan"; #name space of associated Object Type, in this case it is Port
my $objectType = "VlanConfig";   # Object Type, please refer SDK for list of available object types 
my $indexParam ="name";  #This is the Index Paramater for VlanConfig, please refer SDK for the meaning of Index Param
my $indeParamValue ="tvlan";   # This is the Index Parameter Value
my $vlanNamePrefix = "tvlan";

my $tagParam = "tagValue"; # Parameter Name to be set, Please check SDK for PortConfig parameters
my $tagParamValue = "220"; # Parameter Value, please check SDK for Parameter value type

my $taggePortsParam = "vlanTaggedPorts"; # Parameter Name to be set, Please check SDK for PortConfig parameters
my $taggePortsParamValue = "1:1-1:4"; # Parameter Value, please check SDK for Parameter value type

my $vrParam = "vrName"; # Parameter Name to be set, Please check SDK for PortConfig parameters
my $vrParamValue = "VR-Default"; # Parameter Value, please check SDK for Parameter value type

my $vlanTag = 4095;
my $vlanId = 65536;

my $i = 0;
my $total = 4095;

$t = localtime( );
print $t . "\n";
my $t1 = time();

for($i = 0; $i < $total; $i++)
{

 $indeParamValue = $vlanNamePrefix."$vlanId";
 $tagParamValue = "$vlanTag";   	

 $vlanId = $vlanId - 1;
 $vlanTag = $vlanTag - 1;
 if($vlanTag == 0)
 {
    $vlanTag = 4095;	 
 }

 
 # assemble request
 my @params = (  SOAP::Data->name("filter" =>
                           \SOAP::Data->value(SOAP::Data->name("$indexParam" => $indeParamValue), 
                                              SOAP::Data->name("$vrParam" => $vrParamValue), 
                                              SOAP::Data->name("$tagParam" => $tagParamValue), 
                                              SOAP::Data->name("$taggePortsParam" => $taggePortsParamValue)))
                                      ->type($ns.":".$objectType),
                 SOAP::Header->name("hdr" =>
                           \SOAP::Data->value(SOAP::Data->name("sessionId" => $sessionId),
                            SOAP::Data->name("reqId" => "1")))

          );


 #print @params;

 # send request
 my $response = $connection->call($method => @params);

 # handle error
 if ($response->fault) { 
	print $response->faultcode, " ", $response->faultstring, "\n"; 
	#exit();
 }
 #print "Succesfully created\n";
 print ".";
}

# close the session
closesession($sessionId, $ARGV[0], $ARGV[1]);

print "\n";

$t = localtime( );
print $t . "\n";

my $t2 = time();

my $diff = $t2 - $t1;
my $mDiff = int($diff / 60);
my $sDiff = sprintf("%02d", $diff - 60 * $mDiff);

print "Total Time taken for creating $total Vlans with each has ports  $taggePortsParamValue :  $mDiff\:$sDiff\n";


