import sys
import exsh

do_list = [
    'create vlan 10-20',
    'config vlan 10-20 add ports all tagged',
        ]

show_list = [
    'show vid',
    'show ports',
    'show ports vid',
    'show ports info',
    'show ports config no',
    'show ports statistics no',
    ]

# just print any command line args to show they showed up
print sys.argv

# stuff to do
for cmd in do_list:
    print '\n',cmd
    exsh.clicmd(cmd)

# stuff to show
for cmd in show_list:
    print '\n',cmd
    print exsh.clicmd(cmd,capture=True)
