#Handling Ansible task errors
* Tasks that are expected to fail need to be handled a certain way if the intention is to have the playbook continue even if that particular task fails. An example of this is Trellix, the Trellix role is able to install the necessary installers but is unable to "tag" the systems via ESS. The expectaion for Trellix is that there needs to be two services enabled and runnning, but those services cannot be installed via code, instead they are installed on a system when tagged on ESS (for now...).

```
- name: Check status of ENS platform
  command: systemctl is-active mfeespd
  register: mfeespd_status
  failed_when: mfeespd_status.rc != 3 and mfeespd_status.rc != 0
  changed_when: false

- name: Ensure mfeespd is active - V-238334
  service:
    name: mfeespd
    enabled: true
    state: started
  when: ("{{mfeespd_status.stdout}}" == 'inactive') or ("{{mfeespd_status.stdout}}" == 'active')
  ignore_errors: true
```

* Referencing the Trellix role, you can see that we want the service 'mfeespd' enabled and running, but that won't be possible on a new system being deployed until tagged on ESS. The task is created so that a variable (mfeespd_status) is registered with the information about its status. The task then sets the values for what is *required* and the *expected* final outcome. In this case, we want mfeespd to be 'enabled' and 'started'. If this were to be ran without the 'when' and its arguments as shown above, the task would fail and stop the playbook on a system that has not been tagged in ESS. The arguments set in the 'when' module and the 'ignore_errors: true' allow for the task to check if the service is enabled and started, then regardless of the result, continue on to the next task. At the end of the playbook there will be a 'PLAY RECAP' and if the system failed these tasks, it would show 'ignored=2'.

## FIPS example

```
- name: Misc - Ensure fips is enabled - V-238363
  shell: ua status | grep fips-updates | awk '{print $3}'
  register: check_ua_active
  changed_when: false
  when: manage_ubuntu_V_238363

- name: Misc - Enable FIPS - V-238363
  command: ua enable fips-updates --assume-yes
  ignore_errors: true
  when: (manage_ubuntu_V_238363) and (check_ua_active.stdout != "enabled") and (check_ua.stdout != "This machine is not attached to an Ubuntu Pro subscription.")
```

* In this instance, we have a task that is checking to see if fips is enabled. Because of licensing, it is expected for this task to fail many times but we want the playbook to continue running and not stop once this failure occurs.