# Initial VM Deployment and OS  Install
These steps are done ***ONLY*** when initially creating a brand new template.

1. Deploy a VM from the STIG template.
    - Reference these [instructions](https://confluence.web.yuma.army.mil/display/NST/Build+Server) if needed
    
    - Make sure VM is powered off

    - Make sure the network is not set to the 629 or 630 subnet so that it doesn't network boot when powered on
  
1.  Attach the Ubuntu ISO
    - Click `Edit Settings` option under the `VM Hardware` section
    
    - Add a CD/DVD Drive from the `Add New Device` dropdown
    
    - Attach Ubuntu ISO file either locally or from `Datastore ISO file` option
    
    - You may need to put an iso in the datastore if the one you need is not present

    - Check the box to `Force EFI` setup screen at next boot

1. Power on the VM and boot from the ISO
    - Navigate to boot menu from EFI setup screen
    
    - Select the device you put your download on
      - ex `SATA CD DRIVE`

1. Start the Ubuntu install wizard
    - Select `Install Ubuntu Server` option
    
    - When prompted to update to new installer, choose to continue **WITHOUT** updating as it is likely we don't support the newest version  

    - There are a few screens prompting for configuration options
      - In MOST cases, the default should be left selected
      
      - Click continue until you see config options for the disk and partition, select `Custom storage layout`

1. Custom storage layout:
    - Set primary disk as boot device
      - Under available `Devices` select `80GB` local disk
      
      - Select `Use As Boot Device` option

      - This will automatically create the required `/boot/efi` filesystem
    
    - Create primary volume group
      - Under the same `80GB` local disk select `free space`

      - Select `Add GPT Partition` option
        - Size: Leave blank to consume remaining free space
        
        - Format: `Leave unformatted`
      
      - Select `Create volume group (LVM)` option
        - Name: `vg_primary`

        - Devices: Check the partition you just created
    
    - Create STIG required `/var/log/audit` filesystem
      - Find the volume group you created under `Available Devices` and under that select `free space`
      
      - Select `Create Logical Volume`
        - Name: `lv_audit_log`

        - Size: `2`

        - Format: `ext4`

        - Mount: `/var/log/audit`                                                

    - Create root filesystem
      - Find the volume group you created under `Available Devices` and under that select `free space`
      
      - Select `Create Logical Volume`
        - Name: `lv_root`

        - Size: Leave blank to consume remaining free space

        - Format: `ext4`

        - Mount: `/` 

1. Profile Setup
    - Your name: `ypgansible`

    - Your server's name: `template`

    - Pick a username: `ypgansible`

    - Choose a password: get password from password vault under Ansible

1. SSH Setup
    - Check the `Install OPENSSH server` option only

1. Continue to finish the Ubuntu installation wizard

1. Remove CD drive you attached earlier

1. Perform customization steps outlined below

# Customization Steps
These are YPG specific customizations made to the template
  - All changes should be recorded here so that new templates can be created with all the same customizations
  - Each customization only needs to be done once

---

1. If updating an existing template, convert template to a VM and power on

1.  Update netplan
      - Open netplan configuration file
        ```
        sudo vi /etc/netplan/00-installer-config.yaml
        ```
      - Force netplan to identify to DHCP server with MAC address instead if client ID by adding `dhcp-identifier: mac` line
      
      - After adding the file should look similar to this: (ens may have different number, use command ip link to verify yours)
        ```
        network:  
          ethernets:
            ens224:  
              dhcp4: true
              dhcp-identifier: mac
          version: 2
        ```

1. Disable and remove unattended upgrades as they can conflict with our scheduled updates
    ```
    sudo systemctl disable --now unattended-upgrades.service  
    sudo apt remove unattended-upgrades   
    ```

1. Perform generalization steps


# Generalization Steps
These steps need to be perform **AFTER EVERY TIME** customizations are made to the template.

---

1. Ensure the the network is connected to 630 subnet

1. Run system updates
    ```
    sudo apt update && apt -y upgrade && apt -y autoremove && apt clean
    ```

1. Run the following commands:
    - Remove machine ID
      ```
      sudo truncate -s0 /etc/machine-id
      sudo rm /var/lib/dbus/machine-id
      sudo ln -s /etc/machine-id /var/lib/dbus/machine-id
      ```

    - Clean cloud-init
      ```
      sudo cloud-init clean
      ```

    - Clear history
      ```
      sudo history -c
      history -c
      ```

1. Power off VM

1. Convert VM to template with the name `template_ubuntu_24.04`
