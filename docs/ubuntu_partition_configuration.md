# Manual Ubuntu OS Parition Configuration
* When installing the Ubuntu OS manually on a server the following steps need to be taken to partition correctly
* The disk housing the Operating System:
    * Go to OS disk
    * Choose disk as boot device
    * Click free space under the OS disk
    * Create gpt partition
    * First need to create /var/log/audit partition so name it accordingly
    * 2G for the partition size
    * ext4 for format
    * /var/log/audit for mount point
    * Go to free space under the os disk
    * Leave space blank to use up the rest of the disk
    * ext4 format
    * Mount point /
