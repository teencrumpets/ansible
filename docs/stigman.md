# Running STIGMan deployment pipeline
* **Select Environment**: This chooses whether the role will be ran on a lab, dev, prep, or prod environment system.
* **Name of Server**: This is where you enter the system name (in caps) of the system in which you want stigman deployed on
* **Mode**: "deploy" deploys stigman on the chosen server. "restore"

# STIGMan Variables
* The following are the required variables in order for the role to work properly.
```
stigman_nginx_version               # This specifies the image version for nginx that the container will be running
stigman_port                        # This is the port in which the stigman application will be using on the host
stigman_version                     # This specifies the image version for stigman that the container will be running

stigman_kc_version                  # This specifies the image version for keycloak that the container will be running
stigman_kc_adm_username             # Keycloak username used for stigman.yuma.army.mil/kc
stigman_kc_host_url                 # The url used for users to access the keycloak gui
stigman_kc_host_adm_url             # The url used for users to access the keycloak gui

stigman_oidc_provider
stigman_client_oidc_provider        
stigman_db_user                     # The database (mysql) user account used in the background for stigman (same as the stigman_mysql_user below)
stigman_swagg_server        

stigman_mysql_version               # The mysql image version used for the container
stigman_mysql_user                  # The database (mysql) user account used in the background for stigman (same as the stigman_db_user above)
stigman_mysql_database              # name of the mysql database that stigman uses

stigman_mysql_backup_dir            # Volume directory where backups for mysql are stored
stigman_mysql_restore_dir           # Volume directory where backups are restored from (will be different on prep environments)
stigman_keycloak_backup_dir         # Volume directory where keycloack data is backed up
stigman_keycloak_restore_dir        # Volume directory where keycloak data is restored from (will be different on prep environment)
stigman_binary                      # Directory on share where files are stored for the role to access (like truststore)

stigman_webserver                   # Name of webserver (nginx) volume
stigman_html                        # Name of html volume for stigman
stigman_volume                      # Name of main stigman volume (home)
stigman_accessmanagement            # Name of keycloak volume
stigman_database                    # Name of mysql database volume
```