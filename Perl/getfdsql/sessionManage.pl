sub opensession {
    # usage: opensession(switch, username, password)
    # return value, session id if successful, null otherwise.
    my $host = shift();
    my $username = shift();
    my $passwd = shift();

    # print "Debug: $host, $username, $passwd.\n";
    # form the request to initiate connection
    my $connection = SOAP::Lite
	-> proxy("http://$username\@$host/xmlservice", timeout => 15)
	-> ns("http://www.extremenetworks.com/XMLSchema/xos/common", "com") # namespace and prefix for operation
	-> autotype(0)
	-> envprefix('SOAP-ENV');

    my $method = SOAP::Data->name("com:openSessionRequest");
    my @params = (SOAP::Data->name("session" =>
				   (SOAP::Data->name("session"=>
						     \SOAP::Data->value(
							 SOAP::Data->name("username" => $username),
							 SOAP::Data->name("password" => $passwd),
							 SOAP::Data->name("sessionId" => ""),
							 SOAP::Data->name("timeout" => "30"),
							 SOAP::Data->name("appName" => "perlEx")
						     )
						     )
				    )
				   )
	);
    # now send the request
    $result = $connection->call($method => @params);
    # errorhandling:
    if ($result->fault) {
	print "Error: ",$result->faultcode, " ", $result->faultstring, "\n";
	return null;
    }
    # if successful, return the sessionId:
    $rethash = $result->valueof('//session/sessionId');
    return $rethash;
}

sub closesession{
    my $sessionId=shift();
    my $host = shift();
    my $username = shift();

    # debug
    # print "Closing session id $sessionId...\n";
    # set up connection                                                                                                         
    my $connection = SOAP::Lite
        -> proxy("http://$username\@$host/xmlservice", timeout=>10)
        -> ns("http://www.extremenetworks.com/XMLSchema/xos/common", "com")
        -> autotype(0)
        -> envprefix('SOAP-ENV'); 
    my $method = SOAP::Data->name("com:closeSessionRequest");
    my @params = (SOAP::Data->name("sessionId" =>$sessionId));

    # send request
    $result = $connection->call($method =>@params);

    # handle error
    if ($result->fault) {
	print $result->faultcode, " ", $result->faultstring, "\n";
    }

}

# crucial that the required file returns true:
1;