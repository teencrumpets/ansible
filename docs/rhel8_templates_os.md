## Steps on creating Rhel 8 Template 
## Deployment and OS  Install
1. Find Stig Rhel8 Template and deploy new server from there, the folder it goes in is UCS-Prep as that is where templates are kept currently. For more details on deploying a server you can find instructions here (skip to virtual section):  https://confluence.web.yuma.army.mil/display/NST/Build+Server
It should start powered off but turn off if necessary.
  
2.  Once virtual machine(VM) is created, there should be an "Edit Settings" option under the "VM Hardware" section. In there add an CD/DVD Drive from the "Add New Device" dropdown. It should be configured as "Datastore ISO file"  
3. You may need to put an iso in the datastore if the one you need is not present. To do so follow steps 3-5, otherwise skip  
4. Go to the datastore tab, which is third icon from first on the right sidebar and select the one named VMware-ISO  
![alt text](pics/vmware_datastore.png)  
5. You should see a selection of folders. Linux Datastores for templates are generally stored under the Linux folder, where there are folders for each distribution. If you are uploading an new distribution, select New Folder. If not select upload file **ONCE** you have clicked and entered into the correct folder, for our case it is Linux/RHEL8, and upload your ISO from your computer. An ISO is often downloaded from the official distributor's website.  
6. In VM console, there should be dropdown labeled "VMRC" where you can go to Removable Devices and attach your download  (ISO) to the device you added in the step 2.  
7. We need to boot the VM from the iso instead of network booting, any of the following options will work, choose easiest for you:  
    * **BEFORE** turning VM on, Click the box that forces entry into EFI setup screen. Can do this under "Edit Settings" menu 
    * Can also power on the VM and **IMMEDIATELY** press escape key repeatedly until the boot menu appears. Can add time to boot delay to help with this option in order to have more time to hit escape. This can be found under the "Edit Settings" menu  
    *   **BEFORE** turning VM on, disconnect the network adapter from VLAN 630 to avoid automatically network booting. Can do this under "Edit Settings" menu. This option requires you to reattach network adapter to VLAN 630 after installing OS (before generalization steps)  
8. Power On VM (if not already running)and navigate to boot menu (may need to restart VM if your VM was already running). Select the device you put your download on (SATA CD DRIVE). On next screen, select to install RHEL8    

9. After it verifies and installs everything, it should
restart and go to setup page
10.  Follow link on instructions on how to do initial setup of RHEL8, inluding partition: https://confluence.web.yuma.army.mil/display/NST/Deploy+RHEL+8  

11. Afterwards, it should start installing and when done, it should give option to reboot now, select it
12. Remove CD drive you attached earlier, can do so by navigating to the CD Drive the same way you navigated to it to attach the ISO in a earlier step but this time hover over your attached device (CD Drive) and click the settings sub-option where it should give option to remove device
## Customization  
13.  Change network-scripts for ens192  
    
      ```
        sudo vi /etc/sysconfig/network-scripts/ifcfg-ens192
      ```
    
      Then configure it as follows (you will see a UUID line about third from the bottomost line on your screen that will be cleared out as shown below) then save and exit:
    ![alt text](pics/template_help2.png)

## Generalization  
14. Log in server and follow generalization steps (template must be generalized **EVERY** time it is changed): 
 Note: If you removed the network adapter in a previous step, you must reattach to VLAN 630  

* Subscribe with rhel acoount (make one first if you don't have one) and put in the account credentials:
```
  subscription-manager register
```
*  Update server and perform other generalization steps:
```
  dnf upgrade
```
```
  dnf update
```
    rm -rf /etc/ssh/ssh_host_*
```
    hostnamectl set-hostname localhost.localdomain
```

    rm -rf /etc/udev/rules.d/70-*
```
    chmod 777 /etc/machine-id
```
```
"vi /etc/machine-id" to edit and remove the line in it, save and exit
``` 
```
chmod 444 /etc/machine-id 
```   
   Unsubscribe system with following commands:  
  ```
        subscription-manager unregister
        subscription-manager remove --all
        subscription-manager clean
  ```
    

15.  Power off VM, remove network adapter and right click the VM name from the sidebar, click the template option and convert to template. 