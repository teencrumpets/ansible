# Before Running Role
**If SSH keys will be used on server run deploy role first**

# SSH Keys
* SSH keys by default will be setup on prod and prep servers, when left enabled the role will disable username password authentication when trying to SSH
* To disable SSH key setup either
    1. Set ssh_key=false at runtime (better option if lab server)
    2. Create host variable file that sets ssh_key=false (better option for prod, and prep)

## RHEL 8 Variables
| Name   |      Found      |  Value |
|----------|:-------------:|------:|
| All Vuln IDs |  default vars |  |
| rsyslog_linux_port |  default vars | 10614 |
| agent_name |  default vars |  |
| register |  default vars | false |
| grub_hash |  default vars | Hash of grub password |
| modload_imfile |  default vars | true |
| rsyslog_change |  default vars | true |
| inputfilename |  default vars | true |
| inputfiletag |  default vars | true |
| inputfilestate |  default vars | true |
| inputfileseverity |  default vars | true |
| inputfilefacility |  default vars | true |
| inputrunfile |  default vars | true |
## Important Variables
* Vuln IDs can be set to true or false in host variable files
* Register is used to determine if you want the server registered to RHSS, set to false by default

## Registering RHEL8 with Role
* When a RHEL8 server is registered, it is registered with the hostname set on the server
* Rules the hostname has to follow to be registered
    * All lowercase
    * No special characters including dashes and underscores

## How Registering works with Validation Pipeline
* In order to pass all packages tasks in the RHEL8 playbook the server must be registered
* Packages playbook includes a task that if the validation pipeline is being ran, the target server will be named according to the build agent running te pipeline
    * Build agent name has to be filtered to remove the underscore, for the register task to pass
    ```
    - script: |
        agent_name=$(echo $(Agent.Name) | tr -d '_')
        echo "##vso[task.setvariable variable=build_agent]$agent_name"
      displayName: 'Set filtered agent_name'
    ```