# Updating Linux

## Update Linux Variables
| Name   |      Found      |  Value |
|----------|:-------------:|------:|
| allow_reboot |  default vars | Default: true |
| auto_update |  default vars <br> host vars| Default: true|
| clean_inventory |  group vars (all) | Default: false|

## Opting out of Automatic Updates
* If you set auto_update to false in a host variable file this will not allow the server to recieve updates automatically when the scheduled baselines run.

## Removing the inventory files
* If you need the inventory files removed from a server they were placed on, set variable clean_inventory to true

## Upcoming Features of this Role
* Ability to run role on RHEL 8