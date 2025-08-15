# Jira Role
Jira has four modes: Deploy, Backup, Update, Bounce, and Restore. The only scheduled job that runs for Jira runs the backup mode, and it runs daily.

To run the modes add extra variable: mode
```
Ex.
mode=update
```
Jira is currently running on Docker Host and Docker Prep Host

## Jira Variables
| Name   |      Found      |  Value |
|----------|:-------------:|------:|
| mode |  group vars | update <br> deploy <br> restore <br> backup |
| volume_backups |    default   |   5 |
jira_db | host vars | jiradb
jira_db_connection | host vars | jiradb
jira_db_user | host vars | jiradb
jira_ports | host vars | **Prod Value** <br> 9078 <br> **Prep Value** <br> 9077
jira_version | host vars | 9.15.1
postgres_version | host vars | 15.6
db_volume | default vars | jira-db
jira_volume | default vars | jira-home
jira_logs | default vars | jira-logs
collation | default vars | en_US.UTF-8
postgres_container_name | default vars | postgres
jira_container_name | default vars | jira
jira_proxy_name | host vars | jira.web.yuma.army.mil
jira_ca | default vars | jira-ca
jira_backup_dir | default vars | **Prod Value** <br> /mnt/backup/docker_volumes/jira/home <br> **Prep Value** <br> /mnt/backup/docker_volumes/jira-prep/database
jira_restore_dir | default vars | **Prod Value** <br> /mnt/backup/docker_volumes/jira/home <br> **Prep Value** <br> /mnt/backup/docker_volumes/jira/home
postgres_restore_dir | default vars | **Prod Value** <br> /mnt/backup/docker_volumes/jira/database <br> **Prep Value** <br> /mnt/backup/docker_volumes/jira/database
postgres_backup_dir | default vars | **Prod Value** <br> /mnt/backup/docker_volumes/jira/database <br> **Prep Value** <br> /mnt/backup/docker_volumes/jira-prep/database
|jira_healthcheck| default vars(prod, prep) group(dev)| https://{{jira_proxy_name}}/status|

## Deploy
Deploy is used to deploy an instance of Jira with a Postgress as its database. After this mode is ran you will have to setup Jira.

If you're trying to import a backup from a previous instance of Jira, add the backup to /var/lib/docker/volumes/jira-home/_data/import on the server running your instance.

## Backup
Backup creates a backup of jira-home and jira-db volumes. This mode will be scheduled to run nightly, but can be run on demand. The update mode will also run backup tasks.

The amount of backups kept is controlled by the variable volume_backups, more information about the variable can be found in the Jira Variables section. Also in the Jira Variables section you will find variables that contain information about where backups are saved.

## Update
Update is used to update the version of Jira, and can update the version of postgress if necessary. If trying to upgrade Postgress review documentation for Jira to see what versions of Postgress Jira supports.

Additional instructions will be in Atlassian_updates.md

## Bounce
Bounce will restart Confluence

## Restore
Restore is primarily used to clone down Jira Prod to Jira Prep, but can be used to restore Jira Prod if any issues occur. Restore uses the most recent backup done. 

in the Jira Variables section you will find variables that contain information about where restore is grabbing the backup file to use.