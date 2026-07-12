---
title: "Fir"
url: "https://docs.alliancecan.ca/wiki/Fir"
category: "General"
last_modified: "2026-07-03T12:45:22Z"
page_id: 26935
display_title: "Fir"
---

Availability date: August 11, 2025
Login node: fir.alliancecan.ca
Automation node: robot.fir.alliancecan.ca
Globus collection: alliancecan#fir-globus
JupyterHub: jupyterhub.fir.alliancecan.ca
Data transfer node (rsync, scp, sftp ...): to be determined
Portal: to be determined

Fir is a versatile, heterogeneous computing cluster built in partnership with Lenovo Canada and Data Direct Networks (DDN) and is designed to support a wide range of scientific computations. It is hosted at Simon Fraser University (SFU) in Burnaby, British Columbia, and is named after the Red Creek Fir—the largest known Douglas fir tree on Earth by volume.

=About Fir=

SFU remains committed to environmentally sustainable high-performance computing. With Fir, the university is transitioning from traditional air cooling to advanced direct-to-chip liquid cooling, significantly improving energy efficiency and reducing power consumption associated with cooling.

The new high-speed InfiniBand network in Fir delivers more than twice the performance of the previous-generation Cedar cluster.

Fir is ranked #78 on the June 2025 TOP500 list of the world’s most powerful supercomputers.

=Access=

Each researcher must request access in CCDB, via Resources--> Access Systems.

Select Fir from the list on the left.

Select I request access.

It can take up to one hour for your access to be enabled.

=Site-specific policies=

Fir's compute nodes have full access to the internet.

The crontab tool is not supported.

Each job should have a duration of at least one hour (at least five minutes for test jobs) and the maximum job duration is 7 days (168 hours).

For transferring data via Globus, use the endpoint specified at the top of this page; for tools like rsync and scp, please use the login node.

Visual Studio Code is blocked on the Fir login nodes.

=Storage=

51PB high-performance DDN Lustre storage (2PB NVME / 49 SAS).

Storage Area	Access Path                    	Quotas                                	Backup                	Notes
HOME        	Default $HOME                  	Small per-user quota                  	Daily automatic backup	Cannot be increased; use `/project for larger storage
SCRATCH     	$HOME/scratch                  	Large per-user quota                  	No backup             	For temporary files; old files are purged automatically
PROJECT     	$HOME/project/${def-project-id}	Large and adjustable per-project quota	Daily backup          	For group data sharing and large datasets

=High-performance interconnect=

* InfiniBand NDR interconnect
* CPU node island size, is 27:5 blocking factor over 216 nodes of 192 cores
* GPU nodes are 2:1 blocking factor
* Storage access is fully non-blocking

=Node characteristics=

nodes	cores	available memory 	CPU                                                 	Storage    	GPU
864  	192  	750G or 768000M  	2 x AMD EPYC 9655 (Zen 5) @ 2.7 GHz, 384MB cache L3 	7.84TB NVMe
8    	192  	6000G or 6144000M	2 x AMD EPYC 9654 (Zen 4) @ 2.4 GHz, 384MB cache L3 	7.84TB NVMe
160  	48   	1125G or 1152000M	1 x AMD EPYC 9454 (Zen 4) @ 2.75 GHz, 256MB cache L3	7.84TB NVMe	4 x NVidia H100 SXM5 (80 GB memory), connected via NVLink

==CPU nodes==

===Architecture===
Each node features 2 × AMD EPYC 9655 (Zen 5) @ 2.7 GHz processors, totaling 192 physical cores. The system is built on a chiplet-based NUMA architecture, where each chiplet (CCD) operates as a separate NUMA node. The memory and cache hierarchy is non-uniform, and performance is sensitive to data locality.

===Layout===

* 2 sockets, each with:
** 96 cores
** 4 NUMA nodes, each with:
*** 3 CCDs (chiplets), each with:
**** 8 cores
**** 32 MiB shared L3 cache
*** 3 memory channels

Each core with:
* 1 MiB L2 cache
* 32+32 KiB L1 instruction/data cache
* 12 DDR5 memory channels (shared via the I/O die)

Total:
* 8 NUMA nodes per node (4 per socket × 2)
* 24 CCDs (chiplets) per node (12 per socket  × 2)
* 192 cores total
* 768 MiB L3 cache total

===Performance tuning recommendations===

To make best use of the EPYC 9655's architecture:

1. Align tasks to CCDs
Each CCD contains 8 tightly-coupled cores with shared L3 cache. Keeping threads within a CCD avoids inter-chiplet communication latency.

Use:#SBATCH --cpus-per-task=8

This ensures that threads of each task stay within a single CCD.

2. Distribute tasks across CCDs

With 24 CCDs per node, launch 24 tasks per node to fully utilize all CCDs without overloading any single one.

Use:#SBATCH --ntasks-per-node=24

Together with --cpus-per-task=8, this fills the full 192-core node cleanly.

==GPU nodes==

===Architecture===
Each GPU node contains 1 × AMD EPYC 9454 (Zen 4) @ 2.75 GHz processor with 48 physical cores. This processor uses AMD’s chiplet-based NUMA architecture, with memory access times that vary depending on core and memory locality. GPU nodes use the NPS=4 mode (NUMA Per Socket), dividing the socket into four NUMA nodes for better memory locality.

===Layout===

* 1 socket, configured as NPS=4:
** 4 NUMA nodes, each with
*** 2 CCDs (Core Complex Dies), each with
**** 6 cores
**** 32 MiB of shared L3 cache
*** 3 memory channels

Each core has:
* 1 MiB L2 cache
* 32 KiB L1 instruction cache
* 32 KiB L1 data cache
* 12 DDR5 memory channels (shared via the I/O die)

* 2 NVidia H100 80GB accelerators
** The 4 node accelerators are interconnected by SXM5.

===Performance tuning recommendations===

To fully utilize the architecture of the EPYC 9454 CPU and ensure optimal CPU-GPU data locality:

1. Bind threads to CCDs

Each CCD has 6 closely coupled cores sharing a 32 MiB L3 cache. To keep threads within a CCD: #SBATCH --cpus-per-task=6

This confines threads to one CCD, reducing cross-CCD latency and improving cache usage.

2. Match Tasks to NUMA Nodes
With 4 NUMA nodes per socket (NPS=4), launch 4 tasks per node (or a multiple thereof) for best performance:

#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=12

This keeps each task within a NUMA domain and ensures local access to memory and the GPU.

===GPU instances===

To request one or more full H100 GPUs, you need to use one of the following Slurm options:

One H100-80gb : --gpus=h100:1

Multiple H100-80gb per node :
* --gpus-per-node=h100:2
* --gpus-per-node=h100:3
* --gpus-per-node=h100:4

For multiple full H100 GPUs spread anywhere: --gpus=h100:n (replace n with the number of GPUs you want)

Approximately half of the GPU nodes are configured with MIG technology, and only 3 GPU instance sizes are available:

* 1g.10gb: 1/8th of the computing power with 10GB GPU memory
* 2g.20gb: 2/8th of the computing power with 20GB GPU memory
* 3g.40gb: 3/8th of the computing power with 40GB GPU memory

To request one and only one GPU instance for your compute job, use the corresponding option:

* 1g.10gb : --gpus=nvidia_h100_80gb_hbm3_1g.10gb:1
* 2g.20gb : --gpus=nvidia_h100_80gb_hbm3_2g.20gb:1
* 3g.40gb : --gpus=nvidia_h100_80gb_hbm3_3g.40gb:1