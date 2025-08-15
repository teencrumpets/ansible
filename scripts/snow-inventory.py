#!//usr/bin/python3

import requests
import json
import os
import yaml
import argparse
from getpass import getpass

# Remove "Null" from YAML output
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

def snowRequest(user, pwd, url, env):

    uriTable = 'api/now/table/cmdb_ci_computer'
    grpSYS_ID = 'b55445b12df11300076d390d5abf2543'
    

    # Hardware query
    uriQuery = f"?sysparm_query=install_status%3D1^assignment_group%3D{grpSYS_ID}^environment%3D{env}"
    uriFields = '&sysparm_fields=name%2Cassignment_group%2Csys_id%2Cos_version'
    uriOptions = '&sysparm_display_value=true&sysparm_limit=1000'
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    hwURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    # IP Address query
    uriTable = 'api/now/table/cmdb_ci_ip_address'
    uriQuery = '?sysparm_query=install_status%3D1^u_hardware_ciISNOTEMPTY^u_primary%3Dtrue'
    uriFields = '&sysparm_fields=u_hardware_ci%2Cinstall_status%2Cip_address%2Cu_primary'
    uriOptions = '&sysparm_display_value=false&sysparm_limit=1000'
    ipURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    qryHW = requests.get(hwURI, auth=(user, pwd), headers=headers, verify=False)
    qryIP = requests.get(ipURI, auth=(user, pwd), headers=headers, verify=False)

    if qryHW.status_code != 200: 
        print('Hardware query failed')
        print('Status:', qryHW.status_code, 'Headers:', qryHW.headers, 'Error Response:',qryHW.json())
        exit(1)
    if qryIP.status_code != 200: 
        print('IP Address query failed')
        print('Status:', qryIP.status_code, 'Headers:', qryIP.headers, 'Error Response:',qryIP.json())
        exit(1)

    jsonHW = (qryHW.json())["result"]
    jsonIP = (qryIP.json())["result"]
    hwCount = len(jsonHW)
    ipCount = len(jsonIP)

    with open('./snow_groups.yml', 'r') as file:
        baselineData = yaml.safe_load(file)

    out = {"all": {"hosts": None, "children": {}}}

    for hwID in range(hwCount):
        for ipID in range(ipCount):
            if (jsonHW[hwID]["sys_id"] == jsonIP[ipID]["u_hardware_ci"]["value"]) and (jsonHW[hwID]["os_version"]):
                ip = jsonIP[ipID]["ip_address"]
                name = jsonHW[hwID]["name"]
                opSys = jsonHW[hwID]["os_version"]["display_value"]
                baseline = baselineData.get(f"{opSys}", "other")

                if baseline != "other":
                    if baseline not in out["all"]["children"]:
                        out["all"]["children"][baseline] = {"hosts": {}}
                    out["all"]["children"][baseline]["hosts"][name] = {"ansible_host": ip}

    return out

def writeYAML(ymlPath, env, response):
    invName = f"{env}-inventory.yml"

    if env == "Production":
        invName = "inventory.yml"
        
    ymlPath += invName
    with open(ymlPath, 'w') as fInventory:
        yaml.dump(response, fInventory, default_flow_style=False)
        print(f"Inventory file saved to {ymlPath}")

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--user", help="SNOW user account name")
    parser.add_argument("-p", "--password", help="Password for SNOW user account")
    parser.add_argument("-o", "--output", help="Directory to save inventory file to")
    parser.add_argument("-l", "--link", help="Specify which SNOW environment URL to target")
    args = parser.parse_args()

    yaml.add_representer(type(None), represent_none)
    scriptDir = os.getcwd()

    if args.user:
        user = args.user
    else:    
        user = input("Enter ServiceNow user name: ")

    if args.password:
        pwd = args.password
    else:
        pwd = getpass("Enter ServiceNow user password: ")

    if args.output:
        ymlPath = f"{args.output}/"
    else:
        ymlPath = f"{scriptDir}/../"

    if args.link:
        url = args.link
    else:
        url = 'http://6.2.10.5:16002/'

    env = "Production"
    response = snowRequest(user, pwd, url, env)
    writeYAML(ymlPath, env, response)

    env = "Lab"
    response = snowRequest(user, pwd, url, env)
    writeYAML(ymlPath, env, response)

    env = "Pre-Production"
    response = snowRequest(user, pwd, url, env)
    writeYAML(ymlPath, env, response)

if __name__ == '__main__':
    main()