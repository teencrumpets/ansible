#!//usr/bin/python3

import requests
import json
import os
import yaml
import argparse
from getpass import getpass
import re
import ast

def getUsers(user, pwd, url, default_accounts, service_accounts, server_hostname):
    log = []
    # User Address query
    uriTable = 'api/now/table/u_user_server_map'
    uriQuery = '?sysparm_query=u_hostnameISNOTEMPTY^u_nameISNOTEMPTY'
    uriFields = '&sysparm_fields=u_hostname%2Cu_name'
    uriOptions = '&sysparm_limit=1000'
    userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    qryUserMan = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

    if qryUserMan.status_code != 200: 
        log.append(f'Unable to query user server map table, Status: {qryUserMan.status_code}, Headers: {qryUserMan.headers}, Error Response: {qryUserMan.json()}')
        exit(1)

    jsonUserMan = (qryUserMan.json())["result"]

    firstLoop = True
    for x in jsonUserMan:
        edited = False

        hostSysID = x['u_hostname']['value']
        
        uriTable = 'api/now/table/cmdb_ci_server'
        uriQuery = f'?sysparm_query=sys_id%3D{hostSysID}'
        uriFields = '&sysparm_fields=name'
        uriOptions = '&sysparm_limit=1000'
        userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

        qryServer = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)
        jsonServer = (qryServer.json())["result"]
        
        hostname =jsonServer[0]["name"]

        userSysID = x['u_name']['value']

        uriTable = 'api/now/table/u_user_server_profiles'
        uriQuery = f'?sysparm_query=sys_id%3D{userSysID}'
        uriFields = '&sysparm_fields=u_uid%2Cu_gid%2Cu_username%2Cu_public_ssh_key%2Cu_name,%2Cu_password_hash'
        uriOptions = '&sysparm_limit=1000'
        userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

        qryLinuxUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)
        jsonLinuxUser = (qryLinuxUser.json())["result"]

        userSysID = jsonLinuxUser[0]['u_name']['value'] 

        uriTable = 'api/now/table/sys_user'
        uriQuery = f'?sysparm_query=sys_id%3D{userSysID}'
        uriFields = '&sysparm_fields=active'
        uriOptions = '&sysparm_limit=1000'
        userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

        qryUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)
        jsonUser = (qryUser.json())["result"]

        activeAccount = jsonUser[0]['active']

        if activeAccount == "false":
            continue

        username = jsonLinuxUser[0]["u_username"]
        uid = jsonLinuxUser[0]["u_uid"]
        gid = jsonLinuxUser[0]["u_gid"]
        sshKey = jsonLinuxUser[0]["u_public_ssh_key"]
        paswd_hash = jsonLinuxUser[0]["u_password_hash"]

        if firstLoop:
            firstLoop = False
            userData = {"users": []}
            userData["users"].append({"username": username, "uid": uid, "gid": gid, "ssh": sshKey, "password_hash": paswd_hash, "hosts": [hostname]})
            continue

        for i in userData["users"]:
            if username == i["username"]:
                if i["hosts"] != hostname:
                    i["hosts"].append(hostname)
                    edited = True
                    break

        if not edited: 
            userData["users"].append({"username": username, "uid": uid, "gid": gid, "ssh": sshKey, "password_hash": paswd_hash, "hosts": [hostname]})

    for x in default_accounts:
        username = x["username"]
        uid = x["uid"]
        gid = x["gid"]
        sshKey = x["ssh"]
        paswd_hash = x["password_hash"]
        hostname = "all"

        userData["users"].append({"username": username, "uid": uid, "gid": gid, "ssh": sshKey, "password_hash": paswd_hash, "hosts": hostname})

    if service_accounts:
        for x in service_accounts:
            username = x["username"]
            uid = x["uid"]
            gid = x["gid"]
            sshKey = x["ssh"]
            paswd_hash = x["password_hash"]

            userData["users"].append({"username": username, "uid": uid, "gid": gid, "ssh": sshKey, "password_hash": paswd_hash, "hosts": server_hostname})
    return userData


def addNewUser(user, pwd, url, sshKey, hashed_pwd, email):
    log = []
    #Looking up users sysID
    uriTable = 'api/now/table/sys_user'
    uriQuery = f'?sysparm_query=email%3D{email}'
    uriFields = '&sysparm_fields=sys_id'
    uriOptions = '&sysparm_limit=1000'
    userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    qryUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

    if qryUser.status_code != 200: 
        log.append(f'Unable to get users sysID, Status: {qryUser.status_code}, Headers: {qryUser.headers}, Error Response: {qryUser.json()}')
        exit(1)

    jsonUser = (qryUser.json())["result"]
    userSysID = jsonUser[0]['sys_id']
    
    #Checking if user already has user server profile
    uriTable = 'api/now/table/u_user_server_profiles'
    uriQuery = f'?sysparm_query=u_name%3D{userSysID}'
    uriFields = '&sysparm_fields=sys_id'
    uriOptions = '&sysparm_limit=1000'
    userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    qryLinuxUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

    if qryLinuxUser.status_code != 200: 
        log.append(f'Unable to find if user already exists on user server profile table, Status: {qryLinuxUser.status_code}, Headers: {qryLinuxUser.headers}, Error Response: {qryLinuxUser.json()}')
        exit(1)

    jsonLinuxUser = (qryLinuxUser.json())["result"]
    #Linux user that needs to be added to server
    if(jsonLinuxUser):
        log.append("Linux account exists for user")
    #New Linux user
    else:
        uriTable = 'api/now/table/u_user_server_profiles'
        uriQuery = '?sysparm_query=ORDERBYdescu_uid'
        uriFields = '&sysparm_fields=u_uid'
        uriOptions = '&sysparm_limit=1000'
        userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

        qryLinuxUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

        if qryLinuxUser.status_code != 200: 
            log.append(f'Unable to get available uid, Status: {qryLinuxUser.status_code}, Headers: {qryLinuxUser.headers}, Error Response: {qryLinuxUser.json()}')
            exit(1)

        jsonUID = (qryLinuxUser.json())["result"]

        if(jsonUID):
            jsonUID = sorted(jsonUID, key=lambda x: x['u_uid'], reverse=True)

            uid = int(jsonUID[0]['u_uid'])
            uid += 1
            gid = uid
        else:
            uid = 10000
            gid = uid

        uriTable = 'api/now/table/sys_user'
        uriQuery = f'?sysparm_query=email%3D{email}'
        uriFields = '&sysparm_fields=sys_id%2Cfirst_name%2Clast_name'
        uriOptions = '&sysparm_limit=1'
        userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

        qryLinuxUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

        if qryLinuxUser.status_code != 200: 
            log.append(f'unable to get users name, Status: {qryLinuxUser.status_code}, Headers: {qryLinuxUser.headers}, Error Response: {qryLinuxUser.json()}')
            exit(1)

        jsonSysID = (qryLinuxUser.json())["result"]

        userSysID = jsonSysID[0]['sys_id']
        firstName = jsonSysID[0]['first_name']
        lastName = jsonSysID[0]['last_name']
        
        #Filter spaces and special charcters
        firstName = firstName.split(' ')[0]
        lastName = lastName.split(' ')
        if (len(lastName) > 1):
            lastName = lastName[len(lastName)-1]
        else:
            lastName = lastName[0]
        firstName = re.sub(r'[^\w\s]', '', firstName)
        lastName = re.sub(r'[^\w\s]', '', lastName)
        

        uName = str.lower(firstName[0]+lastName)

        #add information about user to linux user management table
        uriTable = 'api/now/table/u_user_server_profiles'
        userURI = f"{url}{uriTable}"

        info = {"u_name": userSysID, "u_username": uName, "u_uid": uid, "u_gid": gid, "u_password_hash": hashed_pwd, "u_public_ssh_key": sshKey}
        info = json.dumps(info)
        response = requests.post(userURI, auth=(user, pwd), headers=headers ,data=info, verify=False)

        if log:
            return log
        else:
            return "Success"


def changePassword(user, pwd, url, linux_user, hashed_pwd):
    log = []
    uriTable = 'api/now/table/u_user_server_profiles'
    uriQuery = f'?sysparm_query=u_username%3D{linux_user}'
    uriFields = '&sysparm_fields=sys_id'
    uriOptions = '&sysparm_limit=1000'
    userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    qryUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

    if qryUser.status_code != 200: 
        log.append(f'User Address query failed, Status: {qryUser.status_code}, Headers: {qryUser.headers}, Error Response: {qryUser.json()}')
        exit(1)

    jsonUser = (qryUser.json())["result"]
    userSysID = jsonUser[0]['sys_id']

    uriTable = 'api/now/table/u_user_server_profiles/'
    userURI = f"{url}{uriTable}{userSysID}"

    info = {'u_password_hash': hashed_pwd}
    info = json.dumps(info)
    response = requests.patch(userURI, auth=(user, pwd), headers=headers ,data=info, verify=False)
    
    if log:
        return log
    else:
        return "Success"


def changeSSHKey(user, pwd, url, sshKey, linux_user):
    log = []

    uriTable = 'api/now/table/u_user_server_profiles'
    uriQuery = f'?sysparm_query=u_username%3D{linux_user}'
    uriFields = '&sysparm_fields=sys_id'
    uriOptions = '&sysparm_limit=1000'
    userURI = f"{url}{uriTable}{uriQuery}{uriFields}{uriOptions}"

    headers = {"Content-Type":"application/json","Accept":"application/json"}

    qryUser = requests.get(userURI, auth=(user, pwd), headers=headers, verify=False)

    if qryUser.status_code != 200: 
        log.append(f'Unable to get sysID for user, Status: {qryUser.status_code}, Headers: {qryUser.headers}, Error Response: {qryUser.json()}')
        exit(1)

    jsonUser = (qryUser.json())["result"]
    userSysID = jsonUser[0]['sys_id']

    uriTable = 'api/now/table/u_user_server_profiles/'
    userURI = f"{url}{uriTable}{userSysID}"

    info = {'u_public_ssh_key': sshKey}
    info = json.dumps(info)
    response = requests.patch(userURI, auth=(user, pwd), headers=headers ,data=info, verify=False)

    if response.status_code != 200: 
        log.append(f'Unable to change SSH key, Status: {response.status_code}, Headers: {response.headers}, Error Response: {response.json()}')
        exit(1)

    if log:
        return log
    else:
        return "Success"


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--user", help="SNOW user account name", required=True)
    parser.add_argument("-p", "--password", help="Password for SNOW user account", required=True)
    parser.add_argument("-t", "--ansible_tag", help="Ansible Playbook tag", required=True)
    parser.add_argument("-d", "--default_accounts", help="All default accounts on the server")
    parser.add_argument("-a", "--service_accounts", help="Service accounts on the server")
    parser.add_argument("-n", "--hostname", help="hostname on the server")
    parser.add_argument("-s", "--key", help="Public SSH Key")
    parser.add_argument("-l", "--server_username", help="Server username")
    parser.add_argument("-o", "--hashed_password", help="Hashed Password")
    parser.add_argument("-e", "--email", help="Users email")
    parser.add_argument("-w", "--snow_url", help="Snow url", default="http://6.2.10.5:16002/")
    args = parser.parse_args()

    user = args.user
    pwd = args.password
    sshKey = args.key
    server_hostname = args.hostname
    hashed_pwd = args.hashed_password
    tag = args.ansible_tag
    userEmail = args.email
    username = args.server_username

    if args.snow_url:
        url = args.snow_url

    #default accounts is originally seen as a string when passed to script, ast.literal_eval ensures it's seen as a list
    if args.default_accounts:
        default_accounts_string = args.default_accounts
        default_accounts = ast.literal_eval(default_accounts_string)

    if args.service_accounts:
        service_accounts_string = args.service_accounts
        service_accounts = ast.literal_eval(service_accounts_string)
    else:
        service_accounts = ""

    if tag == 'update' and hashed_pwd:
        response = changePassword(user, pwd, url, username, hashed_pwd)

    if tag == 'update' and sshKey:
        response = changeSSHKey(user, pwd, url, sshKey, username)

    if tag == 'newUser':
        response = addNewUser(user, pwd, url, sshKey, hashed_pwd, userEmail)

    if tag == 'manage':
        response = getUsers(user, pwd, url, default_accounts, service_accounts, server_hostname)
        print(response)
        jsonPath = "/home/ypgansible/users.json"
        with open(jsonPath, 'w') as fUsers:
            json.dump(response, fUsers)
            print(f"Json file saved to {jsonPath}")

if __name__ == '__main__':
    main()