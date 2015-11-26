# mlag_config_check.py
# This script will check a switch's MLAG config to ensure that there is only one port in the ISC
# vlan, and that all vlans added to MLAG port exist on the ISC port as well. This does not ensure
# that the tagging on vlans matches across MLAG peers.
# 
# Last updated: June 29, 2015

def main():
	# Find which vlan is the ISC vlan
	cli_output = exsh.clicmd('show mlag peer', True).split()
	isc_vlan = cli_output[10]

	# Check the number of ports added to the ISC vlan, and get the port number of the ISC link
	cli_output = exsh.clicmd('show vlan ' + isc_vlan, True).split()

	index = cli_output.index('Ports:')
	index = index + 1 # +1, since we found the item before the number of ports

	num_ports = cli_output[index]

	# Remove the trailing period from that output

	if num_ports.endswith('.'):
		num_ports = int(num_ports[:-1])

	#Check the number of ports added to the ISC vlan

	if num_ports > 1:
		print 'Multiple ports are added to the ISC vlan (' + isc_vlan + '). Please correct.'
		return
	elif num_ports == 0:
		print 'No ports are added to the ISC vlan (' + isc_vlan + '). Please correct.'
		return

	# At this point, we can assume that there is one port added to the ISC vlan,
	# and continue checking the MLAG configuration.

	# Determine what the port number of the ISC is

	if 'Tag:' in cli_output:
		index = cli_output.index('Tag:')
		index = index + 1
		isc_port = cli_output[index]
	elif 'Untag:' in cli_output:
		index = cli_output.index('Untag:')
		index = index + 1
		isc_port = cli_output[index]
	else:
		print 'Error: An error occurred. Unable to determine ISC port'
		return

	# Remove the flags around the port number

	if isc_port.endswith('g'):
		isc_port = isc_port[:-1]
	elif isc_port.endswith('G'):
		print "The ISC port is also configured as an MLAG port. Please correct."
		return

	if isc_port.startswith('*'):
		isc_port = isc_port[1:]
	elif isc_port.startswith('!'):
		isc_port = isc_port[1:]
		print 'The ISC port (' + isc_port + ') is disabled. Please correct.'

	# Create a list of the vlans that exist on the ISC port

	cli_output = exsh.clicmd('show port ' + isc_port + ' info detail', True).split()

	vlan_on_next_iteration = False

	isc_port_vlans = list()

	for i in cli_output:
		
		if vlan_on_next_iteration:
			#remove a trailing comma, if present
			if i.endswith(','):
				vlan = i[:-1]
			else:
				vlan = i
			isc_port_vlans.append(vlan)

			


		if i == 'Name:':
			vlan_on_next_iteration = True
		else :
			vlan_on_next_iteration = False

	# Now, isc_port_vlans contains all the vlans on the ISC port.
	# Now we can iterate through MLAG ports, and check if the vlans on them are
	# on the ISC port. If not, an error will be written to the CLI.

	cli_output = exsh.clicmd('show config vsm', True)

	lines = cli_output.split('\n')

	#remove an empty string that breaks the for loop below

	lines = lines[:-1]

	#create an empty list to be used in the loop

	mlag_ports = list()

	for l in lines:
		line = l.split()
		if line[0] == 'enable':
			mlag_ports.append(line[3])


	for p in mlag_ports:


		cli_output = exsh.clicmd('show port ' + p + ' info detail', True).split()

		vlan_on_next_iteration = False

		port_vlans = list()

		for i in cli_output:
			
			if vlan_on_next_iteration:
				#remove a trailing comma, if present
				if i.endswith(','):
					vlan = i[:-1]
				else:
					vlan = i
				if vlan not in isc_port_vlans:
					print 'Vlan ' + vlan + ' is not added to the ISC port (' + isc_port + '), and is found on MLAG port ' + p + '. Please correct.'

			if i == 'Name:':
				vlan_on_next_iteration = True
			else :
				vlan_on_next_iteration = False

    ## Check local and remote checksums to determine if FDB and VLANs match
    
    checksums = exsh.clicmd('debug fdb show globals | include LclCkhsum:', True).split()
    
    local = checksums[2]
    remote = checksums[3]
    
    if local is remote:
        print 'Local and remote FDB checksums match.'
    else:
        print 'Local and remote FDB checksums do not match. Please check config on the other MLAG peer.'
        print exsh.clicmd('debug fdb show globals', True)
    
    

	print 'MLAG config check completed.'

main()
