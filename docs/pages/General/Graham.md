---
title: "Graham/en"
url: "https://docs.alliancecan.ca/wiki/Graham/en"
category: "General"
last_modified: "2026-07-16T14:46:35Z"
page_id: 1194
display_title: "Graham"
---

Availability: In production June 2017 until late 2025.  SERVICE NOW ENDED.
Login node: graham.alliancecan.ca
Globus collection: computecanada#graham-globus
Data transfer node (rsync, scp, sftp, etc.): use robot or login nodes

Graham is a heterogeneous cluster, suitable for a variety of workloads, and located at the University of Waterloo. It is named after Wes Graham, the first director of the Computing Centre at Waterloo.

The parallel filesystem and external persistent storage (called "NDC-Waterloo" in some documents) are similar to Cedar's. The interconnect is different and there is a slightly different mix of compute nodes.

It is entirely liquid cooled, using rear-door heat exchangers.

Getting started with Graham

How to run jobs

Transferring data

==Site-specific policies==

* By policy, Graham's compute nodes cannot access the internet. If you need an exception to this rule, contact technical support with the following information:

IP:
Port/s:
Protocol:  TCP or UDP
Contact:
Removal Date:

On or after the removal date we will follow up with the contact to confirm if the exception is still required.

* Crontab is not offered on Graham.
* Each job on Graham should have a duration of at least one hour (five minutes for test jobs) and no more than 168 hours (seven days).
* A user cannot have more than 1000 jobs, running and queued, at any given moment.  An array job is counted as the number of tasks in the array.

==Storage==

Home space133TB total volume
* Location of home directories.
* Each home directory has a small, fixed quota.
* Not allocated via RAS or RAC. Larger requests go to Project space.
* Has daily backup.
Scratch space3.2PB total volumeParallel high-performance filesystem
* For active or temporary (/scratch) storage.
* Not allocated.
* Large fixed quota per user.
* Inactive data will be purged.
Project space16PB total volumeExternal persistent storage
* Allocated via RAS or RAC.
* Not designed for parallel I/O workloads. Use Scratch space instead.
* Large adjustable quota per project.
* Has daily backup.

==High-performance interconnect==

Mellanox FDR (56Gb/s) and EDR (100Gb/s) InfiniBand interconnect.  FDR is used for GPU and cloud nodes, EDR for other node types.  A central 324-port director switch aggregates connections from islands of 1024 cores each for CPU and GPU nodes.  The 56 cloud nodes are a variation on CPU nodes, and are on a single larger island sharing 8 FDR uplinks to the director switch.

A low-latency high-bandwidth Infiniband fabric connects all nodes and scratch storage.

Nodes configurable for cloud provisioning also have a 10Gb/s Ethernet network, with 40Gb/s uplinks to scratch storage.

The design of Graham is to support multiple simultaneous parallel jobs of up to 1024 cores in a fully non-blocking manner.

For larger jobs the interconnect has a 8:1 blocking factor, i.e., even for jobs running on multiple islands the Graham system provides a high-performance interconnect.

Graham high performance interconnect diagram

==Visualization on Graham==

Graham has dedicated visualization nodes available at gra-vdi.alliancecan.ca that allow only VNC connections. For instructions on how to use them, see the VNC page.

==Node characteristics==

In early 2025 Graham's capacity was reduced to make space for the installation of the new Nibi cluster.  The table below lists the remaining nodes as of February, 2025.

Turbo Boost is enabled for all Graham nodes.

nodes	cores	available memory 	CPU                                            	storage        	GPU
2    	40   	377G or 386048M  	2 x Intel Xeon Gold 6248 Cascade Lake @ 2.5GHz 	5.0TB NVMe SSD 	8 x NVIDIA V100 Volta (32GB HBM2 memory),NVLINK
6    	16   	187G or 191840M  	2 x Intel Xeon Silver 4110 Skylake @ 2.10GHz   	11.0TB SATA SSD	4 x NVIDIA T4 Turing (16GB GDDR6 memory)
30   	44   	187G or 191840M  	2 x Intel Xeon Gold 6238 Cascade Lake @ 2.10GHz	5.8TB NVMe SSD 	4 x NVIDIA T4 Turing (16GB GDDR6 memory)
136  	44   	187G or 191840M  	2 x Intel Xeon Gold 6238 Cascade Lake @ 2.10GHz	879GB SATA SSD 	-
1    	128  	2000G or 2048000M	2 x AMD EPYC 7742                              	3.5TB SATA SSD 	8 x NVIDIA A100 Ampere
2    	32   	256G or 262144M  	2 x Intel Xeon Gold 6326 Cascade Lake @ 2.90GHz	3.5TB SATA SSD 	4 x NVIDIA A100 Ampere
11   	64   	128G or 131072M  	1 x AMD EPYC 7713                              	1.8TB SATA SSD 	4 x NVIDIA RTX A5000 Ampere
6    	32   	1024G or 1048576M	1 x AMD EPYC 7543                              	8x2TB NVMe     	-

Most applications will run on either Skylake or Cascade Lake nodes, and performance differences are expected to be small compared to job waiting times. Therefore we recommend that you do not select a specific node type for your jobs. If it is necessary to constrain a CPU job, use --constraint=cascade. See how to specify the CPU architecture.

Best practice for local on-node storage is to use the temporary directory generated by Slurm, $SLURM_TMPDIR. Note that this directory and its contents will disappear upon job completion.

Note that the amount of available memory is less than the "round number" suggested by hardware configuration.  For instance, "base" nodes do have 128 GiB of RAM, but some of it is permanently occupied by the kernel and OS.  To avoid wasting time by swapping/paging, the scheduler will never allocate jobs whose memory requirements exceed the specified amount of "available" memory.  Please also note that the memory allocated to the job must be sufficient for IO buffering performed by the kernel and filesystem - this means that an IO-intensive job will often benefit from requesting somewhat more memory than the aggregate size of processes.

==GPUs on Graham==
Graham contains Tesla GPUs from three different generations, listed here in order of age, from oldest to newest.

* V100 Volta GPUs (2 nodes with NVLINK interconnect)
* T4 Turing GPUs
* A100 Ampere

P100 GPUs have been decommissioned.  V100 is its successor, with about double the performance for standard computation, and about 8X performance for deep learning computations which can utilize its tensor core computation units.  T4 Turing is the latest card targeted specifically at deep learning workloads - it does not support efficient double precision computations, but it has good performance for single precision, and it also has tensor cores, plus support for reduced precision integer calculations.

===Pascal GPU nodes on Graham===

No longer available.

===Volta GPU nodes on Graham===
Graham has a total of 2 Volta nodes. They have high bandwidth NVLINK interconnect.

The nodes are available to all users with a maximum job duration of seven days.

Following is an example job script to submit a job to one of the nodes (with 8 GPUs).  The module load command will ensure that modules compiled for Skylake architecture will be used.  Replace nvidia-smi with the command you want to run.

Important: You should scale the number of CPUs requested, keeping the ratio of CPUs to GPUs at 3.5 or less on 28 core nodes.  For example, if you want to run a job using 4 GPUs, you should request at most 14 CPU cores.  For a job with 1 GPU, you should request at most 3 CPU cores.     Users are allowed to run a few short test jobs (shorter than 1 hour) that break this rule to see how your code performs.

The two newest Volta nodes have 40 cores so the number of cores requested per GPU should be adjusted upwards accordingly, i.e. you can use 5 CPU cores per GPU. They also have NVLINK, which can provide huge benefits for situations where memory bandwidth between GPUs is the bottleneck. If you want to use one of these NVLINK nodes, you should request it directly by adding  the --constraint=cascade,v100 parameter to the job submission script.

Single-GPU example:

Full-node example:

The Volta nodes have a fast local disk, which should be used for jobs if the amount of I/O performed by your job is significant. Inside the job, the location of the temporary directory on fast local disk  is specified by the environment variable $SLURM_TMPDIR. You can copy your input files there at the start of your job script before you run your program and your output files out at the end of your job script. All the files in $SLURM_TMPDIR will be removed once the job ends, so you do not have to clean up that directory yourself.   You can even create Python virtual environments in this temporary space for greater efficiency.  Please see the information on how to do this.

===Turing GPU nodes on Graham===

The usage of these nodes is similar to using the Volta nodes, except when requesting them, you should specify:

 --gres=gpu:t4:2

In this example, two T4 cards per node are requested.

===Ampere GPU nodes on Graham===

The usage of these nodes is similar to using the Volta nodes, except when requesting them, you should specify:

 --gres=gpu:a100:2

or

 --gres=gpu:a5000:2

In this example, two Ampere cards per node are requested.

==Graham reduction==
Starting January 13, 2025, the Graham cluster will operate at approximately 25% capacity until the new system Nibi comes online.