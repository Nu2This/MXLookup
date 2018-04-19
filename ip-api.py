import argparse
import requests
import os
import re


def query_api(host):
    main_api = 'http://ip-api.com/json/'
    # For every host do an API request
    for x in host:
        json_data = requests.get(main_api + x).json()
        # Print out wanted JSON data formatted nicely
        print('\nCity\State: {}, {}\n'
              'Country:   {}\n'
              'ISP:       {}\n'
              'IP:        {}\n'
              'MX:        {}'.format(
               json_data['city'],
               json_data['regionName'],
               json_data['country'],
               json_data['isp'],
               json_data['query'],
               x))


def findMX(host):
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
