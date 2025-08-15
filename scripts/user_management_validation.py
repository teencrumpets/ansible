#!//usr/bin/python3

import logging
import requests
import json
import os
import yaml
import argparse
from getpass import getpass
import re
import ast
import time

def addServer(user, password, hostname, headers, sys_id_for_server, snow_url, server_table_uri, ubuntu_ref_number, 
                install_status, os, environment, logger, log_level):
    url = f'{snow_url}{server_table_uri}'
    info = {'os_version': ubuntu_ref_number, 'os' : os, 'install_status' : install_status, 
            'name' : hostname, "sys_id": sys_id_for_server, "environment" : environment}
    info = json.dumps(info)
    response = requests.post(url, auth=(user, password), headers=headers ,data=info, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

def addUser(user, password, headers, sys_id_for_user, snow_url, user_table_uri, user_name, email, logger, log_level):
    url = f'{snow_url}{user_table_uri}'
    info = {"user_name":user_name,"first_name":user_name,"sys_id":sys_id_for_user, "email":email}
    info = json.dumps(info)
    response = requests.post(url, auth=(user, password), headers=headers ,data=info, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

def addUsertoProfileTable(user, password, headers, ssh_Key, pw_Hash, sys_id_for_user, sys_id_for_profile, snow_url, 
profile_table_uri, user_name, u_gid, u_uid, logger, log_level):

    url = f'{snow_url}{profile_table_uri}'
    info = {"u_name":sys_id_for_user, "sys_id":sys_id_for_profile,"u_public_ssh_key":ssh_Key,
            "u_password_hash":pw_Hash, "u_username":user_name, "u_gid":u_gid,"u_uid":u_uid}
    info = json.dumps(info)
    response = requests.post(url, auth=(user, password), headers=headers ,data=info, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())    

def mapUserAndServer(user, password, headers, sys_id_for_user, sys_id_for_server, sys_id_for_map, snow_url, map_table_uri, logger, log_level):
    url = f'{snow_url}{map_table_uri}'
    info = {"u_name":sys_id_for_user,"u_hostname":sys_id_for_server, "sys_id":sys_id_for_map}
    info = json.dumps(info)
    response = requests.post(url, auth=(user, password), headers=headers ,data=info, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

def validateNewUser(user, password, headers, ssh_Key, pw_Hash, sys_id_for_profile, snow_url, profile_table_uri, 
ssh_and_pwhash_uri_query, logger, log_level):

    url = f'{snow_url}{profile_table_uri}/{sys_id_for_profile}{ssh_and_pwhash_uri_query}'
    response = requests.get(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    data = response.json()
    json_string = json.dumps(data)
    if pw_Hash not in json_string or (ssh_Key not in json_string):
        logger.debug('credentials not correct, validation for putting in new user credentials failed')
        raise ValueError('credentials not correct, validation for putting in new user credentials failed')  

def validateUpdatePW(user, password, headers, pw_Hash, sys_id_for_profile, snow_url, profile_table_uri, ssh_and_pwhash_uri_query, 
logger, log_level):

    url = f'{snow_url}{profile_table_uri}/{sys_id_for_profile}{ssh_and_pwhash_uri_query}'
    response = requests.get(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    data = response.json()
    json_string = json.dumps(data)
    if pw_Hash not in json_string:
        logger.debug('credentials not correct, validation for updating PW function failed')
        raise ValueError('credentials not correct, validation for updating PW function failed')  

def validateSSHCheck(user, password, headers, ssh_Key, sys_id_for_profile, snow_url, profile_table_uri, ssh_and_pwhash_uri_query, 
logger, log_level):

    url = f'{snow_url}{profile_table_uri}/{sys_id_for_profile}{ssh_and_pwhash_uri_query}'
    response = requests.get(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    data = response.json()
    json_string = json.dumps(data)
    if ssh_Key not in json_string:
        logger.debug('credentials not correct, validation for updating SSH function failed')
        raise ValueError('credentials not correct, validation for updating SSH function failed')  

def compareProfileFromServerToSnow(user, password, headers, local_ssh_key, local_pw_hash, sys_id_for_profile, snow_url, profile_table_uri, 
ssh_and_pwhash_uri_query, logger, log_level):

    url = f'{snow_url}{profile_table_uri}/{sys_id_for_profile}{ssh_and_pwhash_uri_query}'
    response = requests.get(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    data = response.json()
    json_string = json.dumps(data)
    logger.info(data)
    logger.info("snow credentials ABOVE, local credentials below")
    logger.info(local_ssh_key)
    logger.info(local_pw_hash)
    
    if local_ssh_key.strip() not in json_string.strip() or (local_pw_hash.strip() not in json_string.strip()):
        logger.debug('credentials not correct, validation for comparing profile from server to snow failed')
        logger.info(json_string)
        raise ValueError('credentials not correct, validation for comparing profile from server to snow failed')  

def removeProfile(user, password, headers, sys_id_for_profile, snow_url, profile_table_uri, logger, log_level):
    url = f'{snow_url}{profile_table_uri}/{sys_id_for_profile}'
    logger.debug(url)
    response = requests.delete(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers)

def removeMap(user, password, headers, sys_id_for_map, snow_url, map_table_uri, logger, log_level):
    url = f'{snow_url}{map_table_uri}/{sys_id_for_map}'
    logger.debug(url)
    response = requests.delete(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers)

def removeUser(user, password, headers, sys_id_for_user, snow_url, user_table_uri, logger, log_level):
    url = f'{snow_url}{user_table_uri}/{sys_id_for_user}'
    logger.debug(url)
    response = requests.delete(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers)

def removeServer(user, password, headers, sys_id_for_server, snow_url, server_table_uri, logger, log_level):
    url = f'{snow_url}{server_table_uri}/{sys_id_for_server}'
    logger.debug(url)
    response = requests.delete(url, auth=(user, password), headers=headers, verify=False)
    if response.status_code != 200: 
        logger.debug('Status:', response.status_code, 'Headers:', response.headers)

def main():
    logFile = logging.basicConfig(filename="user_management_validation.log",
        format='%(asctime)s %(message)s',
        filemode='w')
    logger = logging.getLogger()
    log_level = logger.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--user", help="SNOW user account name")
    parser.add_argument("-p", "--password", help="Password for SNOW user account")
    parser.add_argument("-w", "--snow_url", help="url of snow")
    parser.add_argument("-n", "--hostname", help="hostname on the server")
    parser.add_argument("-ls", "--local_ssh_key", help="local ssh key")
    parser.add_argument("-lp", "--local_pw_hash", help="local pw hash")
    parser.add_argument("-s", "--ssh_public_key", help="ssh key")
    parser.add_argument("-o", "--hashed_password", help="pw hash")
    parser.add_argument("-z", "--validate_mode", help="mode used to determine what is being validated, only used for validation pipeline")
    parser.add_argument("-v", "--validation_args", help="user management validation args")

    

    args = parser.parse_args()
    validation_script_args = (args.validation_args)
    # replaces singles quotes because they cause an error when trying to convert(.load) to JSON and 
    # dict ALWAYS has single quotes inserted into it when it is passed in from the playbook by default 
    pattern = "'"
    replacement = '"'
    formatted = re.sub(pattern, replacement, validation_script_args)
    validation_script_args = json.loads(formatted)
    
    snow_url = args.snow_url
    user = args.user
    password = args.password
    mode = args.validate_mode
    hostname = args.hostname
    ssh_Key = args.ssh_public_key
    pw_Hash = args.hashed_password
    local_pw_hash = args.local_pw_hash
    local_ssh_key = args.local_ssh_key

    ubuntu_ref_number = validation_script_args['ubuntu_ref_number']
    install_status = validation_script_args['install_status']
    os = validation_script_args['os']
    environment = validation_script_args['environment']
    user_name = validation_script_args['user_name']
    email = validation_script_args['email']
    u_gid = validation_script_args['u_gid']
    u_uid = validation_script_args['u_uid']

    server_table_uri = validation_script_args['server_table_uri']
    user_table_uri = validation_script_args['user_table_uri']
    profile_table_uri = validation_script_args['profile_table_uri']
    map_table_uri = validation_script_args['map_table_uri']
    
    ssh_and_pwhash_uri_query = validation_script_args['ssh_and_pwhash_uri_query'] 

    sys_id_for_user = validation_script_args['sys_id_for_user']
    sys_id_for_server = validation_script_args['sys_id_for_server']
    sys_id_for_profile = validation_script_args['sys_id_for_profile']
    sys_id_for_map = validation_script_args['sys_id_for_map']
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    if mode == "setUp":
        addServer(user, password, hostname, headers, sys_id_for_server, snow_url, server_table_uri, ubuntu_ref_number, 
                install_status, os, environment, logger, log_level)

        addUser(user, password , headers, sys_id_for_user, snow_url, user_table_uri, user_name, email, logger, log_level)

        addUsertoProfileTable(user, password, headers, ssh_Key, pw_Hash, sys_id_for_user, sys_id_for_profile, 
        snow_url, profile_table_uri, user_name,  u_gid, u_uid, logger, log_level)

        mapUserAndServer(user, password, headers, sys_id_for_user, sys_id_for_server, sys_id_for_map, snow_url, map_table_uri, 
        logger, log_level)

    elif mode == "newUserCheck":
        validateNewUser(user, password, headers, ssh_Key, pw_Hash, sys_id_for_profile, snow_url, profile_table_uri, ssh_and_pwhash_uri_query, 
        logger, log_level) 

    elif mode == "updatePWCheck":
        validateUpdatePW(user, password, headers, pw_Hash, sys_id_for_profile, snow_url, profile_table_uri, ssh_and_pwhash_uri_query, 
        logger, log_level)  

    elif mode == "updateSSHCheck":
        validateSSHCheck(user, password, headers, ssh_Key, sys_id_for_profile, snow_url, profile_table_uri, ssh_and_pwhash_uri_query, 
        logger, log_level) 

    elif mode == "unMap":
        removeMap(user, password, headers, sys_id_for_map, snow_url, map_table_uri, logger, log_level)

    elif mode == "removeAll":
        removeProfile(user, password, headers, sys_id_for_profile, snow_url, profile_table_uri, logger, log_level)
        removeUser(user, password, headers, sys_id_for_user, snow_url, user_table_uri, logger, log_level)
        removeServer(user, password, headers, sys_id_for_server, snow_url, server_table_uri, logger, log_level)  

    elif mode == "addProfile":
        compareProfileFromServerToSnow(user, password, headers, local_ssh_key, local_pw_hash, sys_id_for_profile, snow_url, profile_table_uri, 
        ssh_and_pwhash_uri_query, logger, log_level)


if __name__ == '__main__':
    main()