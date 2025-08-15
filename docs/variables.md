**Listed in order of precedence**
# Environment Variables
* Relates to the different environments (prod, prep, and dev)
* Ex. want prod to look at snow prod and dev to look at snow dev

# Vault
* Used to store variables where the value shouldn't be seen 

# Host Variables 
* Specific to the server it will be ran on
* To make a host variable file
    1. Make folder with the same name as the server
    2. Ensure the name uses all caps

# Group Variables 
* Used in more than one role

# Default Variables 
* Used for a specific role 

### Additional Information
* For information on variable precedence see [Ansible Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#ansible-variable-precedence)