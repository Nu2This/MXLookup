import argparse
import requests
import os
import re
import sys
import traceback


def query_api(host):
    """Queries the ip-api site in order to check geolocation and mx record of
    the host"""
    main_api = 'http://ip-api.com/json/'
    # For every host do an API request
    try:
        for x in host:
            # Store response in 'json_data'
            json_data = requests.get(main_api + x).json()
            # Checks to see if there is a 'message' field in the json data and
            # prints the message instead of printing our formatted data.
            # This is done because messages are always an error with this api.
            if 'message' in json_data:
                print('\nThe IP "{}" is {}'.format(x, json_data['message']))
            # Print out wanted JSON data formatted nicely
            else:
                print('\nAS:         {}\n'
                      'City\State: {}, {}\n'
                      'Country:    {}\n'
                      'ISP:        {}\n'
                      'IP:         {}\n'
                      'MX:         {}'.format(
                       json_data['as'],
                       json_data['city'],
                       json_data['regionName'],
                       json_data['country'],
                       json_data['isp'],
                       json_data['query'],
                       x))
    # Added exception handling of key errors to help identify problems when
    # reading the json data
    except KeyError:
        traceback.print_exc(file=sys.stdout)
        print('Key Error')
        print('JSON: ')
        print(json_data)


def findMX(host):
    """Looks up the MX record of a host"""
    p = os.popen('host -t MX ' + host)

    # initialize dicts
    std_out = []
    # Stores the standard output of p(above)
    split = []
    # Used to hold the a line in std_out that we want to split.
    MXServer = []
    # The server address that we are sending to the api. 

    # Append terminal output to list std_out
    for line in p:
        if re.search('not found', line):
            print('No MX record found querying ' + host)
            query_api([host])
            break
        # Check to see if 'domain name pointer' is in the line and finds the
        # ip associated with the pointer to do a query on. Created for IPs that
        # do not have a easily parsed MX record return.
        elif re.search('domain name pointer', line):
            print(line)
            print('Domain name pointer found querying original host: ' + host)
            query_api([host])
            extra = re.search('.in-addr.arpa .*', str(line))
            # This finds out the 'extra' stuff I dont really care about. i only
            # need the IP that is in the line before .in-addr.arpa
            thing = line.replace(extra.group(0), '')
            # This takes the line and replaces what is stored in the 'extra'
            # variable with nothing and gives us the 'thing' we want to query,
            # an IP address.
            print('\nDomain Name pointer Query: ' + thing)
            query_api([thing.rstrip()])
            break
        std_out.append(line)
    p.close

    # split line into dict and return MX servers
    for x in std_out:
        # When using os.popen it basically acts like a terminal allowing you to
        # run terminal commands from your Python script and use its output. We
        # are using as an example 'host -t MX google.com' the output would look
        # like:
        # google.com mail is handled by 30 alt2.aspmx.l.google.com
        # google.com mail is handled by 40 alt3.aspmx.l.google.com
        # google.com mail is handled by 10 aspmx.l.google.com
        # google.com mail is handled by 20 alt1.aspmx.l.google.com
        # google.com mail is handled by 50 alt4.aspmx.l.google.com
        split = std_out[x].split()
        # We use .split() method to split the std_out list entry by spaces

        MXServer.append(split[-1])
        # We take the last item in the split(aspmx.l.google.com) and append it
        # to the list 'MXServer'
    query_api(MXServer)
    # Now we send the list 'MXServer' to the query_api function


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname to lookip")
    args = parser.parse_args()
    findMX(args.host)
