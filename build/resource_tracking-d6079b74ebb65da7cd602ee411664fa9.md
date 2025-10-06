# Resource tracking

Tracking resource usage is helpful to understand how your jobs are currently consuming cluster resources and to monitor for any unexpected changes (e.g., large, unexpected changes in priority can reveal when jobs may be less efficient than expected).
In this section, we provide general guidelines for checking your account's (and its associated allocation's) resource usage using both a [GUI-based dashboard](#using-the-metrix-portal) as well as via directly [at the command line](#tracking-resource-usage-at-an-account-level).
We also overview how to [check current usage patterns on a given cluster](#requesting-resources), such that you can make an informed choice about which resources to request.

## Using the Metrix portal

Alliance Canada maintains a [metrix portal](https://docs.alliancecan.ca/wiki/Metrix) for each of its clusters.
Please refer to the the Alliance Canada documentation for each cluster (e.g., [Rorqual](https://docs.alliancecan.ca/wiki/Rorqual/en)) for the most up-to-date link for the portal.

This is the most user-friendly way to access all of the information we discuss below.
However, it is still a good idea to understand how to access this information outside of the metrix portal; as this data is pulled in real time, it may fail to populate if the system is over-subscribed !
If there is a known problem with the Metrix portal, this should be documentated on https://status.alliancecan.ca.

## Tracking resource usage at an account level

To view all users in a given allocation (e.g., `rrg-pbellec_gpu`) or in multiple allocations, we can run:

```console
sshare -l --accounts=rrg-pbellec_gpu -a
```

We can also pass multiple allocations in a comma-separated list.
To view only a subset of users within allocations, simply pass the `-u` flag with the relevant user name(s):

```console
sshare -l --accounts=rrg-pbellec_cpu,def-pbellec_cpu -u emdupre
```

We can interpret each of the returned fields following [Alliance Canada's documentation](https://docs.alliancecan.ca/wiki/Job_scheduling_policies#Priority_and_fair-share):

- `RawShares` is proportional to the number of CPU-years that was granted to the project for use on this cluster in the Resource Allocation Competition.
- `NormShares` is the number of shares assigned to the user (or account) divided by the total number of assigned shares within the level. 
- `RawUsage` is calculated from the total number of resource-seconds (that is, CPU time, GPU time, and memory) that have been charged to this account. **Past usage is discounted with a half-life of one week, so usage more than a few weeks in the past will have only a small effect on priority.**
- `EffectvUsage` is the account's usage normalized with its parent; that is, the project's usage relative to other projects, the user's relative to other users in that project.
- `LevelFS` is the account's fairshare value compared to its siblings, calculated as `NormShares` / `EffectvUsage`. 
    * If an account is over-served, the value is between 0 and 1.  
    * If an account is under-served, the value is greater than 1.  
    * Accounts with no usage receive the highest possible value, `inf` or "infinity".  
    

### Tracking resource usage at a job level

The Alliance Canada documentation has lots of resources for [monitoring jobs, including tracking their resource usage](https://docs.alliancecan.ca/wiki/Monitoring_jobs).

One useful command to get a full accounting of a completed job is with `scontrol`:

```console
scontrol show job -dd <JOBID>
```

## Requesting resources

In order to more efficiently _request_ resources, we can use the `partition-stats` command, called simply using:

  ```console
  partition-stats
  ```

We can interpret its output again following the [Alliance Canada documentation](https://docs.alliancecan.ca/wiki/Job_scheduling_policies#Percentage_of_the_nodes_you_have_access_to).
Specifically, the command will return:

- how many jobs are waiting to run ("queued") in each partition,
- how many jobs are currently running,
- how many nodes are currently idle, and
- how many nodes are assigned to each partition.


### Estimating start time for a given job

As Alliance Resources [implement backfilling](https://docs.alliancecan.ca/wiki/Job_scheduling_policies#Backfilling), jobs are not strictly started in terms of priority order, but also in terms of what resources are available.
The start time for a given job can therefore be estimated using:

```console
squeue --start -j <JOBID>
```

Note, though, that this is not a strictly accurate estimate, as it depends on multiple factors including that other, currently running jobs have requested accurate time limits.
