# Guide to Update Jira and Confluence

## Updating Prep
**Always update Prep before updating prod**
- If at any point Confluence and/or Jira prep does not come back up you will need to do a restore before trying to update again
1. Clone down prod to prep
    - For Confluence:
        - In ADO pipelines->All->On-Demand->Applications->Confluence
    - For Jira:
        - In ADO pipelines->All->On-Demand->Applications->Jira
    - What to select to clone down 
        - Environment: prep
        - Mode: restore
        - Skip Ubuntu and Docker: true
1. Update the variable in the ansible repo in ADO relating to Jira and/or Confluence
    - Create a branch
    - For Confluence:
        - Find the host variable file for docker host prep 
        - Update variable confluence_version to the version you are going to
    - For Jira:
        - Find the host variable file for docker host prep 
        - Update variable jira_version to the version you are going to
1. Create a pull request and coordinate with approver 
    - To update Confluence and/or Jira the branch does not need to be merged to main
    - Reasons why you might not merge the update branch to main before update
        - Have to walk the application up, you would have to update the variable multiple times in this case
        - Updating prep and prod on the same day
1. Run pipeline to update applciation 
    - For Confluence:
        - In ADO pipelines->All->On-Demand->Applications->Confluence
    - For Jira:
        - In ADO pipelines->All->On-Demand->Applications->Jira
1. Once updated log into application using username and password ()
    - For Confluence:
        - Under General Configuration update Server Base URL to correct URL for prep
        - Under Authentication Methods disable 'Prod SAML SSO' and enable "Prep SAML SSO'
        - Update license if needed
    - For Jira:
        - Under General Configuration update Base URL to correct URL for prep
        - Under Authentication Methods disable 'SAML SSO' and enable "Prep SAML SSO'
        - Update license if needed

## Updating Prod
**Always update Prep before updating prod, if you have not done tis look at above instructions**
- If at any point Confluence and/or Jira does not come back up you will need to do a restore before trying to update again
1. Update the variable in the ansible repo in ADO relating to Jira and/or Confluence
    - Create a branch (only if your branch to update prep has been merged)
    - For Confluence:
        - Find the host variable file for docker host 
        - Update variable confluence_version to the version you are going to
    - For Jira:
        - Find the host variable file for docker host 
        - Update variable jira_version to the version you are going to
1. Create a pull request and coordinate with approver 
    - To update Confluence and/or Jira the branch does not need to be merged to main
    - Reasons why you might not merge the update branch to main before update
        - Have to walk the application up, you would have to update the variable multiple times in this case
        - Updating prep and prod on the same day
1. Run pipeline to update applciation 
    - For Confluence:
        - In ADO pipelines->All->On-Demand->Applications->Confluence
    - For Jira:
        - In ADO pipelines->All->On-Demand->Applications->Jira
1. Once updated log into application
    - For Confluence:
        - Ensure update went smoothly
    - For Jira:
        - Under Indexing run Full re-index
        - Ensure update went smoothly 

## Migrating to Different Database
**Excluding step 1 ensure these steps work on a non-production environment before attempting migration on prod** 
1. Schedule a maintenance time 
1. Backup Jira/Confluence within application
    - Jira and Confluence have a backup site option within the application. Run this during the scheduled maintenance time
    - Confluence has option to backup with attachments, make sure to select that option
    - Download the zip file given after the backup is done.
1. Run the pipeline that backs up the application
    - Allows for quicker option of reverting if you need to backout of migration
1. Merge branch that has changes for database to main
1. Remove current instance of Confluence
    - docker compose down
    - docker volume rm (all confluence volumes)
1. Deploy new instance
1. Setup and restore the site. 
    - Both Jira and Confluence have options to restore from the backup done in the previous step
    - Find the option to restore confluence after initial setup
    - Jira gives an option to restore during initial setup
1. Ensure there are no errors, and connection between Jira and Confluence is fine

### Reverting After Failed Migration
1. Revert changes made to main branch
1. Onces changes have been reverted from main branch run pipeline to restore application.

## Important Certificates to add to the Truststore
keytool -printcert -sslserver marketplace.atlassian.com:443 -rfc >> marketplace.atlassian.com.crt
keytool -printcert -sslserver marketplace-cdn.atlassian.com:443 -rfc >> marketplace-cdn.atlassian.com.crt
keytool -printcert -sslserver api.media.atlassian.com:443 -rfc >> api.media.atlassian.com.crt