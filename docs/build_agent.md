# Build Agent Role
- This role is dependent on being given a pat token from ADO. These tokens expire so if the task to cofigure the build agent fails the variable ado_pat in the prod vault needs to be changed.

- To pass the ADO pipeline validation the variable ado_pat must be set with a pat in the dev vault
# Build Agent Role
- Can use this role to create multiple build agents on one server
- UMASK is set to 022 at the beginning of this role to allow ansible and python modules to be installed as root, changes back to 077 at end of playbook
- This role is dependent on being given a pat token from ADO. These tokens expire so if the task to configure the build agent fails the variable ado_pat in the prod (or dev vault if token for validation has expired) vault needs to be changed. To add an token, click your profile icon in ADO and then select "Security" where there should be option to add token, where it should be given custom access to only have access to read and manage agent pools. (Only shows up when "Show all scopes" is clicked).

- To pass the ADO pipeline validation the variable ado_pat must be set with a pat in the dev vault

## Important Variables
- build_agents
    - This variable sets the name of the service account the agent will run on, the pool the agent will be placed, and the build agent name
    - Set in a host variable file: 
    ```
    build_agents:
      - build_agent: 
        name: Name of build agent
        agent_pool: Name of pool
        agent_account: "Service account name"
    ```

- ado_url
    - The ADO Collection must be specified in the ADO url

## Commands to run role manually
- Read the rest of this documentation before running following commands
- Can change ENV if you don't have access to prod
### With Docker and Ubuntu
`ansible-playbook site.yml -e "HOSTS=build_server_name role=build_agent ENV=prod" --ask-vault-pass`
### Just to install build agents
`ansible-playbook site.yml -e "HOSTS=build_server_name role=build_agent ENV=prod fast=true" --ask-vault-pass`  
## Troubleshooting
If space fills up,:
```
# docker system prune -a
 ```  

or if no unused images may need to delete data from work folders. Would need to cd into 
/opt/build_agents/some_agent_name/_work and rm all contents in _work subdirectory

In rare circumstances, an agent may need to be deleted from the server in order to re-install with the correct permissions/scope. In this case, the directory of the build agent as well as the service needs to be deleted. Below is example  


```
sudo rm -rf /opt/build_agents/ypg_linux_1/
 ```  
 ```
sudo systemctl reset-failed
```

 The command "systemctl reset-failed" will reset all units with failed status

Do not remove service name from systemd unless there is an explicit error