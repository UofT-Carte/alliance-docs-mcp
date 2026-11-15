---
title: "Monitoring jobs/en"
url: "https://docs.alliancecan.ca/wiki/Monitoring_jobs/en"
category: "General"
last_modified: "2026-11-03T18:50:14Z"
page_id: 28553
display_title: "Monitoring jobs"
---

Ensuring that your jobs make efficient use of the resources that are assigned to them is an important part of being a responsible user. This is particularly true when you are using a new program or have made some other substantial change in the work being done by your job.

The best tool for examining job performance is the Metrix web service or "portal" for each cluster.  Please see Metrix for a description of the tool and a list of URLs.

The remainder of this page describes other methods for evaluating the efficiency of jobs.

= Current jobs =

By default squeue will show all the jobs the scheduler is managing at the moment. It will run much faster if you ask only about your own jobs with
 $ squeue -u $USER
You can also use the utility sq to do the same thing with less typing.

You can show only running jobs, or only pending jobs:
 $ squeue -u  -t RUNNING
 $ squeue -u  -t PENDING

You can show detailed information for a specific job with scontrol:
 $ scontrol show job -dd

Do not run squeue from a script or program at high frequency (e.g., every few seconds). Responding to squeue adds load to Slurm and may interfere with its performance or correct operation.

= Email notification =

You can ask to be notified by email of certain job conditions by supplying options to sbatch:
 #SBATCH --mail-user=your.email@example.com
 #SBATCH --mail-type=ALL
For a complete list of the options see SchedMD's documentation.

= Output buffering =

Output from a non-interactive Slurm job is normally buffered, which means that there is usually a delay between when data is written by the job and when you can see the output on a login node.  Depending on the application you are running and the load on the filesystem, this delay can range from less than a second to many minutes, or until the job completes.

There are methods to reduce or eliminate the buffering, but we do not recommend using them because buffering is vital to preserving the overall performance of the filesystem.  If you need to monitor the output from a job in real time, we recommend you run an interactive job as described above.

= Completed jobs =

== Monitoring Single Job with seff ==

Get a short summary of the CPU and memory efficiency of a job with seff:
 $ seff 12345678
 Job ID: 12345678
 Cluster: cedar
 User/Group: jsmith/jsmith
 State: COMPLETED (exit code 0)
 Cores: 1
 CPU Utilized: 02:48:58
 CPU Efficiency: 99.72% of 02:49:26 core-walltime
 Job Wall-clock time: 02:49:26
 Memory Utilized: 213.85 MB
 Memory Efficiency: 0.17% of 125.00 GB

Find more detailed information about a completed job with sacct, and optionally, control what it prints using --format:
 $ sacct -j
 $ sacct -j  --format=JobID,JobName,MaxRSS,Elapsed

The output from sacct typically includes records labelled .bat+ and .ext+, and possibly .0, .1, .2, ....
The batch step (.bat+) is your submission script - for many jobs that's where the main part of the work is done and where the resources are consumed.
If you use srun in your submission script, that would create a .0 step that would consume most of the resources.
The extern (.ext+) step is basically prologue and epilogue and normally doesn't consume any significant resources.

If a node fails while running a job, the job may be restarted. sacct will normally show you only the record for the last (presumably successful) run. If you wish to see all records related to a given job, add the --duplicates option.

Use the MaxRSS accounting field to determine how much memory a job needed. The value returned will be the largest resident set size for any of the tasks. If you want to know which task and node this occurred on, print the MaxRSSTask and MaxRSSNode fields also.

The sstat command works on a running job much the same way that sacct works on a completed job.

== Monitoring Multiple Jobs with reportseff ==

reportseff is a Python wrapper around sacct that provides a tabular, color-coded summary of Slurm job efficiency. While seff is limited to inspecting a single job at a time, reportseff queries accounting records in a single batch call to evaluate CPU, memory, and walltime utilization across job arrays, directories of output logs, or entire user histories.

=== Usage ===

reportseff accepts job IDs, array IDs, paths to Slurm output files, or user/time filters:

* Current directory scan: Running reportseff without arguments scans the working directory for standard Slurm output files (e.g., slurm-%j.out or %x_%A_%a.out) and displays metrics for the corresponding jobs.
* Specific jobs or arrays: Pass one or more job IDs (reportseff 123456), array tasks (123456_1), or log filenames directly.
* User and time filtering: Use -u  to query a user's recent jobs, and --since to constrain the time window (accepts standard sacct date formats or shorthand like d=4,h=2).
* Custom columns: Append or override sacct and efficiency fields using --format (e.g., --format +MaxRSS,ReqMem,GPUEff).

=== Examples ===

Check efficiency for all jobs in the current directory

Calling reportseff inside a project directory containing Slurm output logs automatically parses the job IDs from the filenames:

$ reportseff
   JobID      State          Elapsed   TimeEff   CPUEff   MemEff
 39481020   COMPLETED       01:12:44    60.6%    98.2%    45.1%
 39481021_1 COMPLETED       00:45:10    37.6%    94.0%    12.3%
 39481021_2 COMPLETED       00:48:02    40.0%    95.1%    14.0%
 39481021_3 OUT_OF_MEMORY   00:19:55    16.6%    88.4%   100.0%

Query jobs over the last 3 days with extra memory columns

To audit all jobs run by your user over the past three days and append requested memory (ReqMem) and peak memory footprint (MaxRSS) to the default table:

$ reportseff -u $USER --since d=3 --format +ReqMem,MaxRSS
   JobID      State       Elapsed   TimeEff   CPUEff   MemEff   ReqMem   MaxRSS
 39500112   COMPLETED    04:15:22    85.1%    99.1%    78.4%     16G     12.5G
 39500489   TIMEOUT      12:00:10   100.0%    49.8%    22.0%     64G     14.1G
 39501004   COMPLETED    00:08:14     6.9%    12.5%     3.1%     32G      1.0G

= Attaching to a running job =
It is possible to connect to the node running a job and execute new processes there. You might want to do this for troubleshooting or to monitor the progress of a job.

Suppose you want to run the utility nvidia-smi to monitor GPU usage on a node where you have a job running. The following command runs watch on the node assigned to the given job, which in turn runs nvidia-smi every 30 seconds, displaying the output on your terminal.

 $ srun --jobid 123456 --overlap --pty watch -n 30 nvidia-smi

It is possible to launch multiple monitoring commands using tmux. The following command launches htop and nvidia-smi in separate panes to monitor the activity on a node assigned to the given job.

 $ srun --jobid 123456 --overlap --pty tmux new-session -d 'htop -u $USER' \; split-window -h 'watch nvidia-smi' \; attach

Processes launched with srun share the resources with the job specified. You should therefore be careful not to launch processes that would use a significant portion of the resources allocated for the job. Using too much memory, for example, might result in the job being killed; using too many CPU cycles will slow down the job.

Noteː The srun commands shown above work only to monitor a job submitted with sbatch. To monitor an interactive job, create multiple panes with tmux and start each process in its own pane.

= Monitoring a GPU job =
See Monitor GPU usage