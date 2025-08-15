# Regular Expressions
* When making regular expressions make them as general as possible
```
Use ^(?i)PASS_MIN_DAYS instead of ^(?i)PASS_MIN_DAYS 1
```
* To create more complex regex use: https://regex101.com/
* There are also examples of more complex regex in the playbooks

* Example of how to use regex to add to a line without replacing anything else in the line
```
- name: Setting unrestircted Grub menu options
  replace:
    path: '/etc/grub.d/10_linux'
    replace: '\1  --unrestricted"'
    regexp: (?i)^(class\s*=(?!.*--unrestricted).*)(\"$)
  notify: Update Grub
  when: manage_ubuntu_V_238204
```