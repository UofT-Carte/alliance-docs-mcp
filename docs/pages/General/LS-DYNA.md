---
title: "LS-DYNA/en"
url: "https://docs.alliancecan.ca/wiki/LS-DYNA/en"
category: "General"
last_modified: "2026-07-23T13:51:25Z"
page_id: 14902
display_title: "LS-DYNA"
---

= Introduction =
LS-DYNA is available on all our clusters.  It is used for many applications to solve problems in multiphysics, solid mechanics, heat transfer and fluid dynamics.  Analyses are performed as separate phenomena or coupled physics simulations such as thermal stress or fluid structure interaction.  LSTC was recently purchased by Ansys, so the LS-DYNA software may eventually be exclusively provided as part of the Ansys module. For now, we recommend using the LS-DYNA software traditionally provided by LSTC as documented in this wiki page.

= Licensing =
The Alliance is a hosting provider for LS-DYNA which means LS-DYNA software is installed as modules on the clusters.  The Alliance does NOT however provide a free LS-DYNA license or provide LS-DYNA license hosting services.  Instead, many institutions, faculties, and departments already have licenses that can be used on our clusters.  If a local license is not available then SHARCNET provides a limited number of free licenses on a first come first serve basis to any researcher as described below.

=== Initial setup and testing ===

If a license server has never been used on a cluster, firewall changes will first need to be done on both the cluster side and server side.  This will typically require involvement from both our technical team and the technical people managing your license software.  To arrange this, send an email containing the service port and IP address of your floating license server to technical support. To check if your license file is working with a legacy LSTC server or ANSYS server you may run the following commands:

 touch ~/.licenses/ls-dyna.lic
 module load ls-dyna
 export LSTC_LICENSE=network|ansys
 export LSTC_LICENSE_SERVER=@, or
 export ANSYSLMD_LICENSE_FILE=@
 ls-dyna_s, or ls-dyna_d

You don't need to specify any input file or arguments to run this test.  The output header should contain a (non-empty) value for Licensed to:.  Press ^C to quit the program and return to the command line.

== Configuring your license ==

In 2019 Ansys, purchased the Livermore Software Technology Corporation (LSTC), developer of LS-DYNA.  LS-DYNA licenses issued by Ansys since that time use Ansys license servers.  Legacy LSTC licenses that run on LSTC license servers are now available from ANSYS. This section explains how to configure your job script for each of these cases.

=== LSTC license ===

If you have a license issued to run on a LSTC license server, there are two options to specify it:

Option 1) Specify your license server by creating a small file named ls-dyna.lic with the following contents:

where  is an integer number and  is the hostname of your LSTC license server.  Put this file in directory $HOME/.licenses/ on each cluster where you plan to submit jobs. The values in the file are picked up by LS-DYNA when it runs. This occurs because our module system sets the LSTC_FILE variable to LSTC_FILE=/home/$USER.licenses/ls-dyna.lic whenever you load a ls-dyna or ls-dyna-mpi module.  This approach is recommended for users with a license hosted on a LSTC license server since (compared to the next option) the identical settings will automatically be used by all jobs you submit on the cluster (without the need to specify them in each individual slurm script or setting them in your environment).

Option 2) Specify your license server by setting the following two environment variables in your slurm scripts:
 export LSTC_LICENSE=network
 export LSTC_LICENSE_SERVER=@
where  is an integer number and  is the hostname or IP address of your LSTC license server.   These variables will take priority over any values specified in your ~/.licenses/ls-dyna.lic file which must exist (even if it's empty) for any ls-dyna or ls-dyna-mpi module to successfully load.  To ensure it exists, run touch ~/.licenses/ls-dyna.lic once on the command line on each cluster where you will submit jobs.  For further details, see the official documentation.

=== ANSYS license ===

If your LS-DYNA license is hosted on an Ansys license server, set the following two environment variables in your slurm scripts:
 export LSTC_LICENSE=ansys
 export ANSYSLMD_LICENSE_FILE=@
where  is an integer number and  is the hostname or IP address of your Ansys license server.  These variables cannot be defined in your ~/.licenses/ls-dyna.lic file.  The file however must exist (even if it's empty) for any ls-dyna module to load.  To ensure this, run touch ~/.licenses/ls-dyna.lic once from the command line (or each time in your slurm scripts).  Note that only module versions >= 12.2.1 will work with Ansys license servers.

SHARCNET

The SHARCNET Ansys license supports running single node SMP or MPP LS-DYNA jobs with many cores using the included dysmp license feature. The SHARCNET Ansys license however does NOT support running multi-node distributed memory MPP LS-DYNA jobs since it lacks the required mppdyna feature.  Any researcher from the Alliance can freely use the SHARCNET license to run upto 5 simultaneous lsdyna jobs with 288 cores without any internal software limits such as those present in the student or teaching licenses.  These limits maybe changed depending on the license load to optimize reliable availability and will be updated here at such time.  For example a researcher can currently submit and run a 192 core single full node job and a 96 core half node job using an unlimited mesh size.  The SHARCNET license may only be used for the purpose of Academic research and associated publications.  To utilize the SHARCNET license on the cluster to run LS-DYNA jobs include the following lines to your slurm script:
 export LSTC_LICENSE=ansys
 export ANSYSLMD_LICENSE_FILE=1055@license1.computecanada.ca

= Cluster job submission =

LS-DYNA provides binaries for running jobs on a single compute node (SMP - Shared Memory Parallel using OpenMP) or across multiple compute nodes (MPP - Message Passing Parallel using MPI).  This section provides slurm scripts for each job type.

== Single node jobs  ==

Modules for running jobs on a single compute node can be listed with: module spider ls-dyna.  Jobs may be submitted to the queue with: sbatch script-smp.sh. The following slurm script shows how to run LS-DYNA with 8 cores on a single compute node. Regarding the AUTO option of the LSTC_MEMORY environment variable, this setting allows memory to be dynamically extended beyond the specified memory=1500M word setting where it is suitable for explicit analysis such as metal forming simulations but not crash analysis.  Given there are 4 Bytes/word for the single precision solver and 8 Bytes/word for the double precision solver,  the 1500M setting in the slurm script example below equates to either 1) a maximum amount of (1500Mw*8Bytes/w) = 12GB memory before LS-DYNA self-terminates when solving an implicit problem or 2) a starting amount of 12GB memory prior to extending it (up 25% if necessary) when solving an explicit problem assuming LSTC_MEMORY=AUTO is uncommented.  Note that 12GB represents 75% of the total mem=16GB reserved for the job and is considered ideal for implicit jobs on a single node.   To summarize, for both implicit and explicit analysis, once an estimate for the total solver memory is determined in GB, the total memory  setting for slurm can be determined by multiplying by 25% while the memory parameter value in mega words can be calculated as (0.75*memGB/8Bytes/w)*1000M and (0.75*memGB/4Bytes/w)*1000M for double and single precision solutions respectively.

where
*ls-dyna_s = single precision smp solver
*ls-dyna_d = double precision smp solver

== Multiple node jobs ==

There are several modules installed for running jobs on multiple nodes using the MPP (Message Passing Parallel) version of LS-DYNA.  The method is based on mpi and can scale to very many cores (8 or more).  The modules may be listed by running module spider ls-dyna-mpi.  Sample slurm scripts below demonstrate how to use these modules for submitting jobs to a specified number of whole nodes *OR* a specified total number of cores using sbatch script-mpp-bynode.sh or sbatch script-mpp-bycore.sh respectively.  The MPP version requires a sufficiently  large enough amount of memory (memory1) for the first core (processor 0) on the master node to decompose and simulate the model.  This amount may be satisfied by specifying a value of mem-per-cpu to slurm slightly larger than the memory (memory2) required per core for simulation and then placing enough cores on the master node such that their differential sum (mem-per-cpu less memory2) is greater than or equal to memory1.  Similar to the single node model, for best results, keep the sum of all expected memory per node within 75% of the reserved ram on a node.  Thus in the first script below, assuming a 128GB full node memory compute node, memory1 maybe 6000M (48GB) maximum and memory2 200M (48GB/31cores).

=== Specify node count ===

Jobs can be submitted to a specified number of whole compute nodes with the following script.

where
*ls-dyna_s = single precision mpp solver
*ls-dyna_d = double precision mpp solver

=== Specify core count ===

Jobs can be submitted to an arbitrary number of compute nodes by specifying the number of cores.  This approach allows the scheduler to determine the optimal number of compute nodes to minimize job wait time in the queue.  Memory limits are applied per core, therefore a sufficiently large value of mem-per-cpu must be specified so the master processor can successfully decompose and handle its computations as explained in more detail in the opening paragraph of this section.

where
*ls-dyna_s = single precision mpp solver
*ls-dyna_d = double precision mpp solver

== Performance testing ==

Depending on the simulation LS-DYNA may not be able to efficiently use very many cores in parallel.  Scaling test jobs should therefore always be run before submitting long jobs.  Doing this will help determine the maximum number of cores that can be used before performance degradation begins to occur.   To extract test job statistics such as Job Wall-clock time, CPU Efficiency and Memory Efficiency either the seff jobnumber command or a cluster job portal such as this can be used.  In the past scaling test jobs for the standard airbag problem have shown significantly different performance characteristics in the past depending which cluster they were being run on.  These tests however were rather small using only 6 cores on a single node with the ls-dyna/12.2.1 module and 6 cores evenly distributed across two nodes with the ls-dyna-mpi/12.2.1 module.  Scaling tests should instead be run using the actual research simulation and cluster where the full production runs will be done to get reliable results.

= Graphical use =

LSTC provides LS-PrePost for pre- and post-processing of LS-DYNA models.  This program is made available by a separate module and does not require a license.  To run abaqus graphically in a remote gui desktop do one of the following where the OnDemand desktop approach is recommended :

== OnDemand ==
1. Connect to an OnDemand system using one of the following URLs in your laptop browser :
 NIBI: https://ondemand.sharcnet.ca
 FIR: https://jupyterhub.fir.alliancecan.ca
 RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
 TRILLIUM: https://ondemand.scinet.utoronto.ca
2. Open a new terminal window in your desktop and run :
 module load StdEnv/2020
 module load ls-prepost/4.9
 lsprepost OR lspp49

== VncViewer ==
1. Connect with a VncViewer client to a login or compute node by following TigerVNC
2. Open a new terminal window in your desktop and run:
 module load StdEnv/2020
 module load ls-prepost/4.9
 lsprepost OR lspp49