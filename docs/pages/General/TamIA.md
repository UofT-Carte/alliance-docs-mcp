---
title: "TamIA/en"
url: "https://docs.alliancecan.ca/wiki/TamIA/en"
category: "General"
last_modified: "2026-07-13T20:36:33Z"
page_id: 28130
display_title: "TamIA"
---

Availability : March 31, 2025
Login node : tamia.alliancecan.ca
Automation node : robot.tamia.ecpia.ca
Globus collection : TamIA's Globus v5 Server
Data transfer node (rsync, scp, sftp,...) : tamia.alliancecan.ca
Portal : https://portail.tamia.ecpia.ca/

tamIA is a cluster dedicated to artificial intelligence for the Canadian scientific community. Located at Université Laval, tamIA is co-managed with Mila and Calcul Québec. The cluster is named for the eastern chipmunk, a common species found in eastern North America.

tamIA is part of , the Pan-Canadian AI Compute Environment].

==Site-specific policies==

* By policy, tamIA's compute nodes cannot access the internet. If you need an exception to this rule, contact technical support explaining what you need and why.
* crontab is not offered on tamIA.
* Please note that the VSCode IDE is forbidden on the login nodes due to its heavy footprint. It is still authorized on the compute nodes.
* Each job should be at least one hour long (at least five minutes for test jobs) and you can't have more than 1000 jobs (running and pending) at the same time.
* The maximum duration of a job is one day (24 hours).
* Each job must use all 4 GPUs of the servers allocated, i.e. 4 with H100 and 8 with H200.

==Access==
To access the cluster, each researcher must complete an access request in the CCDB portal under Resources-->Artificial Intelligence-->tamIA. Access to the cluster may take up to one hour after the access request is sent.
You must then submit the General Access to PAICE Systems declaration form.

Eligible principal investigators are members of an AIP-type RAP (prefix aip-).

The procedure for sponsoring other researchers is as follows:
* On the CCDB home page, go to the Resource Allocation Projects table
* Look for the RAPI of the aip- project and click on it to be redirected to the RAP management page
* At the bottom of the RAP management page, click on Manage RAP memberships
* To add a new member, go to Add Members and enter the CCRI of the user you want to add.

The cluster can only be reached from Canada.

==Storage==

HOME  Lustre file system

* Location of home directories, each of which has a small fixed quota.
* You should use the project space for larger storage needs.
* Small per user quota.
* There is currently no backup of the home directories. (ETA Spring 2026)
SCRATCH  Lustre file system

* Large space for storing temporary files during computations
* No backup system in place
* Large quota per user
* There is an automated purge of older files in this space.
PROJECT  Lustre file system

* This space is designed for sharing data among the members of a research group and for storing large amounts of data.
* Large and adjustable per group quota.
* There is currently no backup of the home directories. (ETA Summer 2025)

For transferring data via Globus, you should use the endpoint specified at the top of this page, while for tools like rsync and scp you can use a login node.

==High-performance interconnect==
The InfiniBand NVIDIA NDR network links together all of the nodes of the cluster. Each GPU is connected to a single NDR200 port through an NVIDIA ConnectX-7 HCA. Eeach GPU server has 4 or 8 NDR200 ports connected to the InfiniBand fabric.

The InfiniBand network is non-blocking for compute servers and is composed of two levels of switches in a fat-tree topology. Storage and compute nodes are connected via 4 or 8 400Gb/s connections to the network core.

==Node characteristics==

nodes	cores	available memory	CPU                                    	storage       	GPU
12   	64   	1024GB          	2 x Intel Xeon Gold 6448Y 2,1 GHz, 32C 	1 x 7.68TB SSD	8 x NVIDIA HGX H200 SXM 141GB HBM3 700W, connected via NVLink
53   	48   	512GB           	2 x Intel Xeon Gold 6442Y 2,6 GHz, 24C 	1 x 7.68TB SSD	4 x NVIDIA HGX H100 SXM 80GB HBM3 700W, connected via NVLink
8    	64   	512GB           	2 x Intel Xeon Gold 6438M 2.2G, 32C/64T	1 x 7.68TB SSD	none

===Software environments===
StdEnv/2023 is the standard environment on tamIA.

=== GPU jobs ===
Jobs are assigned on whole nodes with one of the following options:

For jobs on a node with an H100 GPU: --gpus=h100:4

For jobs on a node with an H200 GPU: --gpus=h200:8

For jobs using several GPUs, options are --gpus-per-nodes=h100:4 or --gpus-per-nodes=h200:8.

==Monitoring jobs==

From the tamIA portal, you can monitor your jobs using CPUs and GPUs in real time or examine jobs that have run in the past. This can help you to optimize resource usage and shorten wait time in the queue.

You can monitor your usage of
* compute nodes,
* memory,
* GPU.

It is important that you use the allocated resources and to correct your requests when compute resources are less used or not used at all. For example, if you request 4 cores (CPUs) but use only one, you should adjust the script file accordingly.