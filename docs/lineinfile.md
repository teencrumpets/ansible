# Introduction

Style and convention guide for the [lineinfile module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/lineinfile_module.html).

Typically used for adding or removing single lines from a config file.

# Usage

The following example tasks can be referenced when using lineinfile module.

```
- name: Configure apt to use IPv4 only
  lineinfile:
    path: /etc/apt/apt.conf.d/98-force-ipv4
    line: 'Acquire::ForceIPv4 "true";' 
    regexp: '(?i)ForceIPv4'
```
```
- name: Overwrite log permissions
  lineinfile:
    path: /usr/lib/tmpfiles.d/00rsyslog.conf
    line: 'z /var/log 0750 root syslog -'
    state: present
    regexp: '^(?i)z\s+\/var\/log\s+'
  when: manage_ubuntu_V_238340
```

***

There should always be a verify task that runs after every lineinfile operation to verify that the line is present in the file exactly once. In instances where you expect the line to be there more than once or absent, the verify task must be modified.

The following example task can be referenced, and will fail if the line shows up 0 or 2+ times.
```
- name: Verify apt IPv4 config
  replace:
    path: /etc/apt/apt.conf.d/98-force-ipv4
    regexp: '(?i)ForceIPv4'
    replace: ''
  check_mode: yes
  register: diff
  failed_when: diff.msg != "1 replacements made"
  ignore_errors: true
  changed_when: false
```