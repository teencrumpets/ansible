# Introduction 
Repository for configuration-as-code; leveraging Ansible engine and GitOps best practices. **For new users, see the getting started document in the Documentation directory.**

* **Primary POC:**
    - `Brett Stephens`
* **Alternate POCs:** 
    - `Alyssa Rice`
    - `O'Darrius Caldwell`

# Contribution Rules
Read all of these rules **before contributing** to this project.
* Documentation for style and usage of Ansible modules can be found in the documentation folder and should be followed.
    * Contributions to documentation are welcome and in some cases expected to contributing team members.
    * This documentation is meant to help fellow team members as well as your future self needing to interact with this code base so don't be shy leaving it better than you found it.
* Playbooks managing infrastructure as code (IaC) must be **declarative** with **idempotent** tasks.
    * For more information, reference the [Ansible glossary](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) for these terms.
* All code in this project should be as **consistent as possible for ease of use, reusability, and troubleshooting.**
    * This includes using the same Ansible module as other exisitng tasks in this repo.
    * Documentation on how to consistently use these modules are provided and should be maintained as the code base grows. 
* All code should should be written in a **generalized, scalable, and reusable manner.**
    * Anything specific should be abstracted from the code and defined as a variable.
    * Host, group, role, and environment are the common places to define these variables.
* This project should always follow Ansible [best practices](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html) when possible, including directory structure.
* Configuration baselines will be saved as roles.
    * Enforcement of each STIG check should be managed by variables so that checks can be relaxed as needed.
* All changes must be done in a development branch, and then merged to Main using a Pull Request (PR).
* Get with `POC` or `Alternate POC` if you have any questions, or need help getting setup.

# Branches and Pull Requests
* Work items (type Bug, Epic, or Feature) should be created before starting.
    * Link these work items as a child to an Epic on the [NEC Development PM project.](https://devops.yuma.army.mil/NECCollection/NEC%20Development%20PM/_boards/board/t/NEC%20Development%20PM%20Team/Epics)
    * Follow the project management guidelines outlined there. This is done so that the NEC Development PM board is the high level view of all active development work across projects.
    * Your development branch should be created from this work item. This will automatically link the PR when created.
    * You should merge the main branch into your branch often while developing, and fix any conflicts (if they occur) before creating a Pull Request.
* Pull Requests (PR) can only be created in Azure DevOps.
    * There will be a code review process before the PR gets approved to be merged into main.
    * You do not need to select any reviewers, mandatory reviewers will be added automatically.
    * All comments left by code reviewers must be resolved before the PR can be completed.
    * Build validation pipelines may be triggered depending on the changes you made. These must all succeed before the PR can be completed.
    * After creating the PR, you should use the ``Set auto-complete`` options with the ``Merge (no-fast forward)`` option. If you do this you won't have to come back and complete the PR after it has been approved by all reviewers.