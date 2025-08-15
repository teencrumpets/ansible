#Docker default & host daemon variables
* There are two separate variables when it comes to the docker daemon.json file being created. The host that the role is being ran on needs to have its own variable if there are specific daemon customizations needed on it. 

* On the host, the variable is named: 
```
host_docker_daemon:
```

* The default role variable is named: 
```
default_docker_daemon:
```

* The docker host role takes the host and default variable, and adds them together as one variable.

```
- name: add lists together
  set_fact: 
    merged_daemon_list: "{{ default_docker_daemon | combine(host_docker_daemon) if host_docker_daemon is defined else default_docker_daemon }}"

- name: Write to daemon.json the configurations needed
  copy:
    dest: /etc/docker/daemon.json
    content: "{{ merged_daemon_list | to_nice_json }}"
```

* The if else statement makes it so that if a host_docker_daemon does not exist, the task can continue to run