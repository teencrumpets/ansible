# Introduction
The playbook automates deployment of fortify ssc software.   
# Steps in playbook for fortify deployment  
**Note** This does not explain every task in the playbook, only gives an overview of the main tasks. 
1. Install openjdk 11 as Java is a prerequisite for Tomcat 9 

2. Create system group and user called "tomcat" with the user having no login shell w/ home directory "/opt/tomcat 

3. Downloads most current tomcat 9 from the web, as it is prereq. for fortify ssc 

4. removes old ssc.war (if one exists)in case previous step downloads a newer version of tomcat  
5. Extracts tomcat download into the opt/tomcat and renames /opt/tomcat/apache-_download number_ to /opt/tomcat/version to hide the actual version 

6. Deletes the old tomcat version folder if applicable, then copies the tomcat.service file 

7. set new firewall rule to allow port 8080, then create fortify mount directory to get ssc.war from the nec share, then removed the mounted directory 

8. Also implements many stig compliance rules. 

The audit task (last of stig_compliance) fails on consecutive runs when conditional statements are not there because it throws error if rule already exists.  Conditionals for the task check for error containing "rule exists" and will display "ok" status instead of failing. Displays 'changed" status when output is empty, which indicates the rule has been newly added. Failed status if anything else. 

Also, the ubuntu role that this one imports changes /etc/login.defs in a way that does not allow tomcat to start, so there is a task at the beginning of the fortify role to erase that change and another one towards the end to put it back. 

**IMPORTANT**: updating tomcat happens on each playbook run based on what is on tomcat's source page. It uses curl to get tomcat's source page, then grep to find where the latest version and tar download of tomcat 9 is at. It then pulls this info. in variables and uses it the in subsequent tasks to set up tomcat and fortify ssc. IF tomcat's source page url OR it's organization of the elements on the source page change, the curl and grep methods used to get the info. into variables may need to be changed. So if an error occurs shortly after the tasks where the info. is pulled, it may be due to the task being unable to pull the info. due to the aforementioned changes in the previous sentence. These tasks "get current tomcat download" and "get current tomcat version" will always report "ok" for idempotency reasons when running in semaphore, so it is important to check that they are actually working if an unknown error occurs. The simplest way to check if these tasks are working appropiately is to use Ansible's debug module to print the value of the variable used in the task. If correct version or download is not given, you may need to modify the curl and grep mewthods as mentioned earlier.  
**IMPORTANT**: if a newer version of tomcat ever modifies the amount of hosts or connectors, some of the stig compliance tasks revolving around hosts and connectors may need to be adjusted. Right now, the stig compliance rules only work for the default amount of connectors and host elements as given by tomcat now, this should rarely if ever change in the future.  
**IMPORTANT**: The "change server.info" and "change server.number" tasks near the bottom of the playbook contain random input. Those letters and numbers after "server.info=" and "server.number=" are completely random. This is to hide the default configuration that gives the tomcat version and info that the server is currently running. According to stig, a user should not be able to see the accurate server.info or server.number. These random inputs have no significance outside of hiding the real information and can be modified to another random or generic input if required. 

# Steps for setting up inital login 
1. First page will ask for token number. This is located in init.token on your fortify ssc server in the opt/tomcat/.fortify/ssc folder. If you did not set up fortify ssc using the playbook task or instructions, it may be somewhere else. Paste token and click to continue. 
**IMPORTANT:** If you ran the playbook as is, when you try to click to the next page after pasting the token, it will not move forward due to the stig setting that secures cookies. This happens if the server has not been put behind the F5 yet. 

2. The next page asks for your fortify license, which should be in the SSC_Fortify_Application folder. Upload and continue. 

3. The next page asks for your url for fortify ssc, which is the url you plan to use to access fortify. Then it asks if you want to enable http host header validation or global search. Both boxes should be left unchecked. 

4. Next is setting up the database, the database type should be sql server as that is what we currently use, the username will be the name of the service account for this database, and the password will be the service acount's password. The jdbc url is a string that connects to the database. Below is a generic example:

  jdbc:**sqlserver**://**_hostname_**:**_port_**;database=**_db name_**;encrypt=false;sendStringParametersAsUnicode=false

 
The strings in bold should be changed to fit your case.

5. It then asks for some connection settings: As of currently, we have max idle and active connections set to default , and the default max wait time as well. 
6. If its your first time deploying, you will go to your SSC_Fortify_Application folder and click the sql folder. Then click the folder with the name of the database  type you are using, for example, click sqlserver if you are using sqlserver. Then grab the create-tables.sql script and run it against the database you connected earlier. For existing ssc deployments, there is a download script button on the web page. Download and run it against the database.  
7. The last step is seeding, where you browse the SSC_Fortify_Application folder for the process seed bundle **first** and then click seed database, then get the report seed bundle **second** and seed it, and **lastly**, get the PCI bundle and seed it. After successfull seeding all three, you can click next, where you finish the setup and then close current browser, as well as restart your fortify ssc server.