# Let's get started

The lab applies for storage space and compute time on Alliance Canada every year.
These resources are limited and have to be shared fairly across members of the lab.
Given that no member of the lab has privileged admin rights, this fairness relies on everyone adopting a clear code of conduct, and shared organization.

## Get access 
To get access to simexp resources in Alliance Canada, create an account on [CCDB](https://ccdb.alliancecan.ca/) and then apply for resources under tab "My Account",  select "Apply for a new role", then apply the appropriate role with CCRI `gsf-624-02`. Note that the main allocation of the lab is currently hosted on [rorqual](https://docs.alliancecan.ca/wiki/Rorqual/en). 

## Submitting jobs
You can learn more on high-performance computing (HPC) and the Digital Alliance using their [docs](https://docs.alliancecan.ca/wiki/Running_jobs). The compute allocation of the lab (only available on `rorqual`) can be accessed using the code `gsf-624-ab`. You can log on any HPC of the Alliance, but you will only have access to the default compute allocation there (`gsf-624-aa`). Note that each HPC is managed independently, so compute launched on, say, `beluga` does not affect our `rorqual` allocation. 

## Setup your environment

When you are new to Alliance Canada, we will ask you to run a setup script that will set data management access and give you access to utils for project management, including:

- setup ACLs for the data admin to the project and nearline folders
- add project management commands to your bash environment
- generate SSH keys if not already created, and help you set them up on Github for easier access
- configure the ssh agent and keychain to avoid typing your ssh key password each time you push to github or ssh to another server.
- configure git global variables


You can do it just once on each cluster:

```
/project/def-pbellec/share/data_admin/utils/setup_user_account.sh
```

## Add a new dataset

Datasets are stored in `~/project/(rrg|def)-pbellec/datasets`

> __IMPORTANT__ When applying, it is important that you involve the lab's data admins so they can also sign the non-sharing agreement or other necessary documents. If you want to add a new dataset please contact the lab's data admin (Basile).

## Renewing or terminating your role
Every year Digital alliance requires you to renew your account. It is important to do so on a timely fashion in order to prevent interruption in access. If you change position within the lab, your current role will be terminated and you will be required to re-apply under a new role. 

