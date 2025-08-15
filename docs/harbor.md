# Harbor
* The Harbor Role creates the compose file in the deploy playbook
* Harbor role has five modes: Deploy, Backup, Restore, Update, and Bounce

## Variables
| Name   |      Found      |  Value |
|----------|:-------------:|------:|
| harbor_version |  defaults | 2.11.1 |
| harbor_install_dir | defaults |  /opt/harbor |
| harbor_installed | defaults | false |
| harbor_temp_dir | defaults | /tmp/harbor |
| harbor_name | defaults | registry.web.yuma.army.mil |
| harbor_port| defaults | 80 |
| run_docker | group vars (all) | true |
| run_ubuntu | group vars (all) | true |
| backup_share | group vars (all) | "6.2.2.133:/export/Backup" |
| backup_mount_dir | group vars (all) | /mnt/app |
| backup_mount_dir_harbor | defaults | "{{ backup_mount_dir }}/harbor" |
| harbor_backup_dir | defaults |  "{{backup_mount_dir_harbor}}/docker_volumes/harbor/{{ENV}}/data" |
| harbor_restore_dir| defaults | "{{backup_mount_dir_harbor}}/docker_volumes/harbor/prod/data" |