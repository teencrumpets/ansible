# About Keystone
- Modes
    - deploy
        - This mode will deploy an instance of Keystone on a Docker Host dependent on environment selected.
    - update
        - This mode will backup and then update Keystone by changing the compose file if there's any changes and restarting the app. This is disruptive, ensure downtime is scheduled before running this on production instance.
        - For more information on how to update Keystone reference section: Updating Keystone
    - bounce
        - This mode will restart the application. This is disruptive, ensure downtime is scheduled before running this on production instance.
    - backup
        - This mode will backup data from /mnt/keystone directory. This is disruptive, ensure downtime is scheduled before running this on production instance.
    - restore
        - This mode will restore Keystone using laest backup. This is disruptive, ensure downtime is scheduled before running this on production instance. If restoring to a lab instance there will be an error unless the passwords for the backend databases are the same. 

## Updating Keystone
- MORSE provides images and compose file for Keystone
    - Ensure all images get scanned and uploaded to Harbor
    - Compare new compose file with old
    - Change versions being used in role
    - Schedule down time
    - Run pipeline with update mode

## Testing Changes to Role
1. Deploy new instance
2. Deploy restored instance
3. Remove and add self back in Keycloak

## Files
- compose.yaml
    - The compose file is the initial setup for Keystone. We don't change the compose file unless their was a change provided by morse. Any change we want to make to the Keystone stack is done with the override template.

## Templates
- .env.j2
    - Stores configuartion settings for Keystone to reference.
- override.yaml.j2
    - The keystone images and compose file are provided by MORSE. In this compose file there are images such as Keycloak that we don't want to start, so an override file was created. Keep in mind because we are using an override the command to start Keystone differs from the usual command. 

## Pipelines
- Keystone
    - Located under On-Demand/Applications
    - Ensure that the host variables have been set correctly
    - Can set off Deploy, Bounce, Backup, Restore, or Update
- Backup - Keystone
    - Located under Scheduled
    - Scheduled to set off backup of Keystone prod

## Variables
### Environment Variables
- Located in vault
```YAML
keystone_celery_pw: Relates to Celery Postgres container
keystone_kcadmin_pw: Relates to Keystone Keycloak Postgres container
keystone_kcdb_pw: Relates to Keystone Keycloak Postgres container
keystone_db_pw: Relates to Postgres container
keystone_rabbit_pw: Relates to RabbitMQ container
keystone_keytab_pw: For Windows Share access
```

### Host Variables

```YAML
application_stor_lab: Contains the device name shown when running "lsblk" for where keystone will be storing application storage on /mnt/keystone/ 960 GB SSD
containers_stor_lab: Device name in "lsblk" for where keystone stores keystone configuration files and docker containers on /mnt/data 20TB HDD RAID 10
application_part: Actual partition being made on the application storage device, this partition will be using 100% of the associated device's storage
containers_part: Partition being made on the containers storage device, this partition will be using 100$ of the associated device's storage
kc_env_hosturl: URL for Keystone with /auth
kc_env_admhosturl: URL for Keystone with /auth
wildcard_cert: SSL cert being used for instance of Keystone (lab.crt, rc.crt, or app.crt)
wildcard_key_name: SSL key being used for instance of Keystone (lab.key, rc.key, or app.key)
wildcard_fqdn: FQDN linked to environment Keycloak is in (lab.yuma.army.mil)
keystone_nginx_server: The Nginx server that Keystone needs a proxy config in
keystone_service_file: This will be the proxy config file name
keystone_url: URL for Keystone
keystone_ports: Keystone port
keystone_auth_oidc: Keycloaks .well-known/openid-configuration Keystone reaches out to

fstab_config_host: variable list that contains regexp items for mounts you want to keep in /etc/fstab. If an entry is not added to this list and the role is ran, those entries will be removed. You add another entry by adding a hyphen
(-) on the next line and keeping the indentation, then creating a regexp with tools like regexp101. If you see the entries already in use, you can see the pattern on how to make yours.

Ex. of fstab
fstab_config_host:
  - (?=(^(.(?!(\s+\/mnt\/keystone\s+)))*$))
  - (?=(^(.(?!(\s+\/mnt\/data\s+)))*$))
  - (?=(^(.(?!(\s+\/mnt\/keystone_share\s+)))*$))

host_accounts: Accounts associated with KEystone that need t be on the server. If an account is not listed here it will be removed by user management.

Ex. of host_accounts
host_accounts:
  - username: keystone
    uid:
    gid:
    ssh:
    password_hash:
  - username: rtkit
    uid:
    gid:
    ssh:
    password_hash:
  - username: nvidia-persistenced
    uid:
    gid:
    ssh:
    password_hash:
  - username: dnsmasq
    uid:
    gid:
    ssh:
    password_hash:
  - username: avahi
    uid:
    gid:
    ssh:
    password_hash:
  - username: cups-pk-helper
    uid:
    gid:
    ssh:
    password_hash:
  - username: pulse
    uid:
    gid:
    ssh:
    password_hash:
  - username: geoclue
    uid:
    gid:
    ssh:
    password_hash:
  - username: saned
    uid:
    gid:
    ssh:
    password_hash:
  - username: colord
    uid:
    gid:
    ssh:
    password_hash:
  - username: gdm
    uid:
    gid:
    ssh:
    password_hash:
 
manage_ubuntu_V_238367: Ubuntu check that needs to be false

ufw_host: Firewall Rules specific to the server

Ex. of firewall rule needed for Keystone
ufw_host
  - order: 100
    rule: 'allow'
    direction: 'in'
    from_ip: nginx subnet (grab from nginx defaults)
    proto: 'tcp'
    to_port: Keystone port
```

### Default Variables 
Potential Host Variables
```YAML
isPhysical: Boolean for if instance of Keystone is on physical server, if not add this variable to host file
```

```YAML
keystone_db_user: Relates to Postgres container
keystone_celery_user: Relates to Celery Postgres container
keystone_kcdb_user: Relates to Keystone Keycloak Postgres container
keystone_rabbit_user: Relates to RabbitMQ container
keystone_kcadmin_user: Relates to Keystone Keycloak Postgres container

keystone_compose: Path to Keystone compose file

nginx_container_name: "keystone-nginx"
backend_container_name: "keystone-backend"
backend_db_container_name: "keystone-backend-db"
keycloak_db_container_name: "keystone-keycloak-db"
celery_db_container_name: "keystone-celery-db"
rabbitmq_container_name: "keystone-rabbitmq"
worker_common_container_name: "keystone-worker-common"
worker_ml_container_name: "keystone-worker-ml"
filesharemgr_container_name: "keystone-file-share-mgr"
keycloak_container_name: "keystone-keycloak"

Harbor URLS don't usually change, but version tags will change with updates
harbor_url_for_keystone_frontend: "registry.web.yuma.army.mil/library/keystone_frontend"
keystone_frontend_version_tag:
harbor_url_for_keystone_backend: "registry.web.yuma.army.mil/library/keystone_backend"
keystone_backend_version_tag:
harbor_url_for_keystone_postgresql: "registry.web.yuma.army.mil/library/keystone_postgres"
keystone_postgresql_version_tag:
harbor_url_for_keystone_rabbitmq: "registry.web.yuma.army.mil/library/keystone_rabbitmq"
keystone_rabbitmq_version_tag:
harbor_url_for_keystone_workercommon: "registry.web.yuma.army.mil/library/keystone_workercommon"
keystone_workercommon_version_tag:
harbor_url_for_keystone_workerml: "registry.web.yuma.army.mil/library/keystone_workerml"
keystone_workerml_version_tag:
harbor_url_for_keystone_filesharemgr: "registry.web.yuma.army.mil/library/keystone_filesharemgr"
keystone_filesharemgr_version_tag: 
harbor_url_for_keystone_keycloak: "registry.web.yuma.army.mil/library/keystone_keycloak"
keystone_keycloak_version_tag: 

backup_mount_dir_keystone: Path to mount point for backup share
keystone_db_volume_dir: Path to Keystones database volume directory
keystone_backup_dir: Path to save Keystone backup to
keystone_restore_dir: Path to grab Keystone backup from

nec_svr_ops_dir_keystone: Path to mount point for server ops share
keystone_library: Path to keystone library
Keystone_windows_share: Windows Share that Keystone uses
keystone_fileshare_user: Service account to access Windows share

keystone_app_stor_dir: Mount point for Keystones database volumes
keystone_data_stor_dir: Moint point for data volume
keystone_share_path: Mount point for Windows Share

The different MTLS PEMs
mtls_ca: "/etc/ssl/ca.pem"
mtls_server: "/etc/ssl/server.pem"
mtls_server_key: "/etc/ssl/server-key.pem"
mtls_client: "/etc/ssl/client.pem"
mtls_client_key: "/etc/ssl/client-key.pem"

fstab default configuartion
fstab_config_default:
  - (?=(^(.(?!(\s+\/\s+)))*$))
  - (?=(^(.(?!(\s+\/boot\s+)))*$))
  - (?=(^(.(?!(\s+\/var\/log\/audit\s+)))*$))
  - (?=(^(.(?!(\s+\/boot\/efi\s+)))*$))
  - (?=^((?!(#)).*$))
  - (?=^((?!(\/swap)).*$))

fstab_regexp_begin: (
fstab_regexp_end: .+$)
```

## Setting up Keystone Keycloak client
1. Create Keystone groups
    - In the Keystone client create a role for all the keystone groups
    - Map corresponding roles to groups when creating
    - Ensure Keycloak setup for fine grain access, reference application_delivery_controller documentation in section 'Setup for Group Management'
    - Create a group for the Keystone group managers (role mapped to thisgroup most likely a Keystone admin role)
    - Add group managers for Keystone into two groups
      1. Keystone_group_managers
        - This group once the permissions are setup gives members access into specific keystone groups
      1. group_managers
        - This group allows group managers to add and remove users from groups
    - For setting up permissions for the Keystone group managers reference application_delivery_controller documentation in section 'Setup for Group Management'

1. Create Keystone client
    - Within the keystone client:
      - In roles section, create a role for all keystone groups
      - In client scopes section, in keystone-dedicated create mappers
        1. Mapper type: Group Membership, Name: group, Token claim name: groups. Uncheck full group path
        1. Mapper type: User Client Role, Name: client roles, Client ID: keystone, Token claim name: resource_access.${client_id}.roles