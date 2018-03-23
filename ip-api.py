import argparse
import json
import requests
import os

def search(host):
    main_api = 'http://ip-api.com/json/'

    ip = findMX(host)
    for host in ip:
        json_data = requests.get(main_api + host).json()

        print('\nCity\State: {}, {}\n Country:   {}\n ISP:       {}\n IP:        {}\n MX:        {}'.format(
            json_data['city'],
            json_data['regionName'],
            json_data['country'],
            json_data['isp'],
            json_data['query'],
            host))

def findMX(host):
    p = os.popen('host -t MX ' + host)

    #initialize dicts
    std_out = []
    split = []
    MXServer = []

    #append terminal output to variable std_out
    for line in p:
        std_out.append(line)
    p.close

    #create iterator
    i = 0
    #split line into dict and return MX servers
    for x in std_out:
        split = std_out[i].split()
        MXServer.append(split[6])
        i = i + 1
    return MXServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname to lookip")
    args = parser.parse_args()

    search(args.host)
