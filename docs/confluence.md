# Confluence Role
Confluence has four modes: Deploy, Backup, Update, Bounce, and Restore. The only scheduled job that runs for Confluence runs the backup mode, and it runs daily.

To run the modes add extra variable: mode
```
Ex.
mode=update
```
Confluence is currently running on Docker Host and Docker Prep Host

## Confluence Variables
| Name   |      Found      |  Value |
|----------|:-------------:|------:|
| mode |  group vars | update <br> deploy <br> restore <br> backup |
| volume_backups | default  vars |  5 |
|confluence_db_connection | host vars | **Prod Value** <br> jdbc:sqlserver://;serverName=6.2.0.176;portNumber=50281;databaseName=D_Confluence <br> **Prep Value** <br> jdbc:sqlserver://;serverName=6.2.7.176;portNumber=51870;databaseName=D_Confluence|
|confluence_db_user | host vars | **Prod Value** <br> d_confluence_prod <br> **Prep Value** <br> confluence_prep|
|confluence_proxy_name | host vars | **Prod Value** <br> confluence.web.yuma.army.mil <br> **Prep Value** <br> confluence.prep.yuma.army.mil|
|confluence_version | host vars | 8.5.4 |
|confluence_db_name | host vars | D_Confluence|
|confluence_sql_server | host vars |  **Prod Value** <br> 6.2.0.176,50281 <br> **Prep Value** <br> 6.2.7.176,51870|
|confluence_db_backup_dir| host vars | **Prod Value** <br> \\\\\\necfs\NEC\NEC_App\SQL_Prod_Backup\ProdITS\#OnDemand\DoNotDelete\Ansible\Confluence <br> **Prep Value** \\\\\\necfs\NEC\NEC_App\SQL_Prep_Backup\PrepITS\#OnDemand\DoNotDelete\Ansible\Confluence|
|confluence_db_daily_dir | host vars | **Prod Value** <br> \\\\\\necfs\NEC\NEC_App\SQL_Prod_Backup\ProdITS\YPGRW04XAAA49J3$PRODITS\D_Confluence\FULL <br> **Prep Value** \\\\\\necfs\NEC\NEC_App\SQL_Prep_Backup\PrepITS\Confluence\FULL|
|confluence_backup_dir | default vars | **Prod Value** <br> /mnt/backup/docker_volumes/confluence <br> **Prep Value** <br> /mnt/backup/docker_volumes/confluence/prep|
|confluence_db_restore_dir | default vars \\\\\\necfs\NEC\NEC_App\SQL_Prod_Backup\ProdITS\#OnDemand\DoNotDelete\Ansible\Confluence|
|confluence_restore_dir | default vars | /mnt/backup/docker_volumes/confluence|
|confluence_ports | host vars | 9080|
|confluence_container_name | default vars | confluence|
|confluence_healthcheck| default vars(prod, prep) group(dev)| https://{{confluence_proxy_name}}/status|

## Deploy
Deploy is used to deploy an instance of Confluence Microsoft SQL as its database. After this mode is ran you will have to setup Confluence.

## Backup
Backup creates a backup of Confluence-home and Confluence-config volumes. This mode will be scheduled to run nightly, but can be run on demand. The update mode will also run backup tasks.

The amount of backups kept is controlled by the variable volume_backups, more information about the variable can be found in the Confluence Variables section. Also in the Confluence Variables section you will find variables that contain information about where backups are saved.

## Update
Update is used to update the version of Confluence. If trying to upgrade Postgress review documentation for Confluence to see what versions of Postgress Confluence supports.

Before updating Confluence do a clone down and update Confluence prep first. Additional instructions will be in Atlassian_updates.md
 
## Bounce
Bounce will restart Confluence

## Restore
Restore is primarily used to clone down Confluence Prod to Confluence Prep, but can be used to restore Confluence Prod if any issues occur. Restore uses the most recent backup done. 

In the Confluence Variables section you will find variables that contain information about where restore is grabbing the backup file to use.