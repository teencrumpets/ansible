# VMware Role
## Modules Used
-  vmware_guest
    - This module creates th VM but doesn't add the network adaptor 
    - When the network adaptor was added with this role sometimes the network adaptor wouldn't be connected
- vmware_guest_network
    - Adds the network adaptor to the vm that was created
    - If the role is ran to remove the VM the task with this module won't run

# Variables

#  Examples
- Create a VM
    ```
    ansible-playbook site.yml -e "HOSTS=localhost role=vmware vm_name=node_1 ENV=dev" --ask-vault-pass
    ```

- Run a role on newly created VM
    ```
    ansible-playbook dynamic-site.yml -e "HOSTS=localhost role=ubuntu vm_name=node_1 ENV=dev ssh_known_hosts_file='/dev/null'" --ask-vault-pass
    ```