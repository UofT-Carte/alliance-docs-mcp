---
title: "Abaqus/en"
url: "https://docs.alliancecan.ca/wiki/Abaqus/en"
category: "General"
last_modified: "2026-10-08T16:59:57Z"
page_id: 10030
display_title: "Abaqus"
---

__FORCETOC__
TRANSLATOR'S NOTE FROM JUNE 2026: This page is currently being reviewed.
Abaqus FEA is a software suite for finite element analysis and computer-aided engineering.

= Licensing =

Abaqus software modules are available on the Alliance clusters, however you must provide your own license. There are two types of license servers each with different setup procedures described below.

== FLEXnet servers ==

To configure your account on a cluster to use a FLEXnet-based (aka FlexLM) Abaqus license server, a single file named ~/.licenses/abaqus.lic must be first setup created containing the license manager daemon port number LMGRD-PORT-NUMBER and the fully qualified hostname FLEXnet-SERVER-HOSTNAME. These two pieces of information are then assigned to the ABAQUSLM_LICENSE_FILE environment variable whenever an Abaqus module is loaded.  Another file abaqus_v6.env may also need to exist in the home or job submission directory if its not assumed default:

 [l2 (login node):~ ] cat abaqus_v6.env
 license_server_type = FLEXNET

 [l2 (login node):~/.licenses] cat abaqus.lic
 prepend_path("ABAQUSLM_LICENSE_FILE","LMGRD-PORT-NUMBER@FLEXnet-SERVER-HOSTNAME")

To check if your license server connection is working run the following command:

 [l2 (login node):~]$ module load abaqus
 [l2 (login node):~]$ abaqus licensing ru | grep ABAQUSLM:
   ABAQUSLM: UP v11.19.6.   <-- indicates success

To check how many cae licenses in a pool are available for immediate use by anyone (the difference between "issued" and "in use") run the following command.  Note that reserved licenses will always appear to be "in use" regardless if they actually are or not by the group they are reserved for.  In the case of the SHARCNET license there are 4 cae licenses but only 1 is reserved therefore 3 are in the pool available to anyone for use.  The following example shows that at the time the following command was run non of the 3 cae licenses in the pool were available for use by any group to run abaqus in gui mode on the nibi cluster On-Demand graphical system.

 [l2 (login node):~]$ abaqus licensing ru | grep cae
 Users of cae:  (Total of 4 licenses issued;  Total of 1 license in use)
 "cae" v62.7, vendor: ABAQUSLM, expiry: 17-jan-2027

For a summary of ALL licenses provided by a license

 [l2 (login node):~]$ module load abaqus
 [l2 (login node):~]$ abaqus licensing r
 Feature                         Version     #licenses    Vendor        Expires
 _______                         _________   _________    ______        ________
 abaqus_extended                 62.7         4           ABAQUSLM      17-jan-2027
 abaqus                          62.7         78          ABAQUSLM      17-jan-2027
 ams                             62.7         1           ABAQUSLM      17-jan-2027
 etc etc etc

== DSLS servers ==

To use a DSLS based license server (Dassault Systèmes License Server), you must first configure two single line text files named ~/.licenses/abaqus.lic and abaqus_v6.env as shown below. You may either put a copy of abaqus_v6.env file into each job submit directory **OR** a single copy into your home directory.  For example, placing both following abaqus_v6.env file in your home directory, you would just need to replace LICENSING-CLIENT-PORT-NUMBER:DSLS-SERVER-HOSTNAME in your ~/.licenses/abaqus.lic file then DSLS_LICENSE_FILE will be configured accordingly whenever an Abaqus module is loaded:

 [l2 (login node):~ ] cat abaqus_v6.env
 license_server_type=DSLS

 [l2 (login node):~/.licenses] cat abaqus.lic
 prepend_path("DSLS_LICENSE_FILE","LICENSING-CLIENT-PORT-NUMBER@DSLS-SERVER-HOSTNAME")

With both files setup, you may now check if the license server is reachable and responding by running:

  [l2 (login node):~ ] module load abaqus
  [l2 (login node):~ ] abaqus licensing dslsstat
  SUCCESS: the output message will contain "license servers declared"
  FAILURE: the output message will contain "No license server available"

== New servers ==

If your license server was never set up for use on an Alliance cluster, some additional configuration changes by the Alliance system administrator and your local system administrator will need to be done. Such changes are necessary to ensure the required TCP ports (https protocol) of your Abaqus server are reachable from all cluster compute nodes through the client/server firewalls. For help, please write to technical support and be sure to include the following:
* FLEXnet SERVER: flex lmgrd port number (default 27000), static vendor port number (default 28000)
  where both ports need to be opened on the Alliance cluster and license server firewalls
* DSLS SERVER: administrative port number (default 4084), licensing client port number (default 4085)
  where only the licensing client port must be opened on the Alliance cluster and license server firewalls
* Fully qualified domain name or IPV4 address of your new Abaqus server
You will be sent a list of cluster IP addresses (known as NAT nodes) so your administrator can open the local server firewall to allow connections from these nodes on the required port(s). Please note that a special license agreement must generally be negotiated and signed by both SIMULIA and your institution before a campus license may be used remotely on an Alliance cluster located on the campus of another institution.

== License queuing ==
The default setup for the license server is to queue jobs started on the cluster by Slurm if not enough tokens are available. There are two options to alter this behaviour so jobs don't sit idle on a cluster compute node waiting for a license indefinitely wasting valuable resources. The first option is to terminate a job immediately if not enough licenses are available, therefore never entering a queue. To specify this setting, create a text file named abaqus_v6.env in either your /home OR working (submit) directory containing the line: lmlicensequeuing=OFF. The second option is to specify a finite wait time where the job can enter into a queued state on the license server such as 1 minute by adding the line: lmhanglimit=1. If within 1 minute sufficient licenses do not come available then the job will be dequeud by the license server and in turn be terminated by Slurm.  For each option, messages will be printed at the bottom of the Slurm output file as shown in the Example below.

= Version notes =

== 2026 ==

A new module abaqus/2026 containing the initial Abaqus 2026 Golden/GA release has been installed into the default StdEnv/2023 environment.  Another module named abaqus/2026.2614 containing the latest SIMULIA Established Products 2026 Fix Packs currently at level FD02 (FP.2614) will be made available as soon as possible. To verify your setup run the following :

 module load abaqus/2026
 module load intel/2024
 abaqus verify -all

All tests should Succeed except for CAE (unless you log into an ondemand/juypter graphical desktop
) and TOSCA (unless you set export FED_DSFLEX_LICENSE_CONFIG=port@hostname) before running the verification.

== 2021 ==

Its recommended to discontinue use of abaqus/2021 installed under the previous StdEnv/2020 since this legacy version generates *** buffer overflow detected *** error on all recent clusters.  An unshare workaround previously included in the single node slurm scripts wof this wiki has now been removed.

= Cluster job submission =

Below are prototype Slurm scripts for submitting thread and mpi-based parallel simulations to single or multiple compute nodes. Most users will find it sufficient to use one of the project directory scripts provided in the Single node computing sections. The optional memory= argument found in the last line of the scripts is intended for larger memory or problematic jobs where 3072MB offset value may require tuning. A listing of all Abaqus command line arguments can be obtained by loading an Abaqus module and running: abaqus -help | less.

Single node jobs that run less than one day should find the project directory script located in the first tab sufficient. However, single node jobs that run for more than a day should use one of the restart scripts. Jobs that create large restart files will benefit by writing to the local disk through the use of the SLURM_TMPDIR environment variable utilized in the temporary directory scripts provided in the two rightmost tabs of the single node standard and explicit analysis sections. The restart scripts shown here will continue jobs that have been terminated early for some reason. Such job failures can occur if a job reaches its maximum requested runtime before completing and is killed by the queue or if the compute node the job was running on crashed due to an unexpected hardware failure. Other restart types are possible by further tailoring of the input file (not shown here) to continue a job with additional steps or change the analysis (see the documentation for version specific details).

Jobs that require large memory or larger compute resources (beyond that which a single compute node can provide) should use the mpi scripts in the multiple node sections below to distribute computing over arbitrary node ranges determined automatically by the scheduler.  Short scaling test jobs should be run to determine wall-clock times (and memory requirements) as a function of the number of cores (2, 4, 8, etc.) to determine the optimal number before running any long jobs.

== Standard analysis ==
Abaqus solvers support thread-based and mpi-based parallelization. Scripts for each type are provided below for running Standard Analysis type jobs on Single or Multiple nodes respectively. Lines that start with ##SBATCH are commented, to uncomment change to #SBATCH.  Most users will find it sufficient to use the first scriptsp1.txt script that requires simply changing def-group to your account and mystd-sim.inp to the name of your input file before submitting with the "sbatch scriptsp1.txt" command.

=== Single node computing ===

To write restart data every N=12 time increments specify in the input file:
 *RESTART, WRITE, OVERLAY, FREQUENCY=12
To write restart data for a total of 12 time increments specify instead:
 *RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO
To check for completed restart information, do
 egrep -i "step|start" testsp*.com testsp*.msg testsp*.sta
Some simulations may benefit by adding the following to the Abaqus command at the bottom of the script:
 order_parallel=OFF

The restart input file should contain:
 *HEADING
 *RESTART, READ

To write restart data every N=12 time increments specify in the input file:
 *RESTART, WRITE, OVERLAY, FREQUENCY=12
To write restart data for a total of 12 time increments specify instead:
 *RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO
To check the completed restart information do:
 egrep -i "step|start" testst*.com testst*.msg testst*.sta

The restart input file should contain:
 *HEADING
 *RESTART, READ

=== Multiple node computing ===

Users with large memory or compute needs (and correspondingly access to a large licenses) can use the following script to perform mpi-based computing over an arbitrary range of nodes ideally left to the scheduler to automatically determine. A companion template script to perform restart of multinode jobs is not provided due to additional limitations when they can be used. Only abaqus/2026 or newer may be used with this script.

 xargs)"
for i in `echo "$nodes"  xargs -n1  uniq`; do hostlist=${hostlist}$(echo "['${i}',$(echo "$nodes"  xargs -n1  grep $i  wc -l)],"); done
hostlist="$(echo "$hostlist"  sed 's/,$//g')"
mphostlist="mp_host_list=[$(echo "$hostlist")]"
export $mphostlist
echo "$mphostlist" > abaqus_v6.env

abaqus job=testsp1-mpi input=mystd-sim.inp \
scratch=$SLURM_TMPDIR cpus=$SLURM_NTASKS interactive mp_mode=mpi \
#mp_host_split=1  # number of dmp processes per node >= 1 (uncomment to specify)
}}

== Explicit analysis ==

Abaqus solvers support thread-based and mpi-based parallelization. Scripts for each type are provided below for running explicit analysis type jobs on single or multiple nodes respectively. Template scripts to perform multinode job restarts are not currently provided, pending further testing.

=== Single node computing ===

To write restart data for a total of 12 time increments specify in the input file:
 *RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO
Check for completed restart information in relevant output files:
 egrep -i "step|restart" testep*.com testep*.msg testep*.sta

No input file modifications are required to restart the analysis.

To write restart data for a total of 12 time increments specify in the input file:
 *RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO
Check for completed restart information in relevant output files:
 egrep -i "step|restart" testet*.com testet*.msg testet*.sta

No input file modifications are required to restart the analysis.

=== Multiple node computing ===

Users with large memory or compute needs (and correspondingly access to a large licenses) can use the following script to perform mpi-based computing over an arbitrary range of nodes ideally left to the scheduler to automatically determine. A companion template script to perform restart of multinode jobs is not provided due to additional limitations on how they can be used. Only abaqus/2026 or newer may be used with this script.

 xargs)"
for i in `echo "$nodes"  xargs -n1  uniq`; do hostlist=${hostlist}$(echo "['${i}',$(echo "$nodes"  xargs -n1  grep $i  wc -l)],"); done
hostlist="$(echo "$hostlist"  sed 's/,$//g')"
mphostlist="mp_host_list=[$(echo "$hostlist")]"
export $mphostlist
echo "$mphostlist" > abaqus_v6.env

abaqus job=testep1-mpi input=myexp-sim.inp \
scratch=$SLURM_TMPDIR cpus=$SLURM_NTASKS interactive mp_mode=mpi \
#mp_host_split=1  # number of dmp processes per node >= 1 (uncomment to specify)
}}

== Memory estimates ==

=== Single process ===

An estimate for the total Slurm node memory (--mem=) required for a simulation to run fully in ram (without being virtualized to scratch disk) can be obtained by examining the Abaqus output test.dat file.  For example, a simulation that requires a fairly large amount of memory might show:

                   M E M O R Y   E S T I M A T E

 PROCESS      FLOATING PT       MINIMUM MEMORY        MEMORY TO
              OPERATIONS           REQUIRED          MINIMIZE I/O
             PER ITERATION           (MB)               (MB)

     1          1.89E+14             3612              96345

Alternatively a total memory estimate for a single node threaded process can be obtained by running the simulation interactively on a compute node and then monitoring the memory use with the top (or ps) command as follows:
1) First obtain an allocation on a compute node and start your simulation running:

2) Next ssh into the compute node (c50 according to the sq command) and then run top, i.e.

3) watch the VIRT and RES columns until steady peak memory values are observed

To completely satisfy the recommended "MEMORY TO OPERATIONS REQUIRED MINIMIZE I/O" (MRMIO) value, at least the same amount of non-swapped physical memory (RES) must be available to Abaqus. Since the RES will in general be less than the virtual memory (VIRT) by some relatively constant amount for a given simulation, it is necessary to slightly over-allocate the requested Slurm node memory -mem=. In the above sample Slurm script, this over-allocation has been hardcoded to a conservative value of 3072MB based on initial testing of the standard Abaqus solver. To avoid long queue wait times associated with large values of MRMIO, it may be worth investigating the simulation performance impact associated with reducing the RES memory that is made available to Abaqus significantly below the MRMIO.  This can be done by lowering the -mem= value which in turn will set an artificially low value of memory= in the Abaqus command (found in the last line of the script).  In doing this, the RES cannot dip below the MINIMUM MEMORY REQUIRED (MMR) otherwise Abaqus will exit due to Out of Memory (OOM).  As an example, if your MRMIO is 96GB try running a series of short test jobs with #SBATCH --mem=8G, 16G, 32G, 64G until an acceptable minimal performance impact is found, noting that smaller values will result in increasingly larger scratch space used by temporary files.

=== Multi process ===

To determine the required Slurm memory for multi-node Slurm scripts, memory estimates (per compute process) required to minimize I/O are given in the output dat file of completed jobs. If mp_host_split is not specified (or is set to 1) then the total number of compute processes will equal the number of nodes. The mem-per-cpu value can then be roughly determined by multiplying the largest memory estimate by the number of nodes and then dividing by the number or ntasks. However, if a value for mp_host_split is specified (greater than 1) than the mem-per-cpu value can be roughly determined from the largest memory estimate times the number of nodes times the value of mp_host_split divided by the number of tasks. Note that mp_host_split must be less than or equal to the number of cores per node assigned by Slurm at runtime otherwise Abaqus will terminate. This scenario can be controlled by uncommenting to specify a value for tasks-per-node. The following definitive statement is given in every output dat file and mentioned here for reference:

  THE UPPER LIMIT OF MEMORY THAT CAN BE ALLOCATED BY ABAQUS WILL IN GENERAL DEPEND ON THE VALUE OF
 THE "MEMORY" PARAMETER AND THE AMOUNT OF PHYSICAL MEMORY AVAILABLE ON THE MACHINE. PLEASE SEE
 THE "ABAQUS ANALYSIS USER'S MANUAL" FOR MORE DETAILS. THE ACTUAL USAGE OF MEMORY AND OF DISK
 SPACE FOR SCRATCH DATA WILL DEPEND ON THIS UPPER LIMIT AS WELL AS THE MEMORY REQUIRED TO MINIMIZE
 I/O. IF THE MEMORY UPPER LIMIT IS GREATER THAN THE MEMORY REQUIRED TO MINIMIZE I/O, THEN THE ACTUAL
 MEMORY USAGE WILL BE CLOSE TO THE ESTIMATED "MEMORY TO MINIMIZE I/O" VALUE, AND THE SCRATCH DISK
 USAGE WILL BE CLOSE-TO-ZERO; OTHERWISE, THE ACTUAL MEMORY USED WILL BE CLOSE TO THE PREVIOUSLY
 MENTIONED MEMORY LIMIT, AND THE SCRATCH DISK USAGE WILL BE ROUGHLY PROPORTIONAL TO THE DIFFERENCE
 BETWEEN THE ESTIMATED "MEMORY TO MINIMIZE I/O" AND THE MEMORY UPPER LIMIT. HOWEVER ACCURATE
 ESTIMATE OF THE SCRATCH DISK SPACE IS NOT POSSIBLE.

= Graphical use =

It is recommended to use an OpenOnDemand or JupyterLab to run graphical applications at the Alliance.

== OnDemand ==

1. Start an OnDemand desktop session by clicking one of the following OnDemand links:
 Nibi: https://ondemand.sharcnet.ca
 TRILLIUM: https://ondemand.scinet.utoronto.ca

2. Open a new terminal window within your desktop and load
 module load abaqus/2026

3. Start the application in graphical mode using the cae option. If you are on either: 1) a node without a GPU or 2) a node with a GPU but without VirtualGL support, then append to use the mesa option:
 abaqus cae -mesa

4. If you require better graphical performance and are on a node with a GPU and VirtualGL support then start Abaqus without the -mesa option. When using the Nibi OnDemand desktop, a full h100 (80GB) GPU from the GPU pulldown must be selected.
 abaqus cae

5. To start Abaqus in gui mode, there must be at least one unused CA license according to

 $ abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | grep "Users of cae"
 Users of cae:  (Total of 4 licenses issued;  Total of 3 licenses in use)

== JupyterLab ==

1. Start a JupyterHub desktop session by clicking one of the following JupyterHub links
 FIR: https://jupyterhub.fir.alliancecan.ca
 NARVAL:  https://portail.narval.calculquebec.ca/
 RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
2. Highlight an abaqus module such as abaqus/2026 in the left-hand side Available Module section
3. Click on Load for the highlighted module and a Abaqus (VNC) icon will appear in desktop.
4. Click on the icon and Abaqus should automatically be started in a remote Juypter desktop

== VncViewer ==

This approach is considered obsolete please use the above OnDemand/JuypterHub desktop instead.

1. Connect with a VncViewer client to a login or compute node without a GPU by following TigerVNC
2. Open a new terminal window and enter the following
 module load abaqus/2026
3. Start the application with
 abaqus cae -mesa

= Site-specific use =
== SHARCNET license ==

The SHARCNET license has been renewed until 17-jan-2027 and is operational. It provides a small shared free pool consisting of 3 cae and 54 execute tokens for all researchers. Maximum usage limits are currently set at: 1cae/user, 10 tokens/user and 15 tokens/group. These free tokens are available on a first come first serve basis and mainly intended for testing and light usage before deciding whether or not to purchase dedicated tokens. Costs for dedicated tokens (in 2021) were approximately CAD$110 per compute token and CAD$400 per GUI token: submit a ticket to request an official quote if interested. The free SHARCNET license can be used by any registered Alliance researcher, but only on SHARCNET hardware, and only after agreeing to the below Academic License User Agreement. Groups that purchase dedicated tokens to run on the SHARCNET license server may likewise ONLY use them on SHARCNET hardware (as dictated by the negotiated license agreement with Simulia) including the SHARCNET OOD system (to run Abaqus in graphical mode) or Nibi/Dusky clusters (for submitting compute batch jobs to the queue). Before you can use the license, you must contact technical support and request access. In your email 1) mention that it is for use on SHARCNET systems and 2) include a copy/paste of the following License Agreement statement with your full name and username entered in the indicated locations. Please note that every user must do this it cannot be done one time only for a group; this includes PIs who have purchased their own dedicated tokens.

=== License agreement ===
----------------------------------------------------------------------------------
Subject: Abaqus SHARCNET Academic License User Agreement

This email is to confirm that i "_____________" with username "___________" will
only use “SIMULIA Academic Software” with tokens from the SHARCNET license server
for the following purposes:

1) on SHARCNET hardware where the software is already installed;
2) in affiliation with a Canadian degree-granting academic institution;
3) for education, institutional or instruction purposes and not for any commercial
   or contract-related purposes where results are not publishable;
4) for experimental, theoretical and/or digital research work, undertaken primarily
   to acquire new knowledge of the underlying foundations of phenomena and observable
   facts, up to the point of proof-of-concept in a laboratory.
-----------------------------------------------------------------------------------

=== Configure license file ===
Configure your license file as follows, noting that it is only usable on SHARCNET systems such as the Nibi and Dusky clusters or the SHARCNET OOD desktop system. Note that the old license3.sharcnet.ca server has been permanently shut down; you must update your abaqus.lic file as follows to use the free SHARCNET license:

[l2 (nibi login node):~] cat ~/.licenses/abaqus.lic
prepend_path("ABAQUSLM_LICENSE_FILE","27050@license1.computecanada.ca")

If your Abaqus job fails with the error message [*** ABAQUS/eliT_CheckLicense rank 0 terminated by signal 11 (Segmentation fault)] then verify your abaqus.lic file contains ABAQUSLM_LICENSE_FILE when using abaqus/202X modules.  If your Abaqus jobs fails with error message [License server machine is down or not responding, etc.] and you are using abaqus/6.14.1 then replace ABAQUSLM_LICENSE_FILE with LM_LICENSE_FILE.

=== Query license server ===
Log into the Nibi cluster, load Abaqus, and run one of the following:

ssh nibi.alliancecan.ca
module load StdEnv/2020
module load abaqus

I) Check the SHARCNET license server for started and queued jobs:

abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | egrep "Users|start|queued"

II) Check the SHARCNET license server for started and queued jobs also showing reservations by purchasing groups:

abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | egrep "Users|start|queued|RESERVATION"

III) Check the SHARCNET license server for only cae, standard and explicit product availability:

abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | grep "Users of" | egrep "cae|standard|explicit"

When the output of query I) above indicates that a job for a particular username is queued this means the job has entered the "R"unning state from the perspective of squeue -j jobid or sacct -j jobid and is therefore idle on a compute node waiting for a license. This will have the same impact on your account priority as if the job were performing computations and consuming CPU time. Eventually when sufficient licenses come available the queued job will start.

==== Example ====

The following shows the situation where a user submitted two 6-core jobs (each requiring 12 tokens) in quick succession. The scheduler then started each job on a different node in the order they were submitted. Since the user had 10 Abaqus compute tokens, the first job (27527287) was able to acquire exactly enough (10) tokens for the solver to begin running. The second job (27527297) not having access to any more tokens entered an idle "queued" state (as can be seen from the lmstat output) until the first job completed, wasting the available resources and depreciating the user's fair share level in the process ...

 [l2 (nibi login node):~] sq
            JOBID     USER              ACCOUNT           NAME  ST  TIME_LEFT NODES CPUS TRES_PER_N MIN_MEM NODELIST (REASON)
         27530366  roberpj         cc-debug_cpu  scriptsp2.txt   R    9:56:13     1    6        N/A      8G     c107  (None)
         27530407  roberpj         cc-debug_cpu  scriptsp2.txt   R    9:59:37     1    6        N/A      8G     c292  (None)

 [l2 (nibi login node):~] abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | egrep "Users|start|queued"
 Users of abaqus:  (Total of 78 licenses issued;  Total of 53 licenses in use)
    roberpj c107 /dev/tty (v62.6) (license3.sharcnet.ca/27050 1042), start Mon 11/25 17:15, 10 licenses
    roberpj c292 /dev/tty (v62.6) (license3.sharcnet.ca/27050 125) queued for 10 licenses

To avoid license shortage problems when submitting multiple jobs when working with expensive Abaqus tokens either use a job dependency, job array or at the very least set up a Slurm email notification to know when your job completes before manually submitting another one. There are two easier options to dealing with this situation:

Option 1)

Disable non-interactive (analysis) jobs from starting on a cluster compute node after being submitted to the queue and then becoming idle (when not enough tokens are unavailable the default bahaviour) create a text file in your submit directory (before submitting the job) with the following one line contents and the job will instead terminate immediately.

 [l2 (nibi login node):~/submitdirectory] cat abaqus_v6.env
 lmlicensequeuing=OFF

When a job immediately terminates (without entering a QUEUED state to wait for a license) the end of the corresponding Slurm output file will contain messages such as

 Abaqus 2026
 Checkout exceeds MAX specified in options file.
 FlexNet Licensing error:-87,147
 Number of requested licenses: 14
 Number of total licenses:     78
 Number of licenses in use:    14
 Number of available licenses: 64
 This may be due to insufficient licenses.
 ValueError: not enough values to unpack (expected 2, got 1)
 During handling of the above exception, another exception occurred:
 Exception: DriverLM: can't parse host/port from umbrella
 Abaqus Error: Error checking out Abaqus license.
 Abaqus/Analysis exited with errors

Option 2)

Specify a setting in minutes so that a started job will enter a QUEUED state to wait for a license before being automatically DEQUEUED and terminating if a license does not become available in time.

 [l2 (nibi login node):~/submitdirectory] cat abaqus_v6.env
  lmhanglimit=1

When a job terminates this way, after being queued and no license comes available in the specified time according to the lmhanlimit value (1minute in this example) the messages at the end of the Slurm output file will instead appear as

 Abaqus 2026
 "standard" license request queued for the License Server on license1.computecanada.ca.
 Total time in queue: 0 seconds.
 "standard" license request queued for the License Server on license1.computecanada.ca.
 Total time in queue: 30 seconds.
 "standard" license request queued for the License Server on license1.computecanada.ca.
 Total time in queue: 60 seconds.
 Time limit of in queue has been exceeded. Exiting.
 This may be due to insufficient licenses.
 ValueError: not enough values to unpack (expected 2, got 1)
 During handling of the above exception, another exception occurred:
 Exception: DriverLM: can't parse host/port from umbrella
 Abaqus Error: Error checking out Abaqus license.
 Abaqus/Analysis exited with errors

=== Specify job resources ===
To ensure optimal usage of both your Abaqus tokens and our resources, it's important to carefully specify the required memory and ncpus in your Slurm script. The values can be determined by submitting a few short test jobs to the queue then checking their utilization. For completed jobs use seff JobNumber to show the total Memory Utilized and Memory Efficiency. If the Memory Efficiency is less than ~90%, decrease the value of the #SBATCH --mem= setting in your Slurm script accordingly. Notice that the seff JobNumber command also shows the total CPU (time) Utilized and CPU Efficiency. If the CPU Efficiency is less than ~90%, perform scaling tests to determine the optimal number of CPUs for optimal performance and then update the value of #SBATCH --cpus-per-task= in your Slurm script. For running jobs, use the srun --overlap --jobid=29821580 --pty top -d 5 -u $USER command to watch the %CPU, %MEM and RES for each Abaqus parent process on the compute node. The %CPU and %MEM columns display the percent usage relative to the total available on the node while the RES column shows the per process resident memory size (in human readable format for values over 1GB). Further information regarding how to monitor jobs is available on our documentation wiki

=== Core-token mapping ===

TOKENS 5  6  7  8  10  12  14  16  19  21  25  28  34  38
CORES  1  2  3  4   6   8  12  16  24  32  48  64  96 128

where TOKENS = floor[5 X CORES^0.422]

Each GPU used requires 1 additional TOKEN

== Western license ==

The Western abaqus site license may only be used by Western researchers on compute hardware located on Western's campus. Currently, only the Dusky cluster satisfies this condition. The Nibi and SHARCNET OOD systems may not be used since they are located on Waterloo's campus. Contact the Western Abaqus license server administrator  to inquire about being added to the Western Abaqus license. You will need to provide your alliance username and possibly make arrangements with your supervisor to purchase tokens. If you are granted access then you may proceed to login to Dusky and configure your abaqus.lic file using a text editor such as nano to contain the following single line:

[laptop:~] ssh dusky.alliancecan.ca

[dus241:~] cat .licenses/abaqus.lic
prepend_path("ABAQUSLM_LICENSE_FILE","27000@authorize.robarts.ca")

Now you may submit your job using a slurm script and the sbatch command as described in the Cluster job submission section above. If there are any problems submit a problem ticket to technical support. Specify that you are using the Abaqus Western license on dusky and provide the failed job number along with a paste of any error messages as applicable.