# Trellix Role
*This role is intended to be ran on new systems that need the ESS/Trellix agent installed on.*  

Setting the mode=install installs the agent on the system (RHEL & Ubuntu).
Setting the mode=scan will run an on-demand scan on the sytem, intended to be ran on Docker host systems.
Setting the mode=sync will force the check in process to EPO (cmdagent -p & -c).
Once install mode has been ran, tag system on EPO following the instructions: [Trellix Confluence Documentation](https://confluence.web.yuma.army.mil/pages/viewpage.action?pageId=99647516)  