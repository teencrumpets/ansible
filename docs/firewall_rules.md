# Firewall rules summary
We manage all firewall rules as code ONLY FOR our servers that are deployed and managed by code.
Servers that have non-default, custom firewall rules, will need to strictly follow below guidance:

1. You must define an list of firewall rules. They will all follow below syntax (list name and args may differ) 
Note that this is a list w/ one entry. Another entry of a list would be denoted with another hyphen(-):
    ```yaml
    ufw_defaults:
      - order: 200
        rule: 'deny'
        direction: 'in'
        from_ip: 192.168.0.0/25
        proto: 'tcp'
        to_port: 1
    ``` 

The name of the list is dependent on where your are putting your rules. It may not always be ufw_defaults like above.
The possible choices are below in order of priority: 

    - ufw_group 
        - placed under group_vars folder in group file for server (ONLY if rules apply to all servers in that group)
    - ufw_env 
        - placed under environment folder in environment file for server (ONLY if rules apply to all servers on that environment)
    - ufw_host 
        - highest priority (values in this list given most precedence), placed under host_vars folder in file for the server (ONLY if rules apply to that singular host server)
    - ufw_defaults
        - least priority (values in this list given least precedence). placed under defaults folder within the role (ONLY if rules apply to all systems that will run that role in the future)

# Explanation of args:
     - order(REQUIRED): The order in which rule will be applied. Applies rules from least to greatest.
     - rule(REQUIRED): 'allow' or 'deny' traffic, can also 'limit' or 'reject'
     - direction(REQUIRED):
     - from_ip(optional): Will default to all source IPs if omitted 
     - proto(REQUIRED):
     - to_port(optional): Will default to all ports if omitted
        - Optional only if from_ip or to_ip defined
     - to_ip(optional): Will default to all destination IPs, which is only your host because fire-wall is host-based 

# Pipeline
 - These managed firewall rules will be enforced by the baseline role.
 - Pipeline job log will display how the rules were before and after they were changed.