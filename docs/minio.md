# Minio Role
Minio has one mode: update
Can run role with fast=true to skip running ubuntu and docker role

## Running Minio
Running minio without a mode will deploy minio. If it is ran this way, and minio was already deployed it will update the docker compose file if the file was changed, but it won't stop the service.

## Update Mode
Running minio with update mode will update minio for a change made to the docker compose file.