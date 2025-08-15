# Initial Configuration
1. Update user info
    ```
    git config --global user.name "FIRST_NAME LAST_NAME"
    git config --global user.email "MY_NAME@example.com"
    ```
1. Disable SSL Verifiaction
    ```
    git config --global http.sslVerify false
    ```

1. Update Token HTTP header
    ```
    MY_PAT=<PAT HERE>
    B64_PAT=$(printf "%s"":$MY_PAT" | base64)
    git config --global http.extraHeader "Authorization: Basic ${B64_PAT}"
    ```

# Branches
### Create a new branch and publish to origin

```
git checkout -b <branch_name>
git push --set-upstream origin <branch_name>
```

### Branch merge updates
* When working on a branch, there may be updates/changes done to the main branch so a merge must be done to prevent merge conflicts on the branch you are working on
* Switch to main branch
```
git pull
```
* This will pull any updates/changes done to the main branch since you have been working on your branch. 
* You then want to switch to the branch you are working on and run:
```
git merge main <name of working branch>
```