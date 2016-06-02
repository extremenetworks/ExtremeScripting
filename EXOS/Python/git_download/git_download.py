import httplib


# This function Changes the VR
def vr_change(vrid):
    f = open("/proc/self/ns_id", "w")
    f.write(vrid)
    f.close()


# This function downloads github pages
def pagegit(URL_location):
    c = httplib.HTTPSConnection("raw.githubusercontent.com")
    c.request("GET", "{0}".format(URL_location))
    response = c.getresponse()
    # print response.status, response.reason
    return response.read()


# This function checkes to see if DNS is configured on the switch and downloads the main github page with the correct VR
def internet_check():
    main_page_data = 'False'
    url = '/extremenetworks/ExtremeScripting/master/EXOS/Python/README.md'
    dns = exsh.clicmd('show configuration "nettools" | include "configure dns-client add name-server"', True)
    if 'VR-Default' in dns:
        try:
            vr_change('2')
            main_page_data = pagegit(url)
            print ("\nInternet Connection found on VR-Default")
        except:
            main_page_data = 'False'

    if 'VR-Mgmt' in dns and main_page_data == 'False':
        try:
            vr_change('0')
            main_page_data = pagegit(url)
            print ("\nInternet Connection found on VR-Mgmt")
        except:
            main_page_data = 'False'
    return main_page_data


def main():

    # Checks for internet access and downloads/organizes the script table into a list of dictionaries
    main_page_data = internet_check().split('\n')
    if main_page_data[0] != 'False':
        github = []
        for line in main_page_data:
            if '|[' in line:
                line = line.split('|')
                path = line[1].split('(')
                name = path[0][1:-1]
                detail = line[2].split('(')
                github.append({'name': name, 'path': path[1][:-1], 'Description': detail[0]})

        # This part prints the scripts names and descriptions collected so you can select the script to download
        n = 0
        print ('Script:{0}Description:'.format(' '*29))
        print ('-'*48)
        for line in github:
            n += 1
            if n >= 10:
                print ('{0}: {1} {2} {3}'.format(n, line['name'], (' ' * (31 - len(line['name']))),  line['Description']))
            else:
                print (' {0}: {1} {2} {3}'.format(n, line['name'], (' ' * (31 - len(line['name']))),  line['Description']))

        # Collects user input and formats input for downloading the script readme file to get .py file name
        input = raw_input("What script would you like to download? ")
        try:
            input = int(input)
        except:
            pass

        if input != '' and 1 <= input <= len(github):
            userinput = int(input) - 1

            # This uses the user input[index] to go to the script page to get the .py file name.
            url = "/extremenetworks/ExtremeScripting/master/EXOS/Python/{0}/README.md".format(github[userinput]['path'])
            script_page_data = pagegit(url)
            script_page_data = script_page_data.split('\n')
            for line in script_page_data:
                if '.py)' in line and '.py]' in line:
                    line = line.split('(')
                    script_name = line[1][:-1]

                    # Uses the script name found above to download the .py file to a variable.
                    script_url = "/extremenetworks/ExtremeScripting/master/EXOS/Python/{0}/{1}".format(github[userinput]['path'], script_name)
                    source = pagegit(script_url)

                    # Writes the variable data to the switch with the script name
                    f = open( "/usr/local/cfg/{0}".format(script_name), 'w')
                    f.write(source)
                    f.close()
                    print ("\nBy downloading this file you agree to the License")
                    print ("Terms in the readme, available at the URL below.\n")
                    print ("https://github.com/extremenetworks/ExtremeScripting/blob/master/EXOS/Python/{0}/README.md\n".format(github[userinput]['path']))
                    print ("{0} was downloaded to /usr/local/cfg/.\n".format(script_name))
        else:
            print ("Wrong input please select valid number.")
    else:
        print ("DNS is misconfigured or no internet access was found on VR-Default or VR-Mgmt\n")
        print ("Configure DNS with the command 'configure dns-client add name-server <DNS IP> vr <vr name>'")

    # Revert back to normal VR namespace
    vr_change('0')

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        # catch SystemExit to prevent EXOS shell from exiting to the login prompt
        vr_change('0')