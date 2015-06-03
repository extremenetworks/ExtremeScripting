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
##	Usage: "perl getAllFdb.pl <ip_address> <account> <password>
##  Example: "perl getAllFdb.pl 10.0.0.1 admin password"
##
##  Mysql Table Schema: CREATE TABLE fdb(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, \
##  datetime TIMESTAMP DEFAULT NOW(), macaddress VARCHAR(32), vlan VARCHAR(32), port \
##  VARCHAR(6), age VARCHAR(10));
##  
##  Copyright (c) Extreme Networks Inc.  2006,2007
##  All rights reserved 
##  
### 
######
###
##	Contributors:
##
##	Thorsten Krohn 	- Wilhelm Tel, Germany
##	Andy Gatward 	- Reading University, United Kingdom
##	Paul Tinsley	- Lightining Source, United States
##	Jussi Sjöström  - Xenetic, Finland
##
###
######
use SOAP::Lite; 
use DBI;
use DBD::mysql;
require ('sessionManage.pl');

# MySQL CONFIG VARIABLES
$platform = "mysql";
$database = "fdb";
$host = "localhost";
$port = "3306";
$tablename = "fdbtable";
$user = "fdb";
$pw = "fdb121212";


# Session Config Variables
my $host=$ARGV[0];
my $usrname=$ARGV[1];
my $pwd=$ARGV[2];

#DATA SOURCE NAME
$dsn = "dbi:mysql:$database:localhost:3306";

# PERL DBI CONNECT
$connect = DBI->connect($dsn, $user, $pw) or die "Unable to connect: $DBI::errstr\n";

# PERL SOAPLite Connection
my $sessid=opensession($host,$usrname,$pwd);

if ($sessid==null) {
    die "Could not open connection to switch.\n";
} else {
    print "Connection to switch opened, sessionid $sessid.\n";

# set up connection
my $connection = SOAP::Lite
        -> proxy("http://$usrname:$pwd\@$host/xmlservice", timeout=>10)
	-> ns("urn:xapi/l2protocol/fdb", "xos") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV'); # envelope prefix
	
# assemble the SOAP Message
my $method = SOAP::Data->name('xos:getAllFdb');


# Assign the Result
	$result = $connection->call($method);
	handleResponse($result);


# send request
my $response = $connection->call($method => @params);
}


sub handleResponse {
	my $res = shift;
	if ($res->fault) { 
		print $res->faultcode, " ", $res->faultstring, "\n"; 
		exit();
	}else
	{
						my @fdbentry = $result->valueof('//Body/getAllFdbResponse/reply/fdb');
						my $len = @fdbentry;
						print $len."\n";
							my  $i=0;
    						for ($i=0; $i < $len; $i++) {
							my $fdbentry= $fdb[$i];
							my $macAdress=$fdb->{"macAddress"};
							my $vlan=$fdb->{"vlan"};
							my $port=$fdb->{"port"};
							my $age=$fdb->{"age"};
							
						}
						
						foreach my $test (@fdbentry){
							$mac = $test->{'macAddress'};
							$vlan = $test->{'vlan'};
							$port = $test->{'port'};
							$age = $test->{'age'};
							$query = "INSERT INTO fdb (id, datetime, macaddress, vlan, port, age) VALUES (DEFAULT, DEFAULT, \'$mac\', \'$vlan\', \'$port\', \'$age\')";
							$query_handle = $connect->prepare($query);
							$query_handle->execute();
					            
			          }
             }  
	}

closesession($sessid,$host,$usrname);
