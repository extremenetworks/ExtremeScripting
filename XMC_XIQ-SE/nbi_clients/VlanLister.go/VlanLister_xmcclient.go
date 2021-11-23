package main

/*
#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######
*/

import (
	xmcnbiclient "gitlab.com/rbrt-weiler/go-module-xmcnbiclient"
)

/*
######## ##     ## ##    ##  ######   ######
##       ##     ## ###   ## ##    ## ##    ##
##       ##     ## ####  ## ##       ##
######   ##     ## ## ## ## ##        ######
##       ##     ## ##  #### ##             ##
##       ##     ## ##   ### ##    ## ##    ##
##        #######  ##    ##  ######   ######
*/

// Initializes the actual XMC client
func initializeClient() {
	client = xmcnbiclient.New(config.XMCHost)
	client.SetUserAgent(toolID)
	client.UseHTTPS()
	if config.NoHTTPS {
		client.UseHTTP()
	}
	client.UseOAuth(config.XMCUserID, config.XMCSecret)
	if config.BasicAuth {
		client.UseBasicAuth(config.XMCUserID, config.XMCSecret)
	}
	client.UseSecureHTTPS()
	if config.InsecureHTTPS {
		client.UseInsecureHTTPS()
	}
	timeoutErr := client.SetTimeout(config.HTTPTimeout)
	if timeoutErr != nil {
		stdErr.Fatalf("Could not set HTTP timeout: %s\n", timeoutErr)
	}
}

// Refreshes the OAuth token if it is to expire soon
func proactiveTokenRefresh() {
	if client.Authentication.Type == xmcnbiclient.AuthTypeOAuth {
		if client.AccessToken.ExpiresSoon(config.HTTPTimeout + 1) {
			go client.RetrieveOAuthToken()
		}
	}
}
