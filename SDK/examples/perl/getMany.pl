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
##  This is an example to demonstarte XML API Paging Support
##  
##  It will read  switch ip, username and password from the command line
##  and will give back the Next available objects provided Size and Index Parameter Value, if index is not passed first 'n' number of objects returned.
##
##  Example: "perl get64K.pl 10.0.0.1 admin password"
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
	-> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>1000)
	-> ns("http://www.extremenetworks.com/XMLSchema/xos/switch", "switch") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	


#Get Next API Parameters
#if you would like check more APIs, please change following values 
my $ns = "vlan"; #name space of associated Object Type, in this case it is Port
my $objectType = "VlanConfig";   # Object Type, please refer SDK for list of available object types 
my $indexParam ="name";  #This is the Index Paramater for PortConfig, please refer SDK for the menaing of Index Param; 
                             #If the index attribute is not set, first $nextSize will be returned provided $actionType="next"
my $indexParamValue ="";   # This is the Index Parameter Value
my $actionType = "next";  # Only action supported is "next"
my $nextSize = "256";   # Number of objects to be retrieved, if this  value is not passed EXOS sets to 1 


my $i = 0;
my $pageCount = 16;

my $totalMins = 0;
my $totalSecs = 0;
my $totalCount = 0;
my $tSeconds = 0;

my $st = 0;

for($i = $st; $i < $pageCount; $i++)
{
   	
   my $method = SOAP::Data->name("switch:getRequest")->attr({"action" => $actionType, "maxSize" => $nextSize});
   my @params = ();
   if($i == 10000)
   {
     # assemble request
      @params = (  SOAP::Data->name("filter" => "")->type($ns.":".$objectType),
                SOAP::Header->name("hdr" =>
                                 \SOAP::Data->value(SOAP::Data->name("sessionId" => $sessionId),
                                 SOAP::Data->name("reqId" => "1")))

          );

   } else
   {
     # assemble request
     @params = (  SOAP::Data->name("filter" =>
                               \SOAP::Data->value(SOAP::Data->name("$indexParam" => $indexParamValue),
                                SOAP::Data->name("adminState" => ""),
                                SOAP::Data->name("tagValue" => ""),
                                SOAP::Data->name("vrName" => ""),
                                SOAP::Data->name("vlanTaggedPorts" => ""),
                                SOAP::Data->name("vlanUnTaggedPorts" => "")))->type($ns.":".$objectType),
                SOAP::Header->name("hdr" =>
                               \SOAP::Data->value(SOAP::Data->name("sessionId" => $sessionId),
                                SOAP::Data->name("reqId" => "1")))

          );
   }	

   $t = localtime( );
   my $t1 = time();

   # send request
   my $response = $connection->call($method => @params);

   my $t2 = time();

   $t = localtime( );

   # handle error
   if ($response->fault) { 
        print "Got an error:\n";
	print $response->faultcode, " ", $response->faultstring, "\n"; 
	exit();
   }
   my $diff = $t2 - $t1;
   my $mDiff = int($diff / 60);
   my $sDiff = sprintf("%02d", $diff - 60 * $mDiff);

   $tSeconds = $tSeconds +  $diff;

   my $startId = $i* 256;
   my $endId = ($i + 1) * 256 - 1;
   
   print "XMLGetNext API VlanConfig -  $startId to $endId:   $mDiff:$sDiff\n\n";
   
   # get values from response and dump on the screen
   my @vlanInfo =  $response->valueof('//objects/object');;
   my $len = @vlanInfo;

   $totalCount = $totalCount + $len;

   my $vlanParamValues = $vlanInfo[$len - 1];	
   $indexParamValue = $vlanParamValues ->{"name"};

# Dump out the returned values
   print Dumper(@vlanInfo);
}

# close the session
closesession($sessionId, $ARGV[0], $ARGV[1]);

my $mDiff = int($tSeconds/60);
my $sDiff = sprintf("%02d", $tSeconds - 60 * $mDiff);

print "---------------------------------------------------------------------------\n";
print "Total time taken for XMLAPI VlanConfig GET (with page size 256) of $totalCount Vlans:   $mDiff:$sDiff seconds\n"; 



