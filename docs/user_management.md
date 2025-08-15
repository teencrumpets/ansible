## Functionality
 User Management will manage user accounts by providing the following:  
 **Main** functions:  
 * Adding user profiles on a server as necessary
 * Removing user profiles on a server as necessary  
 * Update a user profile ssh keys on the server  

Secondary functions:  
* update snow  
* update password hash
* installs and update ssh keys
* create user account(snow)

  **Note**: The functionality of user management is often confused with that of scheduled baselines(RHEL/UBUNTU). While User managements performs the above functions mentioned, it does  **NOT**:  
  * disable/enable password auth. based on if ssh-key auth. is enabled/disabled
  * apply stig settings  
  The above is done by scheduled baselines(RHEL/UBUNTU)

## User Management Description and Parameters
  The parameters is info. you will you be asked for when running an pipeline under user management. The parameters for each pipeline is listed below, (first time users read instructions on setting up ssh, generating keys, etc. here BEFORE running any of the below pipelines: https://confluence.web.yuma.army.mil/display/ND/SSH+User+Management):  

  **New Users**: New users should run this pipeline. Parameters:  
  * SSH_PUBLIC - paste the new ssh key you generated here
  * PASSWORD_HASH - paste the new password hash you generated here
  * USERNAME - Your username (target user)
  * ENV - target environment the code will run against
  
  **Update SSH Keys**: For users needing to update their ssh public key
  * SSH_PUBLIC - paste the new key you generated here
  * USERNAME - Your username (target user)
  * ENV - target environment the code will run against

  **Update Password**:  
  * PASSWORD_HASH - paste the new password hash you generated here
  * USERNAME - Your username (target user)
  * ENV - target environment the code will run against
  
  **User Management**:  
  * HOSTS - hostname of target server to be updated 
  * ENV - target environment the code will run against

# Before Running Role
**WARNING: This role will remove any account that isn't listed under default accounts, host accounts, or user accounts as described below**
## Default accounts
* ypgansible
* acas (created in role)
* mfe (created when Mcaffee installed)
* To look at complete list of default accounts see [User Management Default Variables](./defaults/main.yml)

## User Accounts
* Get's user account information from snow
* Get with snow admin to ensure your user account is mapped to the server (only if you need user account on server)

## Host Accounts 
* If the account you need added is not listed under defaults and is not a user account setup a host variable file
* Need host_accounts variable in the host variable file 
```
Example of what to include in the host variable file
host_accounts:
  - username: account1
    uid:
    gid:
    ssh:
    password_hash:
  - username: account2
    uid:
    gid:
    ssh:
    password_hash:
```
* Putting only username will ensure account doesn't get deleted 
* only fill out other fields if account needs to be created or modified by role

## SSH Key Setup
* This role will add public keys to server that it is ran on and disable reauthentication for sudo
* SSH keys are set to be added by default, if the server this roles is being ran on should not use ssh keys either
    1. Set ssh_key=false at runtime (better option if lab server)
    2. Create host variable file that sets ssh_key=false (better option for prod, and prep)

## Validation Pipeline 
* This section is for developers to ensure the main functions of user management are working through use of a validation pipeline
* After inital setup (populating necessary tables in SNOW for testing), the pipeline generally follows a pattern of testing a user management
  function, then proving or verifying (validate) the function worked. For example, the below runs user management in manage mode: 
  ```
  - script: ansible-playbook dynamic-site.yml -e "snow_url=$(snow_url) HOSTS=$(vm_name) ENV=dev role=user_management vm_name=$(vm_name) verify_hostname='' validation_group='' user_mode='manage'" --vault-password-file=$(vault_key.secureFilePath)
  displayName: 'Running manage mode on user management (adding profile to server)'
  ```
Next, we validate that it worked correctly, the below calls the validate role of user management to run validation tasks to validate the function of adding a profile
to the server:  
  ```
- script: ansible-playbook dynamic-site.yml -e "username=$(username) validate_mode="addProfile" ENV=dev vm_name=$(vm_name) role=user_management verify_hostname='' validation_group='' user_mode=$(playbook_mode)" --vault-password-file=$(vault_key.secureFilePath)
  displayName: 'validating adding profile w/ user management'
  ```
For our purposes, these "script" tasks either performs a call to an ansible playbook (validate_role.yml) that runs tasks to help validate the user management functions OR it runs the function of user management that is to be validated. The former may or may not run a python script (user_management_validation.py) to further help validate. You may want to look at those two files for deeper understanding.  

**Variables**: variables for this pipeline are in two places. The ssh public key and hashed password that are used for our test are stored in the Azure DevOps (ADO) library under user_managment in variable groups. The rest of the variables should be in the user_management_validation validation group which is under the group_vars folder. The only exception should be headers, which is directly in the python script (user_management_validation.py) and used for api calls.   
### Additional Notes
* For more information on host variables see [Variables Documention](../../Documentation/variables.md)