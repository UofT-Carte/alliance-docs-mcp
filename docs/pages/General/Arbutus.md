---
title: "Arbutus/en"
url: "https://docs.alliancecan.ca/wiki/Arbutus/en"
category: "General"
last_modified: "2026-10-09T17:22:16Z"
page_id: 27302
display_title: "Arbutus"
---

Availability: late spring 2026
OpenStack dashboard: https://arbutus.alliancecan.ca
Globus endpoint: to be determined
Object Storage (S3 or Swift): https://object-arbutus.alliancecan.ca/:/

Arbutus is an Infrastructure-as-a-Service cloud hosted at the University of Victoria.

==Storage==
7 PB of Volume and Snapshot Ceph storage.
26 PB of Object/Shared Filesystem Ceph storage.
3 PB of NVMe Volume and Snapshot Ceph storage.

==Node characteristics==

nodes	cores	available memory	storage             	CPU                                          	GPU
338  	96   	768GB DDR5      	1 x NVMe SSD, 7.68TB	2 x Intel Platinum 8568Y+ 2.3GHz, 300MB cache
22   	96   	1536GB DDR5     	1 x NVMe SSD, 7.68TB	2 x Intel Platinum 8568Y+ 2.3GHz, 300MB cache
11   	64   	2048GB DDR5     	1 x NVMe SSD, 7.68TB	2 x Intel Platinum 6548Y+ 2.5GHz, 60MB cache
16   	48   	1024GB DDR4     	1 x NVMe SSD, 3.84TB	2 x Intel Gold 6342 2.8 GHz, 36MB cache      	4 x NVidia H100 PCIe Gen5 (94GB)
10   	48   	128GB DDR5      	1 x NVMe SSD, 3.84TB	2 x Intel Gold 6542Y 2.9 GHz, 60MB cache     	1 x NVidia L40s PCIe Gen4 (48GB)

See  Cloud resources for current equipment summary.