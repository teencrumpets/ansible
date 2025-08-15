# About Datahub
- DO NOT RESTART THIS APP MANUALLY
    - For more information read dependencies section
- Datahub is an application that was developed by the SEG to get data from file shares into the Data Mesh.
- Modes:
    - Deploy
        - Will stand up a new instance of dathub as long as all dependencies have been met. Also inserts Datahub service file in Nginx Configuration, so if the service file needs to be replaced run this role. If this role is ran on an existing instance of datahub it will update the compose and service file, but will not restart the application. 
        - If you need to run this mode on an existing instance ensure nothing has changed in the compose file. If there is a change, could be a potential issue when Datahub needs to be brought down.
    - Update
        - Updates Datahub by updating compose file if there's changes, and restarting application. This is disruptive, let SEG know if this is being done on production.
        - Currently testing updates using prep Datahub. All instances of Datahub should be using different database connections.
        - When updating check with SEG(currently Mathias) to see if compose file changed. If it did latest version should be on Portainer. Check to see if all additions to the compose are necessary.
    - Bounce
        - Restarts the application. This is disruptive, let SEG know if this is being done on production.

## Dependencies
- Nginx
    - Must have Nginx setup before deploying
    - Requires a service file to be created for Nginx. This is done in the Datahub role through the deploy mode
    - Datahub now has its own template for nginx, because of api location. Eventually want to edit the service template to be able to include more locations than just the root
- Keycloak
    - Must have Keycloak setup before deploying
    - Setup needed for deployment 
        - Realm Authentication
        - Client
- Override File
    - Datahub Role stores all secrets in an override file that gets deleted after the containers are up. The role will take care of this, but if you try to manually restart Datahub without running the role Datahub will error.

## Variables
### Environment Variables
Located in the Vaults
- All variables with DB_Secret
  - Password for SQL account being used for that database
```YAML
DATA_HUB_DB_SECRET:
WHSE_DB_SECRET:
ORG_DB_SECRET:
RTSS_DB_SECRET:
SSIS_DB_SECRET:
SHARE_PASSWORD: Password for file share service account
CLIENT_SECRET: Secret found in Keycloak client credentials
```

### Host Variables

```YAML
datahub_url: FQDN of Dathub
datahub_service_file: Name of service file that gets placed in Nginx
AUTHORITY: URL for keycloak realm Datahub client is in
CLIENT_ID: Datahub Client name in Keycloak
datahub_nginx_server: Server Nginx is on
SHARE_USER: Service account used to mount file shares
```

SQL Connections
- For Each
    - Name: Database name
    - Host: Connection String
    - User: SQL Account
```YAML
DATA_HUB_DB_NAME: 
DATA_HUB_SQL_HOST:
DATA_HUB_DB_USER:
WHSE_DB_NAME: 
WHSE_SQL_HOST:
WHSE_DB_USER:
ORG_DB_NAME:
ORG_SQL_HOST:
ORG_DB_USER: 
RTSS_DB_NAME:
RTSS_SQL_HOST:
RTSS_DB_USER:
SSIS_DB_NAME: 
SSIS_SQL_HOST:
SSIS_DB_USER:
```

### Default Variables 

```YAML
compose_path: Path to compose file
harbor_url_for_datahub: URL where image for Datahub Web is in Harbor
datahub_version_tag: Tag of Datahub Web in Harbor
harbor_url_for_hangfire: URL where image for Hangfire is in Harbor
hangfire_version_tag: Tag of Hangfire in Harbor
```

Potential Host Variables
```YAML
datahub_ports: Port that Datahub web will use on server
datahub_container_name: Container name for Datahub
hangfire_container_name: Container name for Hangfire
```

File share paths
    - Mounted in Hangfire container
```YAML
SHARE_DATA_HUB:
SHARE_DPB:
SHARE_AI:
```

## Pipelines
- Datahub
    - Located in On-Demand/Applications
    - Must know the server the Datahub instance you want to run the pipeline against
    - Ensure that the host variables have been set correctly
    - Can set off Deploy, Bounce, or Update

## Known Bugs
### Multiple Instances of Hangfire
- Currently having multiple instances of Hangfire can cause issues
    - Before deploying another instance ensure:
        - Hangfire SQL connections are unique to that instance
        - If not a production instance give DB Admin script to run on the databases that were setup for your instance
          ```SQL
          DELETE FROM [Hermes].[Profile]
            GO

          DELETE FROM [Worker].[WorkerJob]
            GO

          DELETE FROM [Hermes].[FileUploadMetadata]
            GO
          ```

## Other Suggested Documentation
- application_delivery_controller.md