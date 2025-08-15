# Build and Test

1. Before you start
    
    - Ansible must be ran from a Linux environment
    
    - **Do not** target the system you write and/or run Ansible playbooks on (AKA the control node)
    
    - The playbooks you write will target one or more **remote** endpoints
    
    - Read the `git` documentation to get started pulling the latest code

1. Install Ansible

    1. Verify Python is installed on your development system (If not, then install python3 using package manager)
        ```
        which python3
        ```
    1. Verify PIP is installed by confirming version info (If not, then install pip3 using package manager)
        ```
        python3 -m pip -V
        ```
    1. Install Ansible <span style="color:red">(DO NOT run as sudo, must be ran as user)</span>
        ```
        python3 -m pip install --user ansible
        ```
    1. Verify Ansible installation by confirming version info
        ```
        ansible --version
        ```
    1. Install `sshpass` via package manager when targeting Linux endpoints

1. <span style="color:yellow">**Create an inventory file**</span> for endpoints to target before running any playbooks
    - Tools to automatically build an inventory file are in the scripts directory
    - Can also be created manually

1. Ensure endpoint(s) being targeted have **ypgansible** user account installed and added to sudo/wheel

1. To run a playbook; make sure you are in the `ansible` directory

1. Run the playbook referencing these example commands if needed
    - Running a playbook
        ```
        ansible-playbook example_playbook.yml
        ```

    - Running an Ansible role (such as the Ubuntu role)
        ```
        ansible-playbook site.yml -e "HOSTS=lab_system role=ubuntu ENV=dev" --ask-vault-pass
        ```
    
    - Running an Ansible role without SSH password being disabled
        ```
        ansible-playbook site.yml -e "HOSTS=lab_system role=ubuntu ENV=dev ssh_key=''" --ask-vault-pass

    - To only play tagged tasks
        ```
        ansible-playbook site.yml -e "HOSTS=lab1 role=ubuntu ENV=dev" -t example_tag --ask-vault-pass
        ```
1. If connecting to Linux endpoints, enter the SSH password for `ypgansible` account on remote system(s) when prompted
    - Hit enter again (without typing anything else) when prompted for the BECOME password

# Ansible Task Examples
- All task names should include name of playbook the task is in, brief description of what the task does, and vulnerabilty ID if applicable
    ```
    name: Filesystem - Get list of system command files - V-238378
    ```