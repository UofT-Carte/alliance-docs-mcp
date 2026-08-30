---
title: "Accessing CVMFS"
url: "https://docs.alliancecan.ca/wiki/Accessing_CVMFS"
category: "General"
last_modified: "2026-08-28T22:42:30Z"
page_id: 11068
display_title: "Accessing CVMFS"
---

= Introduction =
We provide repositories of software and data via a file system called the CERN Virtual Machine File System (CVMFS). On our systems, CVMFS is already set up for you, so the repositories are automatically available for your use. For more information on using our software environment, please refer to wiki pages Available software, Using modules, Python, R and Installing software in your home directory.

The purpose of this page is to describe how you can install and configure CVMFS on your computer or cluster, so that you can access the same repositories (and software environment) on your system that are available on ours.

The software environment described on this page has been presented at Practices and Experience in Advanced Research Computing 2019 (PEARC 2019).

= Before you start =

== Subscribe to announcements ==
Occasionally, changes will be made regarding CVMFS or the software or other content provided by our CVMFS repositories, which may affect users or require administrators to take action in order to ensure uninterrupted access to our CVMFS repositories. Subscribe to the cvmfs-announce@gw.alliancecan.ca mailing list in order to receive important but infrequent notifications about these changes, by emailing cvmfs-announce+subscribe@gw.alliancecan.ca and then replying to the confirmation email you subsequently receive. (Our staff can alternatively subscribe here.)

== Terms of use and support ==
The CVMFS client software is provided by CERN. Our CVMFS repositories are provided without any warranty. We reserve the right to limit or block your access to the CVMFS repositories and software environment if you violate applicable terms of use or at our discretion.

== CVMFS requirements ==
=== For a single system ===
To install CVMFS on an individual system, such as your laptop or desktop, you will need:
* A supported operating system (see Minimal requirements below).
* Support for FUSE.
* Approximately 50 GB of available local storage, for the cache. (It will only be filled based on usage, and a larger or smaller cache may be suitable in different situations. For light use on a personal computer, just ~ 5-10 GB may suffice. See cache settings for more details.)
* Outbound HTTP access to the internet.
** Or at least outbound HTTP access to one or more local proxy servers.

If your system lacks FUSE support or local storage, or has limited network connectivity or other restrictions, you may be able to use some other option.

=== For multiple systems ===
If multiple CVMFS clients are deployed, for example on a cluster, in a laboratory, campus or other site, each system must meet the above requirements, and the following considerations apply as well:
* We recommend that you deploy forward caching HTTP proxy servers at your site to improve performance and bandwidth usage, especially if you have a large number of clients. Refer to Setting up a Local Squid Proxy.
** Note that if you have only one such proxy server it will be a single point of failure for your site. Generally, you should have at least two local proxies at your site, and potentially additional nearby or regional proxies as backups.
* It is recommended to synchronize the identity of the cvmfs service account across all client nodes (e.g. using LDAP or other means).
** This facilitates use of an alien cache and should be done before CVMFS is installed. Even if you do not anticipate using an alien cache at this time, it is easier to synchronize the accounts initially than to try to potentially change them later.

== Software environment requirements ==
=== Minimal requirements ===
*Supported operating systems:
** Linux: with a Kernel 2.6.32 or newer for our 2016 and 2018 environments, and 3.2 or newer for the 2020 environment.
** Windows: with Windows Subsystem for Linux version 2, with a distribution of Linux that matches the requirement above.
** Mac OS: only through a virtual machine.
* CPU: x86 CPU supporting at least one of SSE3, AVX, AVX2 or AVX512 instruction sets.

=== Optimal requirements ===
* Scheduler: Slurm or Torque, for tight integration with OpenMPI applications.
* Network interconnect: Ethernet, InfiniBand or OmniPath, for parallel applications.
* GPU: NVidia GPU with CUDA drivers (7.5 or newer) installed, for CUDA-enabled applications. (See below for caveats about CUDA.)
* As few Linux packages installed as possible (fewer packages reduce the odds of conflicts).

= Installing CVMFS =
If you wish to use Ansible, a CVMFS client role is provided as-is, for basic configuration of a CVMFS client on an RPM-based system.
Also, some scripts may be used to facilitate installing CVMFS on cloud instances.
Otherwise, use the following instructions.

== Pre-installation ==
It is recommended that the local CVMFS cache (located at /var/lib/cvmfs by default, configurable via the CVMFS_CACHE_BASE setting) be on a dedicated file system so that the storage usage of CVMFS is not shared with that of other applications. Accordingly, you should provision that file system before installing CVMFS.

== Installation and configuration ==
For installation instructions, refer to Getting the Software.

For standard client configuration, see Setting up the Software and Client parameters.

The soft.computecanada.ca repository is provided by the default configuration, so no additional steps are required to access it (though you may wish to include it in CVMFS_REPOSITORIES in your client configuration).

== Testing ==

* First ensure that the repositories you want to test are listed in CVMFS_REPOSITORIES.
* Validate the configuration and test proxy-server connections:

* Make sure to address any warnings or errors that are reported.
* Check that the repositories are OK:

If you encounter problems, this debugging guide may help.

= Enabling our environment in your session =
Once you have mounted the CVMFS repository, enabling our environment in your sessions is as simple as running the bash script /cvmfs/soft.computecanada.ca/config/profile/bash.sh.
This will load some default modules. If you want to mimic a specific cluster exactly, simply define the environment variable CC_CLUSTER to one of fir, nibi or rorqual before using the script, for example:
rorqual}}

The above command will not run anything if your user ID is below 1000. This is a safeguard, because you should not rely on our software environment for privileged operation. If you nevertheless want to enable our environment, you can first define the environment variable FORCE_CC_CVMFS=1, with the command
1}}
or you can create a file $HOME/.force_cc_cvmfs in your home folder if you want it to always be active, with

If, on the contrary, you want to avoid enabling our environment, you can define SKIP_CC_CVMFS=1 or create the file $HOME/.skip_cc_cvmfs to ensure that the environment is never enabled in a given account.

== Customizing your environment ==
By default, enabling our environment will automatically detect a number of features of your system, and load default modules. You can control the default behaviour by defining specific environment variables prior to enabling the environment. These are described below.

=== Environment variables ===
==== CC_CLUSTER ====
This variable is used to identify a cluster. It is used to send some information to the system logs, as well as define behaviour relative to licensed software. By default, its value is computecanada. You may want to set the value of this variable if you want to have system logs tailored to the name of your system.

==== RSNT_ARCH ====
This environment variable is used to identify the set of CPU instructions supported by the system. By default, it will be automatically detected based on /proc/cpuinfo. However if you want to force a specific one to be used, you can define it before enabling the environment. The supported instruction sets for our software environment are:
* sse3
* avx
* avx2
* avx512

==== RSNT_INTERCONNECT ====
This environment variable is used to identify the type of interconnect supported by the system. By default, it will be automatically detected based on the presence of /sys/module/opa_vnic (for Intel OmniPath) or /sys/module/ib_core (for InfiniBand). The fall-back value is ethernet. The supported values are
* omnipath
* infiniband
* ethernet

The value of this variable will trigger different options of transport protocol to be used in OpenMPI.

==== RSNT_CUDA_DRIVER_VERSION ====
This environment variable is used to hide or show some versions of our CUDA modules, according to the required version of NVidia drivers, as documented [here]. If not defined, this is detected based on the files founds under /usr/lib64/nvidia.

For backward compatibility reasons, if no library is found under /usr/lib64/nvidia, we assume that the driver versions are enough for CUDA 10.2. This is because this feature was introduced just as CUDA 11.0 was released.

Defining RSNT_CUDA_DRIVER_VERSION=0.0 will hide all versions of CUDA.

==== RSNT_LOCAL_MODULEPATHS ====

if you want your module tree to have higher priority than ours, or

if you want your module tree to have lower priority than ours.
}}
This environment variable allows to define locations for local module trees, which will be automatically mesh into our central tree. To use it, define
/opt/software/easybuild/modules}}
and then install your EasyBuild recipe using

This will use our module naming scheme to install your recipe locally, and it will be picked up by the module hierarchy. For example, if this recipe was using the iompi,2018.3 toolchain, the module will become available after loading the intel/2018.3 and the openmpi/3.1.2 modules.

==== LMOD_SYSTEM_DEFAULT_MODULES ====
This environment variable defines which modules are loaded by default. If it is left undefined, our environment will define it to load the StdEnv module, which will load by default a version of the Intel compiler, and a version of OpenMPI.

==== MODULERCFILE ====
This is an environment variable used by Lmod to define the default version of modules and aliases. You can define your own modulerc file and add it to the environment variable MODULERCFILE. This will take precedence over what is defined in our environment.

=== System paths ===
While our software environment strives to be as independent from the host operating system as possible, there are a number of system paths that are taken into account by our environment to facilitate interaction with tools installed on the host operating system. Below are some of these paths.

==== /opt/software/modulefiles ====
If this path exists, it will automatically be added to the default MODULEPATH. This allows the use of our software environment while also maintaining locally installed modules.

==== $HOME/modulefiles ====
If this path exists, it will automatically be added to the default MODULEPATH. This allows the use of our software environment while also allowing installation of modules inside of home directories.

==== /opt/software/slurm/bin, /opt/software/bin, /opt/slurm/bin ====
These paths are all automatically added to the default PATH. This allows your own executable to be added in the search path.

== Installing software locally ==
Since June 2020, we support installing additional modules locally and have it discovered by our central hierarchy. This was discussed and implemented in this issue.

To do so, first identify a path where you want to install local software. For example /opt/software/easybuild. Make sure that folder exists. Then, export the environment variable RSNT_LOCAL_MODULEPATHS:
/opt/software/easybuild/modules}}

If you want this branch of the software hierarchy to be found by your users, we recommend you define this environment variable in the cluster's common profile. Then, install the software packages you want using EasyBuild:

This will install the piece of software locally, using the hierarchical layout driven by our module naming scheme. It will also be automatically found when users load our compiler, MPI and Cuda modules.

= Caveats =
== Use of software environment by system administrators ==
If you perform privileged system operations, or operations related to CVMFS, ensure that your session does not depend on our software environment when performing any such operations. For example, if you attempt to update CVMFS using YUM while your session uses a Python module loaded from CVMFS, YUM may run using that module and lose access to it during the update, and the update may become deadlocked. Similarly, if your environment depends on CVMFS and you reconfigure CVMFS in a way that temporarily interrupts access to CVMFS, your session may interfere with CVMFS operations, or hang. (When these precautions are taken, in most cases CVMFS can be updated and reconfigured without interrupting access to CVMFS for users, because the update or reconfiguration itself will complete successfully without encountering a circular dependency.)

== Software packages that are not available ==
On our systems, a number of commercial software packages are made available to authorized users according to the terms of the license owners, but they are not available externally, and following the instructions on this page will not grant you access to them. This includes for example the Intel and Portland Group compilers. While the modules for the Intel and PGI compilers are available, you will only have access to the redistributable parts of these packages, usually the shared objects. These are sufficient to run software packages compiled with these compilers, but not to compile new software.

== CUDA location ==
For CUDA-enabled software packages, our software environment relies on having driver libraries installed in the path /usr/lib64/nvidia. However on some platforms, recent NVidia drivers will install libraries in /usr/lib64 instead. Because it is not possible to add /usr/lib64 to the LD_LIBRARY_PATH without also pulling in all system libraries (which may have incompatibilities with our software environment), we recommend that you create symbolic links in /usr/lib64/nvidia pointing to the installed NVidia libraries. The script below will install the drivers and create the symbolic links that are needed (adjust the driver version that you want)

for file in $(rpm -ql ${nv_pkg[@]}); do
  [ "${file%/*}" = '/usr/lib64' ] && [ ! -d "${file}" ] && \
  ln -snf "$file" "${file%/*}/nvidia/${file##*/}"
done
}}

== LD_LIBRARY_PATH ==
Our software environment is designed to use RUNPATH. Defining LD_LIBRARY_PATH is not recommended and can lead to the environment not working.

== Missing libraries ==
Because we do not define LD_LIBRARY_PATH, and because our libraries are not installed in default Linux locations, binary packages, such as Anaconda, will often not find libraries that they would usually expect. Please see our documentation on Installing binary packages.

== dbus ==
For some applications, dbus needs to be installed. This needs to be installed locally, on the host operating system.