# Introduction

Style and convention guide for the [replace module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/replace_module.html).

Typically used for adding or removing multiple lines from a config file, or doing replacements on a subset of an existing , without overriding everything.

# Usage

The following example tasks can be referenced when using lineinfile module.

This example uses a capture group, and insterts a value after the first group.
```
- name: Setting unrestircted Grub menu options
  replace:
    path: '/etc/grub.d/10_linux'
    replace: '\1  --unrestricted"'
    regexp: (?i)^(class\s*=(?!.*--unrestricted).*)(\"$)
  notify: Update Grub
  when: manage_ubuntu_V_238204
```

```
- name: Clean up extra entry for pam_pwquality
  replace:
    path: '/etc/pam.d/common-password'
    regexp: '^(?!password\s|^#|^\s).*'
    replace: ''
  when: manage_ubuntu_V_238228
```

***

There should always be a verify task that runs after **most** replace operations to verify that the line is present in the file exactly once. In instances where you expect the line to be there more than once or absent, the verify task must be modified.

 The following example task can be referenced, and will fail if the line shows up 0 or 2+ times.

```
- name: Verifying patch for 10_linux file
  replace:
    path: '/etc/grub.d/10_linux'
    regexp: '^(?i)class\s*=\s*"'
    replace: ''
  check_mode: yes
  register: diff
  failed_when: diff.msg != "1 replacements made"
  ignore_errors: true
  changed_when: false
  when: manage_ubuntu_V_238204
```