import requests
import warnings
import json
import os
import argparse

class keycloak_api_error(Exception):
    pass

def get_token(url, id, key='', user='', pw='', refresh_token=''):
    full_url = f"{url}realms/master/protocol/openid-connect/token"
    headers = {"Accept":"application/json"}

    if user and pw:
        data = {
            'username': user,
            'password': pw,
            'client_id': id,
            'grant_type': 'password'
        }

    if refresh_token:
        data = {
            'client_id': id,
            'client_secret': key,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.post(url=full_url, headers=headers, data=data, verify=False)

    if response.status_code != 200:
        print(response.json())
        raise keycloak_api_error('Generating token failed')
    
    return response.json()

def get_user(url, token, realm):
    full_url = f"{url}/admin/realms/{realm}/users"
    headers = {'Authorization': f'Bearer {token}'}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.get(url=full_url, headers=headers, verify=False)

    if response.status_code != 200:
        raise keycloak_api_error('Fetching user data failed')
    
    return response.json()

def get_realm(url, token, realm):
    full_url = f"{url}/admin/realms/{realm}/partial-export?exportClients=true"
    headers = {'Authorization': f'Bearer {token}'}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.post(url=full_url, headers=headers, verify=False)

    if response.status_code != 200:
        raise keycloak_api_error('Generating realm export failed')
    
    return response.json()

def import_full_realm(url, token, body):
    full_url = f"{url}/admin/realms"
    headers = {'Authorization': f'Bearer {token}'}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.post(url=full_url, headers=headers, data=body, verify=False)

    if response.status_code != 201:
        raise keycloak_api_error(response.json()['errorMessage'])
    
    return response

def import_partial_realm(url, token, body, realm):
    full_url = f"{url}/admin/realms/{realm}/partialImport"
    headers = {'Authorization': f'Bearer {token}'}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = requests.post(url=full_url, headers=headers, data=body, verify=False)

    if response.status_code != 201:
        print(response)
        raise keycloak_api_error(response.json()['errorMessage'])
    
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode")
    parser.add_argument("-r", "--realm")
    parser.add_argument("-l", "--link")
    parser.add_argument("-i", "--id")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--realm")

    args = parser.parse_args()
    mode = args.mode
    realm = args.realm
    base_url = args.link
    id = args.id
    user = args.user
    pw = args.password

    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = f"{script_directory}/realm-export.json"

    # base_url = 'https://keycloak.app.yuma.army.mil/'
    # id = 'admin-cli'
    # user = 'ypgadmin'

    try:
        refresh_token = get_token(url=base_url, id=id, user=user, pw=pw)['refresh_token']
        access_token = get_token(url=base_url, id=id, refresh_token=refresh_token)['access_token']
        print("Login successful")
        
        if mode == "export":
            realm_export = get_realm(url=base_url, token=access_token, realm=realm)
            export_stream = json.dumps(realm_export)

            with open(f'{json_path}', 'w') as file:
                file.write(export_stream)
            
            print(f"Export saved to {json_path}")

        elif mode == "full_import":
            with open(f'{json_path}', 'r') as file:
                realm_export = file.read()

            import_full_realm(url=base_url, token=access_token, body=realm_export)
        
        elif mode == "partial_import":
            with open(f'{json_path}', 'r') as file:
                realm_export = file.read()

            import_partial_realm(url=base_url, token=access_token, body=realm_export, realm=realm)

        elif mode == "get_user":
            my_user = get_user(url = base_url, token=access_token, realm=realm)
            print(my_user[0]['username'])
        
        print(f"Operation successful: {mode}")

    except keycloak_api_error as api_error:
        print(f"Error: {api_error}")
        exit(1)

if __name__ == "__main__":
    main()