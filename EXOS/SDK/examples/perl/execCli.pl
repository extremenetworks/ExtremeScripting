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
##  This is an example on how to use execCli XMLAPI.
##  execCli XML API is used to send the CLI Command through XML Interfaces and returns the CLI format
##
##  Example: "perl execCli.pl 10.0.0.1 userName password "cli-command" "timer-interval-in-seconds"
##  
##  
##  If perl is not installed on your Windows XP, use the link 
##  http://activestate.com/store/download.aspx?prdGUID=81fbce82-6bd5-49bc-a915-08d58c2648ca
##  Install Windows(x86) MSI package, installer sets your windows PATH; Go to DOS prompt and execute the script as mentioned. 
##  If password is empty, specify empty string in quotes i.e. " "
##  If the time-interval is not specified, executes only once. 
######

use SOAP::Lite; 
use Data::Dumper;
$Data::Dumper::Indent = 1;
$Data::Dumper::Terse=1;

die "Usage: [host] [username] [password] [command] [timer-interval-in-seconds]\n" 
	unless ($ARGV[0] && $ARGV[1]);

my $command="show accounts";  #this is the default command
my $frequency = 0;            #value of '0' inidcates only once, 
# handle empty password
defined($ARGV[2]) ? ($credentials = "$ARGV[1]:$ARGV[2]") : ($credentials = "$ARGV[1]:");
defined($ARGV[3]) ? ($command = $ARGV[3]):();
defined($ARGV[4]) ? ($frequency = $ARGV[4]):();

# set up connection
my $connection = SOAP::Lite
        -> proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10)
	-> ns("urn:xapi/cfgmgmt/cfgmgr", "xoscfg") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix


$connection->proxy("http://$credentials\@$ARGV[0]/xmlservice", timeout=>10);
$connection->uri("urn:xapi/cfgmgmt/cfgmgr", "xoscfg");


# assemble CLI Command
my @params = (	SOAP::Data->name("command" => $command));
			
# send execCli request
while(1){
  $result = $connection->call("xoscfg:execCli"=>@params);
  handleResponse($result);
  if($frequency == 0)
  {
    exit;
  }

  sleep($frequency);
}


sub handleResponse {
	my $res = shift;
	if ($res->fault) { 
		print $res->faultcode, " ", $res->faultstring, "\n"; 
		exit();
	}else
	{
           print Dumper($result->valueof('//reply/'));
	}
}
