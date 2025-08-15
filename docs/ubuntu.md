# Before Running Role
**If SSH keys will be used on server run deploy role first**

# SSH Keys
* SSH keys by default will be setup on prod and prep servers, when left enabled the role will disable username password authentication when trying to SSH
* To disable SSH key setup either
    1. Set ssh_key=false at runtime (better option if lab server)
    2. Create host variable file that sets ssh_key=false (better option for prod, and prep)
