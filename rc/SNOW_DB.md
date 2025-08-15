# Before Running Role
**Keep in mind that the RHEL8 deploy role is called first in the task sequence**

**Most of the time you'll be deploying this as an on demand environment so using SSH keys may not be the option you'll want**

# SSH Keys
* SSH keys by default will be setup on prod and prep servers, when left enabled the role will disable username password authentication when trying to SSH
* To disable SSH key setup either
    1. Set ssh_key=false at runtime (better option if lab server and for on demand)
    2. Create host variable file that sets ssh_key=false (better option for prod, and prep)

## Partioning for Glide
* After the VM is deployed and the RHEL8 Role has been ran AND before running the SNOWDB role you must first
    Add the extra disk inside vCenter from the VM settings for the glide partition. 
* follow the instructions here for using LVM to create the glide partition: 
https://confluence.web.yuma.army.mil/display/SNOW/Creating+Glide
* In a later iteration of this role Partioning tasks may be added

## User Management
There is one account that needs to be created for MariaDB/mysql this user is simply called mysql. 
This user is created in the deploy role. 
* User management will still need be figured out

