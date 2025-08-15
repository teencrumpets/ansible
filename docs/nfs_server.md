# NFS_Server Host Variable Documentation


Below is an example of what the host variable should contain. These variables are to control entries in the /etc/export files.

**path** - Path to be exported

**clients** - List of client IP's allowed to connections

**options** - NFS options to use

**enabled** - If set to true, it will create the entry in /etc/export. False will remove it.
```
---
nfs_exports:
  - path: /export/backups
    clients:
      - 6.2.4.0/26
      - 6.2.11.0/26
    options:
      - rw
      - sync
      - no_subtree_check
    enabled: true
  - path: /export/newpath
    clients:
      - 6.2.4.0/26
      - 6.2.11.0/26
    options:
      - rw
      - sync
      - no_subtree_check
    enabled: false
```