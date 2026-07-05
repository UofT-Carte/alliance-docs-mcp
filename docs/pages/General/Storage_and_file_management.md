---
title: "Storage and file management/en"
url: "https://docs.alliancecan.ca/wiki/Storage_and_file_management/en"
category: "General"
last_modified: "2026-06-22T15:47:23Z"
page_id: 3195
display_title: "Storage and file management"
---

==Overview==

We provide a wide range of storage options to cover the needs of our very diverse users. These storage solutions range from high-speed temporary local storage to different kinds of long-term storage, so you can choose the storage medium that best corresponds to your needs and usage patterns. In most cases the filesystems on our systems are a shared resource and for this reason should be used responsibly because unwise behaviour can negatively affect dozens or hundreds of other users. These filesystems are also designed to store a limited number of very large files, which are typically binary since very large (hundreds of MB or more) text files lose most of their interest in being readable by humans. You should therefore avoid storing tens of thousands of small files, where small means less than a few megabytes, particularly in the same directory. A better approach is to use commands like tar or zip to convert a directory containing many small files into a single very large archive file.

It is also your responsibility to manage the age of your stored data: most of the filesystems are not intended to provide an indefinite archiving service so when a given file or directory is no longer needed, you need to move it to a more appropriate filesystem which may well mean your personal workstation or some other storage system under your control. Moving significant amounts of data between your workstation and one of our systems or between two of our systems should generally be done using Globus.

Note that our storage systems are not for personal use and should only be used to store research data.

When your account is created on a cluster, your home directory will not be entirely empty. It will contain references to your scratch and project spaces through the mechanism of a symbolic link, a kind of shortcut that allows easy access to these other filesystems from your home directory. Note that these symbolic links may appear up to a few hours after you first connect to the cluster. While your home and scratch spaces are unique to you as an individual user, the project space is shared by a research group. This group may consist of those individuals with an account sponsored by a particular faculty member or members of a RAC allocation. A given individual may thus have access to several different project spaces, associated with one or more faculty members, with symbolic links to these different project spaces in the directory projects of your home. Every account has one or many projects. In the folder projects within their home directory, each user has a link to each of the projects they have access to. For users with a single active sponsored role, it is the default project of your sponsor while users with more than one active sponsored role will have a default project that corresponds to the default project of the faculty member with the most sponsored accounts.

All users can check the available disk space and the current disk utilization for the project, home and scratch filesystems with the command line utility diskusage_report, available on our clusters. To use this utility, log into the cluster using SSH, at the command prompt type diskusage_report, and press the Enter key. Below is a typical output of this utility:

# diskusage_report
                   Description                Space           # of files
                 Home (username)         280 kB/47 GB              25/500k
              Scratch (username)         4096 B/18 TB              1/1000k
       Project (def-username-ab)       4096 B/9536 GB              2/500k
          Project (def-username)       4096 B/9536 GB              2/500k

More detailed output is available using the Diskusage Explorer tool.

== Storage types ==
Unlike your personal computer, our systems will typically have several storage spaces or filesystems and you should ensure that you are using the right space for the right task. In this section we will discuss the principal filesystems available on most of our systems and the intended use of each one along with some of its characteristics.
* HOME: While your home directory may seem like the logical place to store all your files and do all your work, in general this isn't the case; your home normally has a relatively small quota and doesn't have especially good performance for writing and reading large amounts of data. The most logical use of your home directory is typically source code, small parameter files and job submission scripts.
* PROJECT: The project space has a significantly larger quota and is well adapted to  sharing data among members of a research group since it, unlike the home or scratch, is linked to a professor's account rather than an individual user. The data stored in the project space should be fairly static, that is to say the data are not likely to be changed many times in a month. Otherwise, frequently changing data, including just moving and renaming directories, in project can become a heavy burden on the tape-based backup system.
* SCRATCH: For intensive read/write operations on large files (> 100 MB per file), scratch is the best choice. However, remember that important files must be copied off scratch since they are not backed up there, and older files are subject to purging. The scratch storage should therefore be used for temporary files: checkpoint files, output from jobs and other data that can easily be recreated. Do not regard SCRATCH as your normal storage!  It is for transient files that you can afford to lose.
* NEARLINE: Nearline is a tape-based filesystem intended for inactive data. Datasets which you do not expect to access for months are good candidates to be stored in /nearline. For more information, see Using nearline storage.
* SLURM_TMPDIR: While a job is running, the environment variable $SLURM_TMPDIR holds a unique path to a temporary folder on a fast, local filesystem on each compute node allocated to the job. When the job ends, the directory and its contents are deleted, so $SLURM_TMPDIR should be used for temporary files that are only needed for the duration of the job. Its advantage, compared to the other networked filesystem types above, is increased performance due to the filesystem being local to the compute node. It is especially well-suited for large collections of small files (for example, smaller than a few megabytes per file). Note that this filesystem is shared between all jobs running on the node, and that the available space depends on the compute node type. A more detailed discussion of using $SLURM_TMPDIR is available at  this page.

==Project space consumption per user==

While the command diskusage_report gives the space and file count usage per user on home and scratch, it shows the total quota of the group on project. It includes all the files from each member of the group. Since the files that belong to a user could however be anywhere in the project space, it is difficult to obtain correct figures per user and per given project in case a user has access to more than one project. However, users can obtain an estimate of their space and file count use on the entire project space by running the command

lfs quota -u $USER /project

In addition to that, users can obtain an estimate for the number of files in a given directory (and its subdirectories) using the command lfs find, e.g.

lfs find  -type f | wc -l

== Best practices ==
* Regularly clean up your data in the scratch and project spaces, because those filesystems are used for huge data collections.
** Document your files with README files.
** For any set of files that could be deleted:
**# Create a temporary directory toDelete
**# Move the files to be deleted to this directory
**# Verify the contents of toDelete
**# Delete toDelete recursively.
** If possible, avoid using * and / characters in your rm commands.
*** Navigate to the parent directory that contains the item(s) to be deleted. Double-check you are in the correct directory.
*** If the directory has a Makefile, it may use * and / in rm commands, but these commands have to be well tested.
** In shell scripts, if environment variables are used in rm commands, each variable has to be tested before use: empty or undefined variables can cause catastrophic errors, and any input value has to be checked against malicious or erroneous use of the script.
* Only use text format for files that are smaller than a few megabytes.
* As far as possible, use scratch and local storage for temporary files. For local storage you can use the temporary directory created by the job scheduler for this, named $SLURM_TMPDIR.
* If your program must search within a file, it is fastest to do it by first reading it completely before searching.
* If you no longer use certain files but they must be retained, archive and compress them, and if possible move them to an alternative location like nearline.
* For more on managing many files, see Handling large collections of files, especially if you are limited by a quota on the number of files.
* Having any sort of parallel write access to a file stored on a shared filesystem like home, scratch and project is likely to create problems unless you are using a specialized tool such as MPI-IO.
* If your needs are not well served by the available storage options please contact technical support.

==Filesystem quotas and policies==

In order to ensure that there is adequate space for all users, there are a variety of quotas and policy restrictions concerning backups and automatic purging of certain filesystems.
By default on our clusters, each user has access to the home and scratch spaces, and each group has access to 1 TB of project space. Small increases in project and scratch spaces are available through our Rapid Access Service. Larger increases in project spaces are available through the annual Resource Allocation Competition. You can see your current quota usage for various filesystems on our clusters using the command diskusage_report.

Filesystem Characteristics

Filesystem    	Default Quota                                                                                                                                                                                                                                                                                                                                         	Lustre-based	Backed up	Purged                                                                              	Available by Default	Mounted on Compute Nodes
Home Space    	50 GB and 500K files per userThis quota is fixed and cannot be changed.                                                                                                                                                                                                                                                                               	Yes         	Yes      	No                                                                                  	Yes                 	Yes
Scratch Space 	20 TB and 1M files per user                                                                                                                                                                                                                                                                                                                           	Yes         	No       	Files older than 60 days are purged.See Scratch purging policy for more information.	Yes                 	Yes
Project Space 	1 TB and 500K files per groupProject space can be increased to 40 TB per group by a RAS request, subject to the limitations that the minimum project space per quota cannot be less than 1 TB and the sum over all four general-purpose clusters cannot exceed 43 TB. The group's sponsoring PI should write to technical support to make the request.	Yes         	Yes      	No                                                                                  	Yes                 	Yes
Nearline Space	2 TB and 5000 files per groupNearline space can be increased to 100 TB per group by a RAS request, summed over all four general-purpose clusters. The group's sponsoring PI should write to technical support to make the request.                                                                                                                    	Yes         	Yes      	No                                                                                  	Yes                 	No

Since April 1, 2024, new Rapid Access Service (RAS) policies allow larger quotas for the project and nearline spaces. For more details, see the "Storage" section at Rapid Access Service.  Quota changes larger than those permitted by RAS will require an application to the annual Resource Allocation Competition.

Filesystem Characteristics

Filesystem    	Default Quota                                                                                                                                                                                                                                                                                                                                                                                                               	Lustre-based	Backed up	Purged	Available by Default	Mounted on Compute Nodes
Home Space    	50 GB and 500K files per userThis quota is fixed and cannot be changed.                                                                                                                                                                                                                                                                                                                                                     	No          	Yes      	No    	Yes                 	Yes
Scratch Space 	20 TB hard / 1TB soft and 1M files per userA 1 TB soft quota on scratch applies to each user. A "soft quota" means you may temporarily exceed the 1 TB limit for up to 60 days; after this period, no additional files may be written to scratch. Files may be written again once the user has removed or deleted enough files to bring their total scratch use under 1 TB. See Scratch purging policy for more information.	No          	No       	No    	Yes                 	Yes
Project Space 	1 TB and 500K files per groupProject space can be increased to 40 TB per group by a RAS request, subject to the limitations that the minimum project space per quota cannot be less than 1 TB and the sum over all four general-purpose clusters cannot exceed 43 TB. The group's sponsoring PI should write to technical support to make the request.                                                                      	No          	Yes      	No    	Yes                 	Yes
Nearline Space	10 TB and 5000 files per groupNearline space can be increased to 100 TB per group by a RAS request, summed over all four general-purpose clusters. The group's sponsoring PI should write to technical support to make the request.                                                                                                                                                                                         	Yes         	Yes      	No    	Yes                 	No

Since April 1, 2024, new Rapid Access Service (RAS) policies allow larger quotas for project and nearline spaces. For more details, see the "Storage" section at Rapid Access Service.  Quota changes larger than those permitted by RAS will require an application to the annual Resource Allocation Competition.

Filesystem Characteristics

Filesystem    	Default Quota                                                                                                                                                                                                                                                                                                                                         	Lustre-based	Backed up	Purged                                                                              	Available by Default	Mounted on Compute Nodes
Home Space    	50 GB and 500K files per userThis quota is fixed and cannot be changed.                                                                                                                                                                                                                                                                               	Yes         	Yes      	No                                                                                  	Yes                 	Yes
Scratch Space 	20 TB and 1M files per user                                                                                                                                                                                                                                                                                                                           	Yes         	No       	Files older than 60 days are purged.See Scratch purging policy for more information.	Yes                 	Yes
Project Space 	1 TB and 500K files per groupProject space can be increased to 40 TB per group by a RAS request, subject to the limitations that the minimum project space per quota cannot be less than 1 TB and the sum over all four general-purpose clusters cannot exceed 43 TB. The group's sponsoring PI should write to technical support to make the request.	Yes         	Yes      	No                                                                                  	Yes                 	Yes
Nearline Space	1 TB and 5000 files per groupNearline space can be increased to 100 TB per group by a RAS request, summed over all four general-purpose clusters. The group's sponsoring PI should write to technical support to make the request.                                                                                                                    	Yes         	Yes      	No                                                                                  	Yes                 	No

Since April 1, 2024, new Rapid Access Service (RAS) policies allow larger quotas for project and nearline spaces. For more details, see the "Storage" section at Rapid Access Service.  Quota changes larger than those permitted by RAS will require an application to the annual Resource Allocation Competition.

Filesystem Characteristics

Location	Quota                                                                 	Expiration Time	Backed Up	On Login Nodes	On Compute Nodes
$HOME   	100 GB and 1M files per user                                          	               	yes      	yes           	read-only
$SCRATCH	25 TB and 10M files per user                                          	TBD            	no       	yes           	yes
$PROJECT	by RRG or RPP allocation, and 1 TB and 2M files per default allocation	               	yes      	yes           	read-only
$ARCHIVE	by RRG or RPP allocation                                              	               	dual-copy	no            	no

Compute nodes do not have local storage.
Archive (a.k.a. nearline) space is on HPSS
Backup means a recent snapshot, not an archive of all data that ever was.

Filesystem Characteristics

Location	Quota                                        	Quota          	Expiration Time	Backed Up	On Login Nodes	On Compute Nodes
$HOME   	50 GB per user                               	50 GB per user 	none           	yes      	yes           	yes
$SCRATCH	CIFAR AI Chairs                              	2 TB per user  	2 months       	no       	yes           	yes
$SCRATCH	AI Institute Faculty Affiliates              	1 TB per user  	2 months       	no       	yes           	yes
$SCRATCH	Faculty members, within an AI program        	500 GB per user	2 months       	no       	yes           	yes
$SCRATCH	Faculty members, applying AI to other domains	250 GB per user	2 months       	no       	yes           	yes
$PROJECT	CIFAR AI Chairs                              	5 TB           	none           	yes      	yes           	yes
$PROJECT	AI Institute Faculty Affiliates              	2 TB           	none           	yes      	yes           	yes
$PROJECT	Faculty members, within an AI program        	1 TB           	none           	yes      	yes           	yes
$PROJECT	Faculty members, applying AI to other domains	500 GB         	none           	yes      	yes           	yes

All filesystems are served from VastData storage
Backup means a recent snapshot, not an archive of all data that ever was.
See Scratch purging policy for more information on expiration time.

Filesystem Characteristics

Location	Quota                                        	Quota          	Expiration Time	Backed Up	On Login Nodes	On Compute Nodes
$HOME   	25 GB per user                               	25 GB per user 	none           	no       	yes           	yes
$SCRATCH	CIFAR AI Chairs                              	2 TB per user  	2 months       	no       	yes           	yes
$SCRATCH	AI Institute Faculty Affiliates              	1 TB per user  	2 months       	no       	yes           	yes
$SCRATCH	Faculty members, within an AI program        	500 GB per user	2 months       	no       	yes           	yes
$SCRATCH	Faculty members, applying AI to other domains	500 GB per user	2 months       	no       	yes           	yes
$PROJECT	CIFAR AI Chairs                              	5 TB           	none           	no       	yes           	yes
$PROJECT	AI Institute Faculty Affiliates              	2 TB           	none           	no       	yes           	yes
$PROJECT	Faculty members, within an AI program        	500 GB         	none           	no       	yes           	yes
$PROJECT	Faculty members, applying AI to other domains	500 GB         	none           	no       	yes           	yes

See Scratch purging policy for more information on expiration time.

Filesystem Characteristics

Location	Quota                                        	Quota         	Expiration Time	Backed Up	On Login Nodes	On Compute Nodes
$HOME   	50 GB per user                               	50 GB per user	none           	yes      	yes           	yes
$SCRATCH	CIFAR AI Chairs                              	5 TB per user 	2 months       	no       	yes           	yes
$SCRATCH	AI Institute Faculty Affiliates              	5 TB per user 	2 months       	no       	yes           	yes
$SCRATCH	Faculty members, within an AI program        	5 TB per user 	2 months       	no       	yes           	yes
$SCRATCH	Faculty members, applying AI to other domains	5 TB per user 	2 months       	no       	yes           	yes
$PROJECT	CIFAR AI Chairs                              	12.5 TB       	none           	yes      	yes           	yes
$PROJECT	AI Institute Faculty Affiliates              	10 TB         	none           	yes      	yes           	yes
$PROJECT	Faculty members, within an AI program        	7.5 TB        	none           	yes      	yes           	yes
$PROJECT	Faculty members, applying AI to other domains	5 TB          	none           	yes      	yes           	yes

See Scratch purging policy for more information on expiration time.

The backup policy on the home and project space is nightly backups which are retained for 30 days, while deleted files are retained for a further 60 days; note that is entirely distinct from the age limit for purging files from the scratch space. If you wish to recover a previous version of a file or directory, you should contact technical support with the full path for the file(s) and desired version (by date).

== See also ==

* Diskusage Explorer
* Project layout
* Using nearline storage
* Sharing data
* Transferring data
* Tuning Lustre
* Archiving and compressing files
* Handling large collections of files
* Parallel I/O introductory tutorial