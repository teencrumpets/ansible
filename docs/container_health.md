# Health Check Role
## About
- Two parts to how the role works:
    1. Have to have a health check in the compose file
        - Once a health check is added to a compose file and the container is started with the health check in its compose file, the container will be marked "healthy", or "unhealthy".
    1. The container_health role has to be added to the role for the application
        - Ex. add before application gets backed up so that if the container is unhealthy the backup won't happen because the applications role will fail
- When the health check role is ran, it will grab the compose file from the role it's ran in and grab all the container names. The role checks if the containers are healthy and will fail if a container is unhealthy

## Variables 
| Name   |      Found      |  Value | Description |
|----------|:-------------:|:-------------:|------:|
| retry_health_task | defaults | 25 | Number of times task is rerun to check if containers healthy |
| time_between_task_attempts | defaults | 20 | Time it takes to try and run command again to check if container is healthy |
| compose_file_path | defaults | /home/ypgansible/compose.yaml | Path where compose file is copied |

## How to Implement
- Find a command to use to check if application is up (ex. from jira: curl -sk jira.web.yuma.army.mil/status)
- Add to compose file 
    ```
    healthcheck:
      test: ["CMD-SHELL", "curl -sk jira.web.yuma.army.mil/status"]
      interval: 30s
      timeout: 5s
      retries: 15
    ```
    - About the parameters
        - test: The command that is used to determine if the container is healthy
        - interval: Time between when the command gets ran again
        - timeout: Time the command has to run before it automatically fails
        - retries: How many times the command is retried 
- Add to the applications role
    - If the application role has a backup mode, have health check role before the backup is taken
    - If the application role stops the application in a mode, have the healthcheck run after the application is started again
    - Ex. of how to add health check to an application role
    ```
    - name: Start Jira service
      command:
        cmd: 'docker compose up -d'
        chdir: /opt/compose/jira
      changed_when: false
      when: (mode == "backup") or (mode == "deploy") or (mode == "update") or (mode == "restore") or (mode == "bounce")
      
    - import_role:
      name: 'container_health'
      when: mode != "deploy"