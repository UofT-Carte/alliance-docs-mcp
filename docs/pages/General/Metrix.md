---
title: "Metrix/en"
url: "https://docs.alliancecan.ca/wiki/Metrix/en"
category: "General"
last_modified: "2026-06-30T14:17:29Z"
page_id: 31422
display_title: "Metrix"
---

= Summary =

The Metrix portal is a website for Alliance users. It collects information on compute nodes and management servers, to interactively generate data so you can track your resource usage (CPUs, GPUs, memory, filesystems) in real time.

Rorqual	https://metrix.rorqual.alliancecan.ca
Narval 	http://metrix.narval.alliancecan.ca
Nibi   	https://portal.nibi.sharcnet.ca
tamIA  	https://portail.tamia.ecpia.ca
Vulcan 	http://metrix.vulcan.alliancecan.ca

Filesystem performance

Here you have the graphs for bandwidths and metadata operations, along with viewing options (last week, last day and last hour).

Login nodes

Under this tab are presented  usage statistics for CPUs, memory, system load, and network, with viewing options (last week, last day, and last hour).

Scheduler

This tab shows statistics for the cluster's allocated cores and GPUs, with viewing options (last week, last day, and last hour).

Scientific software

These graphs show the software most frequently used, with CPU cores and GPUs.

Data transfer nodes

Bandwidth statistics for data transfer nodes are shown under this tab.

= User portal =
Under this tab, you find your quotas for the filesystems, followed by your 10 last jobs. You can select a job by its number to see the details. Also, by clicking on (More details), you are redirected to the Job statistics tab, where all your jobs are listed.

= Job statistics =
The first block shows your current usage (CPU cores, memory, and GPUs). These statistics represent the average usage by all currently running jobs. You can easily compare the resources allocated to you with those you actually use.

You then have a graph of the average for the last few days.

Next is a representation of your activity on the filesystems. On the left, the graph shows the number of disk write commands you have performed (input/output operations per second). On the right, you see the amount of data transferred to the servers over a given period (Bandwidth).

The next section shows all the jobs you have already started, which are currently running or pending. In the top left corner, you can filter jobs by their status (OOM, completed, running, etc.). In the top right corner, you can search by job ID or by job name. Finally, in the bottom right corner, there is an option to quickly navigate between pages by performing multiple jumps.

== CPU jobs ==
At the top, you see the job name, its number, your username, and the status. Details of your submission script are displayed by clicking on Show submitted job script. If the job was launched in interactive mode, the submission script will not be available.

The working directory and the submission command can be seen by clicking on  Show submit command.

The next section shows information on the scheduler. To display the information on your CPU account, click on your account number.

In the Ressources section, you can see the resources used by your job by comparing columns Allocated and Used for the listed parameters.

The CPU graph shows the CPU cores you have requested, over time. On the right, you can select the cores you want to see. Please note that this graph is not available for very short jobs.

This graphs shows the usage of the memory you requested, over time.

The Processes and threads graph shows different parameters. For a multithread job, adding parameters Running threads and Sleeping threads should  not exceed twice the number of cores requested. However, having some Sleeping threads is normal for certain types of programs  (java, Matlab, commercial software or complex programs). There is also a parameter for the program applications that have been executed over time.

The following graphs show filesystem usage by the current job, and not for the entire node. On the left, we have the number of I/O operations per second (IOPS). On the right, the graph illustrates the data transfer rate between the job and the filesystem, over time. This helps identify periods of high or low filesystem activity.

Resource statistics for the entire node may be inaccurate if the node is shared by multiple users. The graph on the left shows the evolution of the bandwidth used by the job over time, in relation to software, licenses, etc. The graph on the right shows the evolution of the network bandwidth used by a job or a set of jobs via the Infiniband network, over time. We can observe periods of massive data transfer (e.g., reading/writing on a filesystem (Lustre), MPI communication between nodes).

The graph on the left shows the evolution of the number of input/output operations per second (IOPS) performed on the local disk, over time. The graph on the right shows the evolution of the bandwidth used on the local disk over time, that is, the amount of data read or written per second.

Usage of local disk space

Power consumption

== CPU jobs (job arrays)==

The page for a CPU job in an array is the same as that for a regular CPU job, except for the Other jobs in the array section. The table lists the other job numbers that are part of the job array, along with information about their status, name, start time, and finish time.

== GPU jobs ==

At the top, you see the job name, its number, your username, and the status. Details of your submission script are displayed by clicking on Show submitted job script. If the job was launched in interactive mode, the submission script will not be available.

The working directory and the submission command are shown by clicking on  Show submit command.

The next section shows information on the scheduler. To display the information on your GPU account, click on your account number.

In the Ressources section, you can see the resources used by your job by comparing columns Allocated and Used for the listed parameters.

The CPU graph shows the CPU cores you have requested, over time. On the right, you can select the cores you want to see. Please note that this graph is not available for very short jobs.

This next graph shows the usage of the memory you requested for CPUs, over time.

The Processes and threads graph shows different parameters.

The following graphs show the usage of the filesystem by the current job, and not for the entire node. On the left, we have the number of I/O operations per second (IOPS). On the right, the graph illustrates the data transfer rate between the job and the filesystem, over time. This helps identify periods of high or low filesystem activity.

The GPU graph shows your GPU usage. The Streaming Multiprocessors (SM) setting indicates the percentage of time taken by the GPU to execute a warp (a group of consecutive threads) in the last sampling. This value should be around 80%. For SM occupancy (defined as the ratio between the number of warps assigned to an SM and the maximum number of warps an SM can handle), a value around 50% is generally expected. Regarding the Tensor setting, the value should be as high as possible. Ideally, your code should use this part of the GPU, which is optimized for multiplications and convolutions of multidimensional matrices. Finally, for FP64, FP32, and FP16 floating-point operations, you should observe significant activity on only one of these, depending on the precision specified by your code.

On the left, you have a graph showing the memory used by the GPU. On the right, a graph of the GPU's memory access cycles shows the percentage of cycles during which the device's memory interface is active sending or receiving data.

The GPU power graph displays the evolution of the GPU's power consumption (in watts), over time.

This next graph shows the GPU bandwidth on the PCIe bus (or PCI Express, for Peripheral Component Interconnect Express).

For statistics on the resources of the entire node, please note that they may be inaccurate if the node is shared among multiple users. The graph on the left shows the evolution of the bandwidth used by the job, over time, in relation to software, licenses, etc. The graph on the right shows the evolution of the network bandwidth used by a job or set of jobs via the Infiniband network, over time. Periods of massive data transfer can be observed (e.g., reading/writing to a filesystem (Lustre), MPI communication between nodes).

The graph on the left shows the evolution of the number of input/output operations per second (IOPS) performed on the local disk, over time. The graph on the right shows the evolution of the bandwidth used on the local disk, over time; that is, the amount of data read or written per second.

Usage of local disk space

Power consumption

= Account statistics =

The Account Statistics section shows your group's usage in two subsections: CPU and GPU.

== CPU accounts ==

Here you have the total number of CPU cores requested by your group, along with their corresponding usage over the past few months. You can also track your priority status, which varies based on your usage.

Applications used most frequently

Here are the resources used by each user in your group.

This graph shows the CPU cores wasted by each user, over time.

Here you see the memory used by each user in your group.

This graph shows the memory wasted by each user.

You then have a representation of your activity on the filesystems. On the left, the graph shows the number of disk write commands you have performed. (input/output operations per second (IOPS)) On the right, you see the amount of data transferred to the servers over a given period. (Bandwidth)

This lists the last jobs ran by all members of the group.

== GPU accounts ==

Here you can see the total GPU requests for your group, along with their usage over the past few months. You can also track your priority, which varies based on your usage.

This graph shows the software more frequently used.

Here you see the resources used by each user in your group.

This graph shows the quantity of GPUs wasted by each user.

Here you see the CPU allocated and used by your GPU jobs.

This graph shows the CPUs wasted by your GPU jobs.

Here you see the memory used by each user in your group.

This graph shows the memory wasted by each user.

You then have a representation of your activity on the filesystems. On the left, the graph shows the number of disk write commands you have performed. (input/output operations per second (IOPS)) On the right, you see the amount of data transferred to the servers over a given period. (Bandwidth)

Here you see the last jobs that were run by your group.

= Cloud statistics =

The table Your Instances displays all the virtual machines associated with your account. The Flavor column refers to the virtual machine type. The UUID column is a unique identifier assigned to each virtual machine.

Each virtual machine has its own usage statistics (CPU cores, memory, disk bandwidth, IOPS and network bandwidth) that can be shown for the last month, week, day or hour.