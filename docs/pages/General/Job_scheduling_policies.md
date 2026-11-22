---
title: "Job scheduling policies/en"
url: "https://docs.alliancecan.ca/wiki/Job_scheduling_policies/en"
category: "General"
last_modified: "2026-11-12T16:21:40Z"
page_id: 4074
display_title: "Job scheduling policies"
---

Parent page: Running jobs

You can do much work on our clusters by submitting jobs
that specify only the number of cores and a runtime limit.
However if you submit large numbers of jobs, or jobs that require large
amounts of resources, you may be able to improve your productivity
by understanding the policies affecting job scheduling.

== Priority and fair-share ==

The order in which jobs are considered for scheduling is determined by priority.
Priority on our systems is determined using the "fair tree" algorithm, described here and here.

Each job is charged to a Resource Allocation Project (RAP).
You specify the project with the --account argument to sbatch.
The project might hold a grant of CPU or GPU time from a Resource Allocation Competition, in which case the account code will probably begin with rrg- or rpp-. Or it could be a non-RAC project, also known as a Rapid Access Service project, in which case the account code will probably begin with def-. See Accounts and Projects for how to determine what account codes you can use.

Every project has a target usage level.  RAC projects have target levels determined by the number of CPU-years or GPU-years granted with each RAC award.  Non-RAC projects (i.e. def- accounts) all have equal target levels, and that equal value is adjusted every few minutes based on the number of projects that are active on the cluster.

See also: Allocations and compute scheduling.

=== Target and recent usage with sshare ===

As an example let us imagine a research group with the account code def-prof1. Members of this imaginary group have user names prof1, grad2 and postdoc3. We can examine the group's usage and share information with the sshare command as shown below. Note that we must append _cpu or _gpu to the end of the account code, as appropriate, since CPU and GPU use are tracked separately.

 [prof1@login1 ~]$ sshare -l -A def-prof1_cpu -u prof1,grad2,postdoc3
        Account       User  RawShares  NormShares  RawUsage  ... EffectvUsage  ...    LevelFS  ...
 -------------- ---------- ---------- -----------  --------  ... ------------  ... ----------  ...
 def-prof1_cpu                     72    0.001607   1512054  ...     0.000043  ...  37.357207  ...
  def-prof1_cpu      prof1          1    0.100000         0  ...     0.000000  ...        inf  ...
  def-prof1_cpu      grad2          1    0.100000     54618  ...     0.036122  ...   2.768390  ...
  def-prof1_cpu   postdoc3          1    0.100000    855517  ...     0.565798  ...   0.176741  ...

The output shown above has been simplified by removing several fields which are not relevant to this discussion.
Furthermore the line that is most important for scheduling is the first one, highlighted in red.
This line describes the status of the project relative to all other projects using the cluster.
In this example, the research group share is 0.1607% and they have used 0.0043% of the resources on the cluster, the group's LevelFS is 37 which is quite high as the group has used a small fraction of their allocated share of resources. We would expect that jobs submitted by this group to have a fairly high priority.

Successive lines describe the status of each user relative to other users in this project.
Reading the 3rd line, grad2 has 1 share allocated within his group representing 10% of the group's allocation is responsible for only 3.6122% of the group's recent resource use and therefore has a higher than average level fairshare within the group. We would expect that jobs submitted by grad2 to have slightly more priority than jobs submitted by postdoc3 but less priority than jobs submitted by prof1.
The priority of jobs belonging to def-prof1 group as compared to the priority of jobs belonging to other research groups is determined solely by the group’s fairshare and not the users fairshare within the group.

The project by itself, or the user within a project, is referred to as an "association" in the Slurm documentation.
* Account, obviously, is the project name with _cpu or _gpu appended.
* User: Notice that the first line of output, the highlighted line, does not include a user name.
* RawShares is proportional to the number of CPU-years or GPU-years that was granted to the project for use on this cluster in the Resource Allocation Competition. All non-RAC accounts have small equal numbers of shares.
** For numeric reasons, inactive def- accounts (which do not have pending or running jobs) are given only one share.  Activity is checked periodically, so if you submit a job with an inactive account, it may take up to 15 minutes before the account shows the expected RawShares and LevelFS.
* NormShares is the number of shares assigned to the user or account divided by the total number of assigned shares within the level. So for the first line, the NormShares of 0.001607 is the fraction of the shares held by the project, relative to all other projects. The NormShares of 0.10000 on the other three lines are the fraction of shares held by each member of the project relative to the other members. (This project has ten members, but we only asked for information about three.)
* RawUsage is calculated from the total number of resource-seconds (that is, CPU time, GPU time, and memory) that have been charged to this account.  Past usage is discounted with a half-life of one week, so usage more than a few weeks in the past will have only a small effect on priority.
* EffectvUsage is the association's usage normalized with its parent; that is, the project's usage relative to other projects, the user's relative to other users in that project. In this example, postdoc3 has 56.6% of the project's usage, and grad2 has 3.6%.
* LevelFS is the association's fairshare value compared to its siblings, calculated as NormShares / EffectvUsage.
** If an association is over-served, the value is between 0 and 1.
** If an association is under-served, the value is greater than 1. Associations with no usage receive the highest possible value, infinity.
** For inactive def- accounts having RawShares set to one, the LevelFS equals a meaningless small number close to 0.0001.

A project which consistently uses its target amount will have a LevelFS near 1.0. If the project uses more than its target, then its LevelFS will be below 1.0 and the priority of new jobs belonging to that project will also be low. If the project uses less than its target usage  then its LevelFS will be greater than 1.0 and new jobs will enjoy high priority.

In practice, the normalization factors used for NormShares and EffectvUsage are not the same. Consequently, LevelFS is not exactly equal to 1.0 when the usage matches the target. The sshare2 utility can correct this discrepancy.

=== Target and recent usage with sshare2 ===

The sshare2 utility receives a reduced set of arguments and prints only the most relevant fields. Here is an example with the same account used in the previous section.

 [prof1@login1 ~]$ sshare2 -A def-prof1_cpu
 Account               RawShares  RecentUsage   PercentUse   Scaled_LevelFS
 -------------------- ---------- ------------ ------------ ----------------
 def-prof1_cpu                72            2        2.41%        41.555277

The different fields are:

* RawShares: same value as that reported by sshare.
* RecentUsage: this is the sshare's RawUsage value downscaled by a factor that removes its time component (in seconds), which makes the result in the same units and scale as the RawShares.
** Note: the RecentUsage behaves like a weighted average where the most recent usage has the most value. That is why the recent usage can look different than the average usage displayed on the Alliance Slurm portal, especially when the usage is not constant over time.
* PercentUse: equivalent to RecentUsage / RawShares, as a percentage.
** When RawShares is 0 or 1, the result is NA because the account has expired or is inactive, respectively.
* Scaled_LevelFS: equivalent to RawShares / RecentUsage and similar to sshare's LevelFS, but a value of 1.0 really means a recent usage equivalent to the target.

For convenience, when no account is specified on the command line, sshare2 displays the information for all accounts associated to the current user. Optionally, the -n flag can be specified to remove the table header.

 [prof1@login1 ~]$ sshare2 -n
 def-prof1_cpu                72            2        2.41%        41.555277
 def-prof1_gpu                 1            0           NA    872691.969325

== Whole nodes versus cores ==

Applications which can efficiently use more cores than are found in a single node may benefit from being scheduled on whole nodes. Some clusters have nodes reserved for jobs which request one or more entire nodes. See whole nodes on the page Advanced MPI scheduling for example scripts and further discussion.

Note that requesting an inefficient number of processors for a calculation simply in order to take advantage of whole-node scheduling will be construed as abuse of the system. For example, a program which takes just as long to run on 192 cores as on 64 cores should request 64 cores, not 192.

If you have huge amounts of serial work and can efficiently use META-Farm, GNU Parallel, GLOST,
or other techniques to pack
serial processes onto a single node, you are also welcome to use whole-node scheduling.

== Time limits ==

Trillium accepts jobs of up to 24 hours run-time, Fir, Narval, Nibi and Rorqual up to 7 days.
These limits are subject to change at the discretion of each site's sysadmin team.

On the general-purpose clusters, longer jobs are restricted to use only a fraction of the cluster by partitions. There are partitions for jobs of
* 3 hours or less,
* 12 hours or less,
* 24 hours (1 day) or less,
* 72 hours (3 days) or less,
* 7 days or less
Because any job of 3 hours is also less than 12 hours, 24 hours, and so on, shorter jobs can always run in partitions with longer time-limits. A shorter job will have more scheduling opportunities than an otherwise-identical longer job.

=== Backfilling ===

The scheduler employs backfilling to improve
overall system usage.

Without backfill scheduling, each partition is scheduled strictly in priority order, which typically results in significantly lower system utilization and responsiveness than otherwise possible. Backfill scheduling will start lower priority jobs if doing so does not delay the expected start time of any higher priority jobs. Since the expected start time of pending jobs depends upon the expected completion time of running jobs, reasonably accurate time limits are important for backfill scheduling to work well.

Backfilling will primarily benefit jobs with short time limits, e.g. under 3 hours.

== Percentage of the nodes you have access to ==

This section aims at giving some insight into how the general-purpose clusters (Fir, Narval, Nibi, Rorqual) are partitioned.

First, the nodes are partitioned into four different categories:
* Base nodes, which have 4 or 8 GB of memory per core
* Large memory nodes, which have 16 to 96 GB of memory per core
* GPU nodes
Upon submission, your job will be routed to one of these categories based on what resources are requested.

Second, within each of the above categories, some nodes are reserved for jobs which can make use of complete nodes (i.e. jobs which use all of the resources available on the allocated nodes). If your job only uses a few cores (or a single core) out of each node, it is only allowed to use a subset of the category. These are referred to as "by-node" and "by-core" partitions.

Finally, the nodes are partitioned based on the walltime requested by your job. Shorter jobs have access to more resources. For example, a job with less than 3 hours of requested walltime can run on any node that allows 12 hours, but there are nodes which accept 3 hour jobs that do *not* accept 12 hour jobs.

The utility partition-stats shows
* how many jobs are waiting to run ("queued") in each partition,
* how many jobs are currently running,
* how many nodes are currently idle, and
* how many nodes are assigned to each partition.
Here is some sample output from partition-stats:

[user@login1 ~]$ partition-stats

Node type |                     Max walltime
          |     3 hr   |   12 hr   |   24 hr   |   72 hr   |   168 hr  |
----------|-------------------------------------------------------------
       Number of Queued Jobs by partition Type (by node:by core)
----------|-------------------------------------------------------------
Regular   |    12:170  |   69:7066 |   70:7335 |  386:961  |   59:509  |
Large Mem |     0:0    |    0:0    |    0:0    |    0:15   |    0:1    |
GPU       |     5:14   |    3:8    |   21:1    |  177:110  |    1:5    |
----------|-------------------------------------------------------------
      Number of Running Jobs by partition Type (by node:by core)
----------|-------------------------------------------------------------
Regular   |     8:32   |   10:854  |   84:10   |   15:65   |    0:674  |
Large Mem |     0:0    |    0:0    |    0:0    |    0:1    |    0:0    |
GPU       |     5:0    |    2:13   |   47:20   |   19:18   |    0:3    |
----------|-------------------------------------------------------------
        Number of Idle nodes by partition Type (by node:by core)
----------|-------------------------------------------------------------
Regular   |    16:9    |   15:8    |   15:8    |    7:0    |    2:0    |
Large Mem |     3:1    |    3:1    |    0:0    |    0:0    |    0:0    |
GPU       |     0:0    |    0:0    |    0:0    |    0:0    |    0:0    |
----------|-------------------------------------------------------------
       Total Number of nodes by partition Type (by node:by core)
----------|-------------------------------------------------------------
Regular   |   871:431  |  851:411  |  821:391  |  636:276  |  281:164  |
Large Mem |    27:12   |   27:12   |   24:11   |   20:3    |    4:3    |
GPU       |   156:78   |  156:78   |  144:72   |  104:52   |   13:12   |
----------|-------------------------------------------------------------

Looking at the first entry in the table, at the upper left, the numbers 12:170, 0:0, and 5:14 mean that there were
* 12 jobs waiting to run which requested
** whole nodes,
** less than 8GB of memory per core, and
** 3 hours or less of run time.
* 170 jobs waiting which requested
** less than whole nodes and were therefore waiting to be scheduled on individual cores,
** less than 8GB memory per core, and
** 3 hours or less of run time.
* 5 jobs waiting which requested
** a whole node equipped with GPUs and
** 3 hours or less of run time.
* 14 jobs waiting which requested
** single GPUs and
** 3 hours or less of run time.
There were no jobs running or waiting which requested large-memory nodes and 3 hours of run time.

At the bottom of the table we find the division of resources by policy, independent of the immediate number of jobs. Hence there are 871 base nodes, called "regular" here (that is, nodes with 4 to 8 GB memory per core), which may receive whole-node jobs of up to 3 hours. Of those 871,
* 431 of them may also receive by-core jobs of up to three hours,
* 851 of them may receive whole-node jobs of up to 12 hours,
* and so on.

It may help to think of these partitions as being like Matryoshka (Russian) dolls. The 3-hour partition contains the nodes for the 12-hour partition as a subset. The 12-hour partition in turn contains the 24-hour partition, and so on.

The partition-stats utility does not give information about the number of cores represented by running or waiting jobs, nor the number of cores free in partly-assigned nodes in by-core partitions, nor about available memory associated with free cores in by-core partitions.

Running partition-stats is somewhat costly to the scheduler. Please do not write a script which automatically calls partition-stats repeatedly. If you have a workflow which you believe would benefit from automatic parsing of the information from partition-stats, please contact Technical support and ask for guidance.

== Number of jobs ==

There may be a limit on the number of jobs you can have in the system at any one time.

On Narval, Nibi and Rorqual, normal accounts can have no more than 1000 jobs in a pending or running state at any time.  Each task of a job array counts as one job.  The limit is applied using Slurm's MaxSubmit parameter.

== Changes over time ==

See Scheduling policy updates to see changes which might affect the behaviour of your job scripts, and when the changes were implemented.