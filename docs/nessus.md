# Introduction
Installs nessus agent and connects it to the nessus manager server, which is able to manage the scans of all servers w/ an nessus agent linked to it. Installion is NOT disruptive.

The last couple task in the nessus playbook links the system to the nessus manager for rhel or ubuntu, the task will return changed if being successfully linked for the first time, and returns ok if given an 409 error, which indicates the system has already been linked. 
Fails if given any other error or output. Look at the last task in the nessus playbook for reference.

When the nfs share for the nessus agent is changed or updated, update the ubuntu_nessus_file and rhel_nessus_file variables in the main.yml file **UNDER** the folder defaults. Other variables listed here can be changed as necessary only if needed.

# Updating nessus installer
Whenever there is a vulnerability or other issue that causes the currently installed version of Nessus to be outdated or incompatible, the role will need to be update. The process is as follows:  
1.  Drag and drop new install file from local computer to dev server
    - The standard process currently is to ssh into a ubuntu server from VS code, where you can open a folder, then drag and drop the new install file from your local window location. **NOTE:** If the new install is in a windows share, you must move it to any folder on your PC (not on a share) or it will not work. If you do not use VS code, other procedures such as scp may suffice. Currently new install files are being placed in a window share at the path e \\necfs\nec\NEC_Misc\Nessus\Agents.

1. Prerequsite: If you **NEVER** mounted anything manually on the linux server you're using, you may need to create an directory to use as a mount point where you will go to access the contents of the share. Folder after /mnt can be name of your choosing.
    ```
    mkdir /mnt/mnt_point
    ```

1. Mount linux share and move file into there
    ```
    mount 6.2.2.243:/nec_svr_ops /mnt/mnt_point
    ```
    
    ```
    mv /path_to_where_you_put_new_install /mnt/mnt_point/nessus_agent/
    ```
    **Note:** The above nessus_agent path is the path on the share that corresponds to where we keep nessus installs

1. Replace variable in defaults folder in nessus
    - Navigate to the main file in the defaults folder under nessus in  this repo
    
    -  Swap the value of the variables for ubuntu_nessus_file and rhel_nessus_file with the names of the new installs you have.

    -  Run the nessus pipeline on servers that need the updated install




