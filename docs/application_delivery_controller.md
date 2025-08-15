# Information on Application Delivery Controller (ADC)
The intention behind the ADC project is to eventually replace the F5. There are two roles that are apart of ADC, Keycloak and Nginx, further information on these roles will be below.

# About Nginx
- DO NOT RESTART THIS APP MANUALLY
    - For more information read dependencies section
- Modes
    - deploy
        - This mode will deploy an instance of Nginx, must know the name of the server that Nginx will be deployed on.
        - Nginx should be deployed before Keycloak.
    - update
        - This mode will update Nginx by changing the compose file if there's any changes and restarting the app. This is disruptive, ensure downtime is scheduled before running this on production instance.
    - bounce
        - This mode will restart the application. This is disruptive, ensure downtime is scheduled before running this on production instance.
    - add_service
        - This mode is used in other application roles to add service files to Nginx Configuration. 
    - remove_service
        - This mode has not been implemented anywhere yet.

## Adding Service File
- An application that is going to use nginx as a reverse proxy needs to add tasks in its role to call Nginx to insert a service file into the Nginx Configuration.
```YAML
- name: Get IP of {{ ansible_hostname }} for service file
  set_fact:
    app_ip: "{{ ansible_host }}"
  when: app_mode in ["deploy"]

- name: Add App service file to Nginx
  delegate_to: "{{ nginx_server }}"
  block:
    - name: Run add service in nginx
      import_role:
        name: 'nginx'
      vars:
        nginx_mode: "add_service"
        service_config: "{{ app_service_file }}"
        fqdn: "{{ app_url }}"
        app_server: "{{ app_ip }}"
        app_port: "{{ app_ports }}"
  when: app_mode in ["deploy"]
```

## Removing Service File
- There's a task in the role located in the config playbook that is currently not in use

## Dependencies
- ssl.pass file
    - In order for Nginx to start correctly there needs to be an ssl.pass file that gives the passphrase for the ssl key. This file is never left on the server, and the role handles it's placement and removal. Do not restart Nginx manually, always use the role.

## Pipelines
- Nginx
    - Located under On-Demand/Applications
    - Must know the server the Nginx instance you want to run the pipeline against
    - Ensure that the host variables have been set correctly
    - Can set off Deploy, Bounce, or Update

## Variables
### Environment Variables
- Located in vault
```YAML
ssl_password: Passphrase for the SSL key
wildcard_key: SSL key
```
- wildcard_key
    - needs to be in specific format
    - Every line below 'wildcard_key: |' needs to be indented
    ```YAML
    wildcard_key: |
        -----BEGIN RSA PRIVATE KEY-----
        Proc-Type:
        DEK-Info:

        rest of key
        -----END RSA PRIVATE KEY-----
    ```
- Example of ansible task that adds an ssl key file using a variable
    ```YAML
    - name: Copy wildcard key file
      copy:
        content: "{{ wildcard_key }}"
        dest: "/var/lib/docker/volumes/{{ cert_volume }}/_data/{{ wildcard_key_name }}"
        owner: 2002
        group: 2002
        mode: 0774
    ```


### Host Variables

```YAML
wildcard_cert: SSL Certificate file name
wildcard_key_name: SSL Key file name
wildcard_fqdn: Wildcard FQDN
```

### Default Variables 
Potential Host Variables
```YAML
nginx_name: Container name for Nginx
```

```YAML
harbor_url_for_nginx: URL where image for Nginx is in Harbor
nginx_version_tag: Tag of Nginx in Harbor
nginx_ports: Port Nginx uses
nginx_volume: NAme of volume for Nginx Config
cert_volume: Name of volume that has Nginx SSL certs
banner_volume: Name of volume that has banner for Nginx
compose_path: Path to compose file
service_template: Name of application service template
nec_svr_ops_dir_nginx: Mount point of NFS share for binary data
cacerts_dod_usa: Path to cacerts file
wildcard_cert_path: Path to SSL Cert file
ssl_conf_path: Path to Nginx SSL Config
config_path: Path to Nginx Config directory conf.d
proxy_conf_path: Path to Nginx Proxy Config
ssl_config: SSL Config path within Nginx container
proxy_config: Proxy Config path within Nginx Container
```

# About Keycloak
- Modes
    - deploy
        - This mode will deploy an instance of Keycloak and postgres, must know the name of the server that Keycloak will be deployed on.
        - Nginx should be deployed before Keycloak.
    - update
        - This mode will update Keycloak by changing the compose file if there's any changes and restarting the app. This is disruptive, ensure downtime is scheduled before running this on production instance.
    - bounce
        - This mode will restart the application. This is disruptive, ensure downtime is scheduled before running this on production instance.
    - restore
        - This mode by default restores Keycloak from the newest production backup of Keycloaks Posgres Database.
    - backup
        - This mode will take a backup of Keycloaks database Postgres on chosen environment. By default there is only one backup found at anytime on the NFS Share for each environment where the backup is stored. If an older backup is needed, get with commvault admin.

## Dependencies
- Nginx
    - Nginx must be deployed before Keycloak
    - Requires a service file to be created for Nginx. This is done in the Keycloak role through the deploy mode

## Variables
### Environment Variables
- Located in vault
```YAML
trust_store_pass: PAssword for trust store
kc_admin_pw: Password for intial user in Keycloak
postgres_keycloak_pw: PAssword for Keycloak database
```

### Host Variables

```YAML
keycloak_hostname: FQDN for Keycloak
keycloak_nginx_server: Server Name Nginx is on
keycloak_service_file: Name of service file being placed in Nginx Config
```

### Default Variables 
# keycloak compose config

Potential Host Variables
```YAML
kc_db_container_name: Name of Postgres Container
adc_keycloak_container_name: Name of Keycloak container
keycloak_port: Port Keycloak is using
```

```YAML
harbor_url_for_postgres: URL where image for Postgres is in Harbor
postgres_version_tag: Tag of Postgres in Harbor
keycloak_db: Keycloak database name
harbor_url_for_keycloak: URL where image for Keycloak is in Harbor
keycloak_version_tag: Tag of Keycloak in Harbor
kc_db_volume: Name of volume for Postgres
cert_volume: NAme of volume storing certs
compose_path: Path to compose file
postgres_keycloak_user: Database User
kc_admin: Intial user of Keycloak
keycloak_service_template: Service template name for Keycloak
volume_backups: Number of Backups that get saved
postgres_restore_dir: Path where postgres pulls backup to restore from
postgres_backup_dir: Path where backups get saved
trust_store_path: Path to trust store
nec_svr_ops_dir_keycloak: Mount point of NFS share for binary data
backup_mount_dir_keycloak: Mount point for NFS share for backups
```

## Pipelines
- Keycloak
    - Located under On-Demand/Applications
    - Must know the server the Keycloak instance you want to run the pipeline against
    - Ensure that the host variables have been set correctly
    - Can set off Deploy, Bounce, Restore, Backup, or Update
- Backup - Keycloak
    - Located under Scheduled
    - Runs on production instance during scheduled time

## Setup for Group Management
1. In Realm settings ensure Admin Permissions is enabled
1. Create Groups
    1. group_managers
        - In this group add users that are going to be managaers of any group
    1. (clientName)_group_managers
        - In this group add users that will manage groups created for a specific client
1. Go into Permissions tab that shows up after Admin Permissions is enabled
    - Create Policies
        1. group_managers_group_members
            - This policy applies to all users that will be group managers
            1. Add group: group_managers
        1. manage_(clientName)_groups
            - This policy applies to all users that are group managers for the specific client
            - There can be multiple of these policies
            1. Add group: (clientName)_group_managers
    - Create Permissions
        1. manage_group_users
            - Authorization scopes: view, manage-group-membership
            - Enforce access to all users
            - Add policy group_managers_group_members
            - This permission allows all users in the group: group_managers to be able to add and remove users from groups. Due to how permissions work, they will only b able to do this for groups they have permissions to. Reference the second step below for how to create permission for group management.
        1. manage_(clientName)_groups
            - Authorization scopes: view, view-members, manage-membership
            - Enforce access to specific groups
                - Choose groups that were made for the specific client
            - Add policy manage_(clientName)_groups
            - This permission allows all users in the group: (clientName)_group_managers to manage groups that were setup for a specific client. Ensure all groups for client are added under specific groups for this permission.