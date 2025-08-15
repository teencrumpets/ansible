#!//usr/bin/python3

import requests
import json
import os
import yaml
import argparse
from getpass import getpass

def snowRequest(user, pwd, url, hostname):
    hostname = hostname.upper()
    # Hardware query
    uriTable = 'api/now/table/cmdb_ci_hardware'
    uriQuery = f"?sysparm_query=install_status%3D1^name%3D{hostname}"
    uriFields = '&sysparm_fields=name%2Csys_id'
    uriOptions = '&sysparm_display_value=true&sysparm_limit=1000'
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    hwURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    qryHW = requests.get(hwURI, auth=(user, pwd), headers=headers, verify=False)

    if qryHW.status_code != 200: 
        print('Hardware query failed')
        print('Status:', qryHW.status_code, 'Headers:', qryHW.headers, 'Error Response:',qryHW.json())
        exit(1)

    jsonHW = (qryHW.json())["result"]
    length = len(jsonHW)

    if length == 1:
        return True

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--user", help="SNOW user account name", required=True)
    parser.add_argument("-p", "--password", help="Password for SNOW user account", required=True)
    parser.add_argument("-n", "--hostname", help="Server hostname", required=True)
    parser.add_argument("-l", "--link", help="Specify which SNOW environment URL to target", required=True)
    args = parser.parse_args()

    user = args.user 
    pwd = args.password
    hostname = args.hostname
    url = args.link

    output = snowRequest(user, pwd, url, hostname)

    if output:
        print(output)

if __name__ == '__main__':
    main()