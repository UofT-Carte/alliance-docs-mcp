---
title: "Rocky"
url: "https://docs.alliancecan.ca/wiki/Rocky"
category: "General"
last_modified: "2026-09-24T18:55:07Z"
page_id: 35052
display_title: "Rocky"
---

Availability: Onboarding in progress
Login node: rocky.alliancecan.ca
Globus collection: Rocky Globus v5
System Status Page: Rocky status page
Portal: To be announced
Open OnDemand: To be announced

Rocky is a GPU cluster dedicated to the needs of the Canadian scientific Artificial Intelligence community. Rocky is located in Calgary, Alberta, hosted on Denvr infrastructure, and managed by Amii (Alberta Machine Intelligence Institute). It is currently being onboarded to the Digital Research Alliance of Canada.

__TOC__

=Site-specific policies=

Internet access is not generally available from the compute nodes. If you cannot connect to a domain you need, contact technical support and we evaluate the request.

Maximum duration of jobs is 7 days.

=Access=

To log in to Rocky, request access in CCDB.

=Rocky hardware specifications=

Rocky is being deployed in two immersion-cooled tanks of 13 nodes each.

Nodes            	Model                                   	CPU                                   	Cores	System Memory 	GPUs per node            	Total GPUs
26 (2 tanks × 13)	Dell PowerEdge XE9680 (immersion-cooled)	2 x Intel Xeon Platinum 8570 (2.1 GHz)	112  	2 TB DDR5-5600	8 x NVIDIA H200 SXM 141GB	208

Within each node, NVLink fully connects the 8 GPUs through NVSwitch.

Each node also has 7 x 3.84 TB NVMe SSDs for fast node-local job storage. See Node-local storage.

=Storage=

Rocky's storage is a Ceph cluster, with user file systems served by CephFS and a total usable capacity of approximately 1.72 PB. Home, Scratch, and Project are on the same CephFS file system.

Home space
* Location of /home directories.
* Each /home directory has a small fixed quota.
* Not allocated via RAS or RAC. Larger requests go to the /project space.
* Has daily backup.
Scratch space
* For active or temporary (scratch) storage.
* Not allocated.
* Large fixed quota per user.
* Inactive data is purged after 60 days.
Project space
* Large adjustable quota per project.
* Has daily backup.

==Node-local storage==

Each job receives a private temporary directory, $SLURM_TMPDIR, on the compute node's local NVMe drives. It is much faster than the shared file systems. Copy your input data there at the start of a job, and copy your results back to /scratch or /project before the job ends.

$SLURM_TMPDIR is not backed up and has no redundancy. Its contents are deleted when the job ends, and a single drive failure can destroy them during the job.

=Network interconnects=

Each node has a dedicated GPU network of 8 x 400 Gbps Ethernet ports (one NVIDIA ConnectX-7 per GPU) with RoCE v2 (RDMA over Converged Ethernet) enabled. General networking and storage traffic use an NVIDIA BlueField-3 dual-port 200 Gbps Ethernet adapter.

=Scheduling=

The Rocky cluster uses the Slurm scheduler to run user workloads. The basic scheduling commands are similar to those on the other national clusters.

You do not need to choose a partition. Request a walltime with --time, and Slurm places your job in the partition that matches that walltime. Jobs submitted without a walltime default to 1 hour. An interactive partition allows jobs of up to 8 hours.

To request GPUs, specify the type h200, for example:

#SBATCH --gres=gpu:h200:1

A job only sees the GPUs it requested.

=Software=

* Module-based software stack.
* The standard Alliance software stack is available through CVMFS.