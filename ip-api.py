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
            json_data = requests.get(main_api + x).json()
            # Checks to see if there is a 'message' field in the json data and
            # prints the message instead of doing a query
            if 'message' in json_data:
                print('\nThe IP "{}" is {}'.format(x, json_data['message']))
            # Print out wanted JSON data formatted nicely
            else:
                print('\nCity\State: {}, {}\n'
                      'Country:    {}\n'
                      'ISP:        {}\n'
                      'IP:         {}\n'
                      'MX:         {}'.format(
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
    split = []
    MXServer = []

    # append terminal output to variable std_out
    for line in p:
        if re.search('not found', line):
            query_api([host])
            break
        # Checs to see if 'domain name pointer' is in the line and finds the ip
        # associated with the pointer to do a query on. Created for IPs that do
        # not have a easily parsed MX record return.
        elif re.search('domain name pointer', line):
            query_api([host])
            extra = re.search('.in-addr.arpa .*', str(line))
            thing = line.replace(extra.group(0), '')
            query_api([thing.rstrip()])
            break
        std_out.append(line)
    p.close

    # create iterator
    i = 0
    # split line into dict and return MX servers
    for x in std_out:
        split = std_out[i].split()
        MXServer.append(split[-1])
        i = i + 1
    query_api(MXServer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname to lookip")
    args = parser.parse_args()
    findMX(args.host)
