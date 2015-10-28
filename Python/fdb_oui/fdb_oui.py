#!/usr/bin/env python
'''
This script scans the FDB table and reports devices connected based on known MAC OUI values
'''
ouiDesc = {
        '00:08:02' : 'Compaq',
        '00:0c:29' : 'VMWare',
        '00:0d:60' : 'IBM',
        '00:12:17' : 'Cisco-Linksys',
        '00:13:e8' : 'Intel',
        '00:15:c5' : 'Dell',
        '00:1e:c9' : 'Dell',
		'84:2b:2b' : 'Dell',
		'a4:ba:db' : 'Dell',
        '02:60:8c' : '3Com',
        '00:01:30' : 'Extreme Networks',
        '00:04:96' : 'Extreme Networks',
		'D8:84:66' : 'Extreme Networks',
		'00:01:F4' : 'Enterasys Networks',
		'00:11:88' : 'Enterasys Networks',
		'00:1F:45' : 'Enterasys Networks',
		'20:B3:99' : 'Enterasys Networks',
        '00:e0:34' : 'Cisco',
        '00:e0:52' : 'Foundry Networks',
        '00:1a:a0' : 'Dell',
        }
exsh.clicmd('disable clipaging', False)
cnt = 0
print ""
for line in exsh.clicmd('show fdb', True).splitlines():
    tokens = line.split()
    if len(tokens) == 0:
        continue
    if tokens[0][0].isdigit():
        oui = tokens[0].lower()[:8]
        if oui in ouiDesc:
            print ouiDesc[oui],'device with MAC address',tokens[0],'on port',tokens[-1]
        else:
            print 'Unknown device with MAC address',tokens[0], 'on port', tokens[-1]
        cnt += 1
print ""
if cnt == 0:
    print 'No FDB entries found\n'
	