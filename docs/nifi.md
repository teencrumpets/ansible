# Running NiFi deployment pipeline
* **Name of Server**: This is where you would enter the system name (in caps) of the system you want NiFi deployed on
* **IMPORTANT NOTE: The manager needs to be deployed before the node deployment.**
* **Mode**: You choose the "deploy_manager" option if you want to deploy a NiFi manager for the cluster
* **Name of nifi node/manager**: the name of the node or manager that would be deployed. Managers have no number (nec, dpb) while nodes are numbered (nec1, nec2, dpb1, dpb3)

# Extra variables
* Extra variables are variables set in the role to specify portions within the role itself. For example, the nifi role can specifically deploy nec node 1 by using the variable "nifi_manager", "nifi_node" and "mode". "mode" is used to 
specify whether a manager or a node will be deployed with the role which also *requires* the use of the variable "nifi_manager" or "nifi_node". "nifi_manager" currently has the two possible variable values of "deploy_manager" or
"deploy_node". "nifi_manager" and "nifi_node" have different options and may change with time since these variables reference the dictionary items in the "nifi_managers" and "nifi_nodes" lists.
* The example below runs the nifi role but deploys a nifi manager container for the nec. The "nec" part is set in the nifi_managers along with "dpb" and other organizations in the future.
* The null portion of the ansible command must be present so the role only runs the needed mode (deploy manager or deploy node)

```
ansible-playbook site.yml -e "HOSTS=all role=nifi mode=deploy_manager nifi_manager=nec nifi_node=null ENV=dev fast=true" --ask-vault-pass
```

* The example below runs the nifi role and deploys node dpb2 which are set in the nifi_nodes list.
```
ansible-playbook site.yml -e "HOSTS=all role=nifi mode=deploy_node nifi_node=dpb2 nifi_manager=null ENV=dev fast=true" --ask-vault-pass
```
* Currently there are only the two modes "deploy_manager" and "deploy_node" available when using the "mode" variable. For the "nifi_manager" variable, you can use "nec" and "dbp" for now but can be expanded by adding to the 
"nifi_managers" list. nec1, nec2, dpb1, dpb2 are the examples of what would be entered for "nifi_node" when the "deploy_node" mode option is chosen and this list can also be expanded. These lists are the variables that the role 
references dependent on if you choose the "deploy_manager" or the "deploy_node" mode. Below is the current list of variables used for both the nifi_managers and the nodes.

```
nifi_managers:
  - nec:
    nifi_manager_dir: nifi_nec_manager
    zk_host_name: nec_zookeeper
    zk_version: latest
    host_port: 2182
    nifi_net: nec-nifi-net
    nifi_flow_storage: nec_nifi_flow_storage
  - dpb:
    nifi_manager_dir: nifi_dpb_manager
    zk_host_name: dpb_zookeeper
    zk_version: latest
    host_port: 2181
    nifi_net: dpb-nifi-net
    nifi_flow_storage: dpb_nifi_flow_storage
```

```
nifi_nodes:
  - nec1:
    nifi_node_dir: nifi_nec_node
    host_name: nifi-nec1.yuma.army.mil
    nifi_port: 7954
    container_port: 7954
    cluster_port: 8445
    socket_port: 5450
    zk_connection: nec_zookeeper:2182
    nifi_sensitive_key: '{{ nifi_nec1_sensitive_key }}'
    nifi_single_username: nec_user
    nifi_single_userpw: '{{ nifi_nec1_usercred_pw }}'
    nifi_net: nec-nifi-net
    nifi_volume: nec_nifi_volume
    nifi_db: nec_nifi_db
    nifi_flowrepo: nec_nifi_flowrepo
    nifi_contentrepo: nec_nifi_contentrepo
    nifi_provrepo: nec_nifi_provrepo
    nifi_state: nec_nifi_state
    nifi_logs: nec_nifi_logs
    nifi_configuration: nec_nifi_configuration
    nifi_store: nec_nifi_store
    nifi_keystore: nec_keystore.p12
    nifi_keystore_pw: '{{ nifi_nec1_keystore_pw }}'
    nifi_privkey_pw: '{{ nifi_nec1_keypw }}'
  - dpb1:
    nifi_node_dir: nifi_dpb_node1
    host_name: nifi-dpb1.yuma.army.mil
    nifi_port: 9449
    container_port: 9449
    cluster_port: 6445
    socket_port: 5454
    zk_connection: dpb_zookeeper:2181
    nifi_sensitive_key: '{{ nifi_dpb1_sensitive_key }}'
    nifi_single_username: dpb_user
    nifi_single_userpw: '{{ nifi_dpb1_usercred_pw }}'
    nifi_net: dpb-nifi-net
    nifi_volume: dpb1_nifi_volume
    nifi_db: dpb1_nifi_db
    nifi_flowrepo: dpb1_nifi_flowrepo
    nifi_contentrepo: dpb1_nifi_contentrepo
    nifi_provrepo: dpb1_nifi_provrepo
    nifi_state: dpb1_nifi_state
    nifi_logs: dpb1_nifi_logs
    nifi_configuration: dpb1_nifi_configuration
    nifi_store: dpb1_nifi_store
    nifi_keystore: dpb1_keystore.p12
    nifi_keystore_pw: '{{ nifi_dpb1_keystore_pw }}'
    nifi_privkey_pw: '{{ nifi_dpb1_keypw }}'
  - dpb2:
    nifi_node_dir: nifi_dpb_node2
    host_name: nifi-dpb2.yuma.army.mil
    nifi_port: 9450
    container_port: 9450
    cluster_port: 6445
    socket_port: 5455
    zk_connection: dpb_zookeeper:2181
    nifi_sensitive_key: '{{ nifi_dpb2_sensitive_key }}'
    nifi_single_username: dpb_user
    nifi_single_userpw: '{{ nifi_dpb2_usercred_pw }}'
    nifi_net: dpb-nifi-net
    nifi_volume: dpb2_nifi_volume
    nifi_db: dpb2_nifi_db
    nifi_flowrepo: dpb2_nifi_flowrepo
    nifi_contentrepo: dpb2_nifi_contentrepo
    nifi_provrepo: dpb2_nifi_provrepo
    nifi_state: dpb2_nifi_state
    nifi_logs: dpb2_nifi_logs
    nifi_configuration: dpb2_nifi_configuration
    nifi_store: dpb2_nifi_store
    nifi_keystore: dpb2_keystore.p12
    nifi_keystore_pw: '{{ nifi_dpb2_keystore_pw }}'
    nifi_privkey_pw: '{{ nifi_dpb2_keypw }}'
```

* If a new organization needs to be added, you then would ensure that each variable used with the other organizations are included in the new list as well but still using a similar setup. Remember that ports need to be unique too
for each organization. The indentation matters for the lists to the spacing needs to be kept the same too. 
* IMPORTANT NOTE: For the nifi_nodes list, the port used for the "nifi_port" and the "container_port" need to be the same in order for the containers to communicate with one another. 
* IMPORTANT NOTE: The variable set for "zk_connection" under the nifi_nodes list needs to match the "host_name" used in the "nifi_managers" list without the colon and port of course. 
* Below a template of the variables for each list will be included where you just need to copy and replace with your values. Remember that the line with the hyphen (-) is the name of the list. I included notes for the variables below
followed by a pound sign (#).

```
nifi_managers:                                          # This specifies that these lists are for the nifi managers
  - mw:                                                 # This is the name of the list that is used by the extra variable "nifi_manager" and "mode"
    nifi_manager_dir: nifi_mw_manager                   # This is the title that will be used for the folder in /opt/compose/
    zk_host_name: mw_zookeeper                             # This variable needs to match the host_name used under the nifi_nodes list before the colon and port number
    zk_version: latest                                  # Can be set at a specific version of the container image
    host_port: 2748
    nifi_net: mw-nifi-net                               # This is the name of the network that the compose file creates for the cluser of that organization and must be the same as the one used in the "nifi_nodes" list
    nifi_flow_storage: mw_nifi_flow_storage             # Volume name for flow storage

nifi_nodes:                                             # This specifies that these lists are for the nifi nifi_nodes
  - mw:                                                 # This is the name of the list that is used by the extra variable "nifi_node" and "mode"
    nifi_node_dir: nifi_mw_node                         # Variable for the name that will be used for the folder in /opt/compose/
    host_name: nifi-mw1.yuma.army.mil                   # This should be the "title" used when doing the CSR (certificate sign request), make sure same layout is used
    nifi_port: 6969                                     # This variable value needs to be unique to its organization but needs to match the value of the below variable "container_port"
    container_port: 7954
    cluster_port: 4200                                  # Unique port to its organization
    socket_port: 5454                                   # Unique port required for multiuser authentication
    zk_connection: mw_zookeeper:2183                    # The "mw_zookeeper" portion of the variable value needs to match the "host_name" variable used above in the "nifi_managers" list and the port number match "host_port" in "nifi_managers" list
    nifi_sensitive_key: '{{ nifi_mw_sensitive_key }}'  # Sensitive key set in docker compose file, value stored in ansible-vault
    nifi_single_username: mw_user                      # Username set in docker compose file
    nifi_single_userpw: '{{ nifi_mw_usercred_pw }}'    # User from above password set in docker compose file, value stored in ansible-vault
    nifi_net: mw-nifi-net                               # This is the name of the network that the compose file uses for the cluser of that organization and must be the same as the one used in the "nifi_nodes" list
    nifi_volume: mw_nifi_volume                         # Volume variable name for nifi data /opt/nifi/filedata
    nifi_db: mw_nifi_db                                 # Volume variable name for nifi database /opt/nifi/nifi-current/database_repository
    nifi_flowrepo: mw_nifi_flowrepo                     # Volume variable name for nifi flow /opt/nifi/nifi-current/flowfile_repository
    nifi_contentrepo: mw_nifi_contentrepo               # Volume variable name for nifi content repo /opt/nifi/nifi-current/content_repository
    nifi_provrepo: mw_nifi_provrepo                     # Volume variable name for nifi provenance /opt/nifi/nifi-current/provenance_repository
    nifi_state: mw_nifi_state                           # Volume variable name for nifi state /opt/nifi/nifi-current/state
    nifi_logs: mw_nifi_logs                             # Volume variable name for nifi logs /opt/nifi/nifi-current/logs
    nifi_configuration: mw_nifi_configuration           # Volume variable name for nifi configuration files /opt/nifi/nifi-current/conf
    nifi_store: mw_nifi_store                           # Volume variable name for nifi store /nifi-store
    nifi_keystore: mw_keystore.p12                      # This references the keystore file that is required in order for SSL to work on the cluster
    nifi_keystore_pw: '{{ nifi_mw1_keystore_pw }}'      # Keystore password stored in ansible-vault
    nifi_privkey_pw: '{{ nifi_mw1_keypw }}'             # Private key password stored in ansible-vault
```