#Tag and push non dockerhub images to Harbor
## Prerequsite:
**Image must be downloaded onto a system that has docker available to be able to push to Harbor**
1. You must login to Harbor on the system that will push the images with your Harbor credentials
    - docker login registry.web.yuma.army.mil
        - Enter your username and password as it prompts for it after the command
1. Transfer images onto the system using something like sftp if the images are locally on your Windows system
1. Once images are on system, you will need to load the images
    - docker load < "image name"
        - example: docker load < backend-v1.0.1.tar
1. Image then needs to be tagged with the correct project on harbor and version
    - running "docker images" will display the images loaded onto the sytem and will give you the name needed when tagging
    - docker tag "image":"version" registry.web.yuma.army.mil/"project"/"image name":"version"
        - example: docker tag gitlab.morsecorp.com:5050/ypg/keystone-services/backend/backend:v1-0-1 registry.web.yuma.army.mil/morse/keystone_backend:v1-0-1
1. Once image has been tagged, it can now be pushed into Harbor
    - docker push registry.web.yuma.army.mil/"project"/"image name":"version tag"
        - example: docker push registry.web.yuma.army.mil/morse/keystone_backend:v1-0-1
1. Image now will be in Harbor and can then be assessed via the ADO pipeline
    - All pipelines > On-Demand > Assessment > Image Assessment to Harbor
1. Run the pipeline after clicking into it
    - The "Source Registry" parameter will be "YPG Harbor" since that is the location in which the image was pushed prior in our steps
    - "Full image repository" will include the project then tagged image name
        - example: morse/keystone_backend
    - "Image tag" will be the version tag we used prior too
        - example: v1-0-1
    - The destination of "Library" or "Lab" will depend on if the image will be used for production or not. In this case, we will be using "Library"
1. Click "run" and the pipeline will begin assessing the image
** NOTE: There will be a step within the pipeline where once assessed, it will need to be approved by CSO prior to it being pushed into Harbor **
1. Once CSO has approved the image and been pushed into Harbor, the image will be available in the "Library" project.