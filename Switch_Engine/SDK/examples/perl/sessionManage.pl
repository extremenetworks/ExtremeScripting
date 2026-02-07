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
##  These are subroutines used to open and close a session.
### 
######

sub opensession {

    my $host = shift();
    my $username = shift();
    my $passwd = shift();

    my $connection = SOAP::Lite
	-> proxy("http://$username\@$host/xmlservice", timeout => 15)
	-> ns("http://www.extremenetworks.com/XMLSchema/xos/common", "com")
	-> autotype(0)
	-> envprefix('SOAP-ENV');

    my $method = SOAP::Data->name("com:openSessionRequest");
    my @params = (SOAP::Data->name("session" =>
				   (SOAP::Data->name("session"=>
						     \SOAP::Data->value(
							 SOAP::Data->name("username" => $username),
							 SOAP::Data->name("password" => $passwd),
							 SOAP::Data->name("sessionId" => ""),
							 SOAP::Data->name("timeout" => "1500"),
							 SOAP::Data->name("appName" => "perlEx")
                                                                       )
						     )
				    )
				    )
	         );
    $result = $connection->call($method => @params);
    if ($result->fault) {
       print "Error: ",$result->faultcode, " ", $result->faultstring, "\n";
       return;
    }

    $rethash = $result->valueof('//session/sessionId');
    return $rethash;
}

sub closesession {

    my $sessionId=shift();
    my $host = shift();
    my $username = shift();

    my $connection = SOAP::Lite
        -> proxy("http://$username\@$host/xmlservice", timeout=>10)
        -> ns("http://www.extremenetworks.com/XMLSchema/xos/common", "com")
        -> autotype(0)
        -> envprefix('SOAP-ENV'); 
    my $method = SOAP::Data->name("com:closeSessionRequest");
    my @params = (SOAP::Data->name("sessionId" =>$sessionId));

    $result = $connection->call($method =>@params);

    if ($result->fault) {
	print $result->faultcode, " ", $result->faultstring, "\n";
    }

}


1;
