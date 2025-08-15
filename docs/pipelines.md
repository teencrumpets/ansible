# Introduction
Pipelines are a series of steps that must be performed in order to deliver a new version of software. CI/CD pipelines are a practice focused on improving software delivery throughout the software development life cycle via automation. The team currently uses ADO (Azure Devops) to build pipelines. In our case, these pipelines are often used in connection with an specified role. 
# Set-up
There is a pipelines directory in the Repos section that contains a pipeline for every associated role. You create this yaml file  in the pipelines directory **BEFORE** creating a new pipeline under the pipelines tab, located under the Repos tab (Pipelines > Pipelines > New pipeline).  
**Until further notice, you MAY need to ask POCs to complete the below paragraph as you may not not have permissions** 
  
There are multiple ways to create it but the simplest is to click the "*classic editor*" option at the bottom, then change the default branch to the branch that you created your pipeline.yml file on. On the next step, there should be an option to apply the yaml template, which allows you to import your yaml file.  
# Start   
You should now be able to see your pipeline under the pipelines tab in the "All" section. After clicking your pipeline, you can click the "Run pipeline" button and if this is your first time running it, permissions to access variables needed for the pipeline are currently blocked until a POC gives you permission. This is only for the time first time and will not persist.
# Syntax and Structure   
The common elements  of some of the basic pipeline yaml files are as follows:  
  
**Triggers** define the events or conditions that will trigger the execution of your pipeline. Triggers can be based on specific branches, tags, or even schedules:
```
trigger:
  branches:
    include:
      - main
```
A **pool** is for selecting which agent to run the pipeline. In our case, most of the time it will be 'Linux Virtual' but can change:
```
pool:
  name: 'Linux Virtual'
```
**Variables** store values you may need to use in the pipeline:
```
variables:
  - group: Ansible
```
This is an example of an script in ADO pipelines. A script can run manual commands, custom scripts and or other logic. Below simply installs pip with a manual command: 
```
- script: python3 -m pip install --upgrade pip
  displayName: 'Upgrade pip'
```   
This script uses an ansible command to run a vmware module through a role. VMware is used to host virtual servers. In this case, the script deploys a vm (virtual machine) dynamically.

```
- script: ansible-playbook site.yml -i $(inventory_path).yml -e "HOSTS=localhost role=vmware ENV=dev vm_name=$(vm_name)" --vault-password-file=$(vault_key.secureFilePath)
  displayName: 'Deploying VM'
```
In this excerpt, this is where you test your role on the dynamically created vm. The example uses 'role=fortify_ssc' but you will replace 'fortify_ssc' with your own role. If your ENV is not dev, that may need to change as well to either dev, prep or prod. 
```
- script: ansible-playbook dynamic-site.yml -i $(inventory_path).yml -e " validation_group=fortify_ssc_validation ENV=dev vm_name=$(vm_name) role=fortify_ssc" --vault-password-file=$(vault_key.secureFilePath)
  displayName: 'Validating Fortify role'
```
Finally, this example removes the vm after all code has ran.
```
- script: ansible-playbook site.yml -i $(inventory_path).yml -e "HOSTS=localhost role=vmware ENV=dev vm_name=$(vm_name) vm_state=absent" --vault-password-file=$(vault_key.secureFilePath)
  displayName: 'Removing VM'
  condition: succeededOrFailed()
```

# Scheduling a Pipeline
Edit the pipeline you want to schedule, at the top right click the three dots, and then select triggers. From this page add a schedule.