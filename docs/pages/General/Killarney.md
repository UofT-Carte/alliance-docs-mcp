---
title: "Killarney"
url: "https://docs.alliancecan.ca/wiki/Killarney"
category: "General"
last_modified: "2026-11-09T20:12:50Z"
page_id: 27762
display_title: "Killarney"
---

Availability: June 9, 2025
Login node: killarney.alliancecan.ca
Open OnDemand: https://ondemand.killarney.vectorinstitute.ai
Globus collection: TBA
System Status Page: https://status.alliancecan.ca/system/Killarney

Killarney is a cluster dedicated to the needs of the Canadian scientific Artificial Intelligence community. Killarney is located at the University of Toronto and is managed by the Vector Institute  and SciNet. It is named after the Killarney Ontario Provincial Park, located near Georgian Bay.

This cluster is part of the Pan-Canadian AI Compute Environment (PAICE).

==Site-specific policies==
Killarney is currently open to Vector affiliated PIs with CCAI Chairs, as well as researchers within an AI program at a Canadian university, or applying AI methods for their research.

Killarney remote filesystems (/home, /scratch, etc) are mounted using NFS v3, which does not support ACLs; as such, commands such as setfacl are not supported. If you need to share data with users outside of your group, please email ops-help@vectorinstitute.ai requesting a shared directory be created.

==Access==
Principal Investigators must first be granted an AIP-type RAP (prefix aip- ) by their AI Institution,
or by applying for General Access to PAICE Systems.

To sponsor researchers in their AIP RAP, the PI must:
# In the Resource Allocation Projects table on the CCDB home page, click on the RAPI project to display the RAP management page.
# At the top of the RAP management page, click on Manage RAP memberships.
# in the Add Members section, enter the CCRI of the users you want to add.

Once members are registered by the PI, they must request access in the CCDB, and have at least one SSH key in CCDB

To ensure integrity and security, Vector enforces geo-blocking on Killarney as one of its cyber-security controls. Vector restricts access to and from countries identified in the Government of Canada's Cyber Threat Assessment.

==Killarney hardware specifications==

Performance Tier   	Nodes	Model      	CPU                      	Cores	System Memory	Storage    	GPUs per node           	Total GPUs
Standard Compute   	168  	Dell 750xa 	2 x Intel Xeon Gold 6338 	64   	512 GB       	350 GB SSD 	4 x NVIDIA L40S 48GB    	672
Performance Compute	10   	Dell XE9680	2 x Intel Xeon Gold 6442Y	48   	2048 GB      	800 GB NVMe	8 x NVIDIA H100 SXM 80GB	80

==Storage system==

Killarney's storage system is an all-NVME VastData platform with a total usable capacity of 1.7PB.

Home space
* Location of /home directories.
* Each /home directory has a small fixed quota.
* Larger requests go to the /project space.
* Has daily backup
Scratch space
* For active or temporary (scratch) storage.
* Large fixed quota per user.
* Inactive data will be purged.
Project space
* Large adjustable quota per project.
* Has daily backup.

==Network interconnects==

Standard Compute nodes are interconnected with Infiniband HDR100 for 100Gbps throughput, while Performance Compute nodes are connected with 2 x HDR 200 for 400Gbps aggregate throughput.

==Scheduling==
The Killarney cluster uses the Slurm scheduler to run user workloads. The basic scheduling commands are similar to the other national systems.

==Software==
* Module-based software stack.
* Both the standard Alliance software stack as well as cluster-specific software.