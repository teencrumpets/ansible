# Files
```
site.yml
```
- Root-level playbook implementing YPG site infrastructure-as-code
- Imports the specified role

```
dynamic-site.yml
```
- Root level playbook for deploying a new VM and then running a role on that new host
- Includes a roles to create a VM, imports the specified role to run against it, then optionally includes a role to clean up the VM when done

# Basics
## Importing roles
- Used to force ansible to evaluate syntax/errors before anything starts running
- This avoids a scenario of VM being created and not getting cleaned up after code in this role throws an error Ansible can't ignore
- Importing a role preserves individual tags applied to tasks within that role

## Including roles
- Used to allow the play to start running before evaluating the role
- Some variables are defined during execution and would be undefined if Ansible evaluated the role before running
- Including a role with a tag applies that tag to every task in the role, individual tags applied to tasks within that role are not preserved

## Vars:
**continue_on_error**
- **Default**: `true`
    - Defined in **All** group variable file
    - Override to `true` `yes` `1` when used to validate roles
- Used to instruct an Ansible play importing a role to either stop or continue when encountering ignorable errors