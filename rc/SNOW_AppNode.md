# Before Running Role
**Keep in mind that the RHEL8 deploy role is called first in the task sequence**

**Most of the time you'll be deploying this as an on demand environment so the use of SSH keys may not be the option you'll want**

# SSH Keys
* SSH keys by default will be setup on prod and prep servers, when left enabled the role will disable username password authentication when trying to SSH
* To disable SSH key setup either
    1. Set ssh_key=false at runtime (better option if lab server)
    2. Create host variable file that sets ssh_key=false (better option for prod, and prep)

## Post Configuration
* After both roles (app node and DB) Have been run you'll need to log into the app node via side door and the admin account in teamvault to configure additional settings. 
* Refer to the Post Clone section of the "cloing process" page in Confluence: 
https://confluence.web.yuma.army.mil/display/SNOW/Cloning+Process
* You must also make sure whatever is being done for SSL termination is in place before being able to hit this new environment via a secure connection and with a friendly name. 