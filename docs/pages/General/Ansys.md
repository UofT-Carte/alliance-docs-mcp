---
title: "Ansys"
url: "https://docs.alliancecan.ca/wiki/Ansys"
category: "General"
last_modified: "2026-05-15T20:23:56Z"
page_id: 4568
display_title: "Ansys"
---

Ansys is a software suite for engineering simulation and 3-D design. It includes packages such as Ansys Fluent and Ansys CFX.

= Licensing =
We are a hosting provider for Ansys. This means that we have the software installed on our clusters, but we do not provide a generic license accessible to everyone. However, many institutions, faculties, and departments already have licenses that can be used on our clusters.  Once the legal aspects are worked out for licensing, there will be remaining technical aspects. The license server on your end will need to be reachable by our compute nodes. This will require our technical team to get in touch with the technical people managing your license software. In some cases, this has already been done. You should then be able to load the Ansys module, and it should find its license automatically. If this is not the case, please contact our technical support so that they can arrange this for you.

== Configuring your license file ==
Our module for Ansys is designed to look for license information in a few places. One of those places is your /home folder. You can specify your license server by creating a file named $HOME/.licenses/ansys.lic consisting of two lines as shown.  Customize the file by replacing FLEXPORT and LICSERVER with the appropriate values for your server.

 FILE: ansys.lic

setenv("ANSYSLMD_LICENSE_FILE", "FLEXPORT@LICSERVER")

The following table provides established values for the CMC and SHARCNET license servers.  To use a different server, locate the corresponding values as explained in Local license servers.

 TABLE: Preconfigured license servers

License 	System/Cluster                  	LICSERVER                	FLEXPORT	NOTES
CMC     	fir                             	172.26.0.101             	6624    	Discontinue use (shutdown Apr 23, 2026)
CMC     	narval/rorqual                  	10.100.64.10             	6624    	Discontinue use (shutdown Apr 23, 2026)
CMC     	nibi                            	10.25.1.56               	6624    	Discontinue use (shutdown Apr 23, 2026)
CMC     	trillium                        	scinet-cmc               	6624    	Discontinue use (shutdown Apr 23, 2026)
SHARCNET	nibi/fir/narval/rorqual/trillium	license1.computecanada.ca	1055

=== Local license servers  ===

Before a local institutional Ansys license server can be used on the Alliance, firewall changes will need to be done on both the server and cluster side.  For many Ansys servers this work has already been done and they can be used by following the steps in the "Ready To Use" section below.  For Ansys servers that have never used on the Alliance, two additional steps must be done as shown in the "Setup Required" section also below.

==== Ready to use ====

To use a local institutional ANSYS License server whose network/firewall connections have already been setup for use on an Alliance cluster, contact your local Ansys license server administrator and get the following two pieces of information:
 1) the configured Ansys flex port (FLEXPORT) number commonly 1055
 2) the fully qualified hostname (LICSERVER) of the license server
Then simply configure your ~/.licenses/ansys.lic file by plugging the values for FLEXPORT and LICSERVER into the FILE: ansys.lic template above.

==== Setup required ====

To use a local Ansys license server that has never been setup for use with an Alliance cluster, then you will ALSO need to get the following from your local Ansys license server administrator:
  3) the statically configured vendor port (VENDPORT) of the license server
  4) confirmation  will resolve to the same IP address as LICSERVER on the cluster
where the  can be found in the first line of the license file with format "SERVER   ".   Send items 1->3 by email to technical support and mention which Alliance cluster you want to run Ansys jobs on.  An Alliance system administrator will then open the outbound cluster firewall so license checkout requests can reach your license server from the cluster compute nodes.  A range of IP addresses will then be sent back to you.  Give these to your local network administrator.  Request the firewall into your local license server be opened so that Ansys license connection (checkout requests) can reach your servers FLEXPORT and VENDPORT ports across the IP range.

== Checking license ==

To test if your ansys.lic is configured and working properly with your license server, run the following sequence of commands on the same cluster that you will be submitting jobs to:

[login-node:~] cd /tmp
 [login-node:/tmp] salloc --time1:0:0 --mem1000M --accountdef-YOURUSERID
 [compute-node/tmp] module load StdEnv/2023; module load ansys/2025R2.04
 [compute-node:/tmp] $EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil lmstat -c $ANSYSLMD_LICENSE_FILE | grep "ansyslmd: UP" 1> /dev/null && echo Success  echo Fail
Success output indicates license checkouts should work when jobs are submitted to the queue.
Fail output indicates a problem with the licensing setup somewhere and jobs will likely fail.

If there is an Ansys license server checkout problem, then the following message will appear in slurm output files when fluent jobs are started by slurm scripts in the queue *OR* when fluent is start interactively simply by doing the following:

[compute-node:/tmp] fluent -g 2d -n 2
 Connected License Server List:
 Hit return to exit.

= Version compatibility =

Ansys simulations are typically forward compatible but NOT backwards compatible.  This means that simulations created using an older version of Ansys can be expected to load and run fine with any newer version.  For example, a simulation created and saved with ansys/2022R2 should load and run smoothly with ansys/2023R2 but NOT the other way around.  While it may be possible to start a simulation running with an older version random error messages or crashing will likely occur.  Regarding Fluent simulations, if you cannot recall which version of ansys was used to create your cas file try grepping it as follows to look for clues :

$ grep -ia fluent combustor.cas
   (0 "fluent15.0.7  build-id: 596")

$ grep -ia fluent cavity.cas.h5
   ANSYS_FLUENT 24.1 Build 1018

== Platform support ==

Ansys provides detailed platform support information describing software/hardware compatibility for the Current Release and Previous Releases.   The Platform Support by Application / Product pdf is of special interest since it shows which packages are supported under Windows but not under Linux and thus not on the Alliance such as Spaceclaim.

== What's new ==

Information for the latest Ansys release can be found here for example Ansys 2026 R1 at the time of this writing.  Posts for previous releases can be found by visiting the Ansys blog page and then scrolling down to the FILTERS search bar.  Inputting for example What’s New Fluent 2024 gpu should pull up a document containing the latest gpu support information for that release. The Press Release search bar is also a good way to find release specific information.

== Service packs ==

Starting with Ansys 2024 a separate Ansys module will appear on the clusters with a decimal and two digits appearing after the release number whenever a service pack is been installed over the initial release.  For example, the initial 2024 release with no service pack applied may be loaded with  module load ansys/2024R1 while a module with Service Pack 3 applied may be loaded with module load ansys/2024R1.03 instead.  If a service pack is already available by the time a new release is to be installed, then most likely only a module for that service pack number will be installed unless a request to install the initial release is also received.

Most users will likely want to load the latest module version equipped with the latest installed service pack which can be achieved by simply doing module load ansys.  While it's not expected service packs will impact numerical results, the changes they make are extensive and so, if computations have already been done with the initial release or an earlier service pack then some groups may prefer to continue using it. Having separate modules for each service pack makes this possible.  Starting with Ansys 2024R1 a detailed description of what each service pack does can be found by searching this link for Service Pack Details.  Future versions will presumably be similarly searchable by manually modifying the version number contained in the link.

= Cluster batch job submission =
The Ansys software suite comes with multiple implementations of MPI to support parallel computation. Unfortunately, none of them support our Slurm scheduler. For this reason, we need special instructions for each Ansys package on how to start a parallel job. In the sections below, we give examples of submission scripts for some of the packages.  While the slurm scripts should work with on all clusters, Niagara users may need to make some additional changes covered here.

== Fluent ==
Typically, you would use the following procedure to run Fluent on one of our clusters:

# Prepare your Fluent job using Fluent from the Ansys Workbench on your desktop machine up to the point where you would run the calculation.
# Export the "case" file with File > Export > Case… or find the folder where Fluent saves your project's files. The case file will often have a name like FFF-1.cas.gz.
# If you already have data from a previous calculation, which you want to continue, export a "data" file as well (File > Export > Data…) or find it in the same project folder (FFF-1.dat.gz).
# Transfer the case file (and if needed the data file) to a directory on the /project or /scratch filesystem on the cluster.  When exporting, you can save the file(s) under a more instructive name than FFF-1.* or rename them when they are uploaded.
# Now you need to create a "journal" file. Its purpose is to load the case file (and optionally the data file), run the solver and finally write the results.  See examples below and remember to adjust the filenames and desired number of iterations.
# If jobs frequently fail to start due to license shortages and manual resubmission of failed jobs is not convenient, consider modifying your script to requeue your job (up to 4 times) as shown under the by node + requeue tab further below.  Be aware that doing this will also requeue simulations that fail due to non-license related issues (such as divergence), resulting in lost compute time.  Therefore it is strongly recommended to monitor and inspect each Slurm output file to confirm each requeue attempt is license related.  When it is determined that a job is requeued due to a simulation issue, immediately manually kill the job progression with scancel jobid and correct the problem.
# After running the job, you can download the data file and import it back into Fluent with File > Import > Data….

=== Slurm scripts ===

==== General purpose ====

Most Fluent jobs should use the following by node script to minimize solution latency and maximize performance over as few nodes as possible. Very large jobs, however, might wait less in the queue if they use a by core script. However, the startup time of a job using many nodes can be significantly longer, thus offsetting some of the benefits. In addition, be aware that running large jobs over an unspecified number of potentially very many nodes will make them far more vulnerable to crashing if any of the compute nodes fail during the simulation. The scripts will ensure Fluent uses shared memory for communication when run on a single node or distributed memory (utilizing MPI and the appropriate HPC interconnect) when run over multiple nodes.  The two narval tabs may be be useful to provide a more robust alternative if fluent crashes during the initial auto mesh partitioning phase when using the standard intel based scripts with the parallel solver.  The other option would be to manually perform the mesh partitioning in the fluent gui then try to run the job again on the cluster with the intel scripts.  Doing so will allow you to inspect the partition statistics and specify the partitioning method to obtain an optimal result.  The number of mesh partitions should be an integral multiple of the number of cores; for optimal efficiency, ensure at least 10000 cells per core.

 uniq`; do echo "${i}:$(cat /tmp/mf-$SLURM_JOB_ID  grep $i  wc -l)" >> /tmp/machinefile-$SLURM_JOB_ID; done
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pshmem -i $MYJOURNALFILE
else
 export FI_PROVIDER=verbs
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
fi
}}

 uniq`; do echo "${i}:$(cat /tmp/mf-$SLURM_JOB_ID  grep $i  wc -l)" >> /tmp/machinefile-$SLURM_JOB_ID; done
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pshmem -i $MYJOURNALFILE
else
 export FI_PROVIDER=verbs
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
fi
}}

==== License requeue ====

The scripts in this section should only be used with Fluent jobs that are known to complete normally without generating any errors in the output however typically require multiple requeue attempts to checkout licenses.  They are not recommended for Fluent jobs that may 1) run for a long time before crashing 2) run to completion but contain unresolved journal file warnings, since in both cases the simulations will be repeated from the beginning until the maximum number of requeue attempts specified by the array value is reached.  For these types of jobs, the general purpose scripts above should be used instead.

==== Solution restart ====

The following two scripts are provided to automate restarting very large jobs that require more than the typical seven-day maximum runtime window available on most clusters. Jobs are restarted from the most recent saved time step files. A fundamental requirement is the first time step can be completed within the requested job array time limit (specified at the top of your Slurm script) when starting a simulation from an initialized solution field. It is assumed that a standard fixed time step size is being used. To begin, a working set of sample.cas, sample.dat and sample.jou files must be present. Next edit your sample.jou file to contain /solve/dual-time-iterate 1 and /file/auto-save/data-frequency 1. Then create a restart journal file by doing cp sample.jou sample-restart.jou and edit the sample-restart.jou file to contain /file/read-cas-data sample-restart instead of /file/read-cas-data sample and comment out the initialization line with a semicolon for instance ;/solve/initialize/initialize-flow. If your 2nd and subsequent time steps are known to run twice as fast (as the initial time step), edit sample-restart.jou to specify /solve/dual-time-iterate 2. By doing this, the solution will only be restarted after two 2 time steps are completed following the initial time step. An output file for each time step will still be saved in the output subdirectory. The value 2 is arbitrary but should be chosen such that the time for 2 steps fits within the job array time limit. Doing this will minimize the number of solution restarts which are computationally expensive. If your first time step performed by sample.jou starts from a converged (previous) solution, choose 1 instead of 2 since likely all time steps will require a similar amount of wall time to complete. Assuming 2 is chosen, the total time of simulation to be completed will be 1*Dt+2*Nrestart*Dt where Nrestart is the number of solution restarts specified in the script. The total number of time steps (and hence the number of output files generated) will therefore be 1+2*Nrestart. The value for the time resource request should be chosen so the initial time step and subsequent time steps will complete comfortably within the Slurm time window specifiable up to a maximum of "#SBATCH --time=07-00:00" days.

=== Journal files ===

Fluent journal files can include basically any command from Fluent's Text-User-Interface (TUI); commands can be used to change simulation parameters like temperature, pressure and flow speed. With this you can run a series of simulations under different conditions with a single case file, by only changing the parameters in the journal file. Refer to the Fluent User's Guide for more information and a list of all commands that can be used.  The following journal files are set up with /file/cff-files no to use the legacy .cas/.dat file format (the default in module versions 2019R3 or older).  Set this instead to /file/cff-files yes to use the more efficient .cas.h5/.dat.h5 file format (the default in module versions 2020R1 or newer).

=== UDFs ===

The first step is to transfer your User-Defined Function or UDF (namely the sampleudf.c source file and any additional dependency files) to the cluster.  When uploading from a windows machine, be sure the text mode setting of your transfer client is used otherwise fluent won't be able to read the file properly on the cluster since it runs linux.  The UDF should be placed in the directory where your journal, cas and dat files reside.  Next add one of the following commands into your journal file before the commands that read in your simulation cas/dat files.   Regardless of whether you use the Interpreted or Compiled UDF approach,  before uploading your cas file onto the Alliance please check that neither the Interpreted UDFs Dialog Box or the UDF Library Manager Dialog Box are configured to use any UDF; this will ensure that only the journal file commands are in control when jobs are submitted.

==== Interpreted ====

To tell fluent to interpret your UDF at runtime, add the following command line into your journal file before the cas/dat files are read or initialized. The filename sampleudf.c should be replaced with the name of your source file.  The command remains the same regardless if the simulation is being run in serial or parallel.  To ensure the UDF can be found in the same directory as the journal file, open your cas file in the fluent gui, remove any managed definitions and resave it.   Doing this will ensure only the following command/method is in control when fluent runs. To use an interpreted UDF with parallel jobs, it will need to be parallelized as described in the section below.

define/user-defined/interpreted-functions "sampleudf.c" "cpp" 10000 no

==== Compiled ====

To use this approach, your UDF must be compiled on an Alliance cluster at least once.  Doing so will create a libudf subdirectory structure containing the required libudf.so shared library.   The libudf directory cannot simply be copied from a remote system (such as your laptop) to the Alliance since the library dependencies of the shared library will not be satisfied, resulting in fluent crashing on startup.  That said, once you have compiled your UDF on an Alliance cluster, you can transfer the newly created libudf to any other Alliance cluster, providing your account loads the same StdEnv environment module version.  Once copied, the UDF can be used by uncommenting the second (load) libudf line below in your journal file when submitting jobs to the cluster.  Both (compile and load) libudf lines should not be left uncommented in your journal file when submitting jobs on the cluster, otherwise your UDF will automatically (re)compiled for each and every job.  Not only is this highly inefficient, but it will also lead to racetime-like build conflicts if multiple jobs are run from the same directory. Besides configuring your journal file to build your UDF, the fluent gui may also be used.  To do this, navigate to the Compiled UDFs Dialog Box, add the UDF source file and click Build.   When using a compiled UDF with parallel jobs, your source file should be parallelized as discussed in the section below.

define/user-defined/compiled-functions compile libudf yes sampleudf.c "" ""

and/or

define/user-defined/compiled-functions load libudf

==== Parallel ====

Before a UDF can be used with a fluent parallel job (single node SMP and multinode MPI) it will need to be parallelized.  By doing this we control how/which processes (host and/or compute) run specific parts of the UDF code when fluent is run in parallel on the cluster. The instrumenting procedure involves adding compiler directives, predicates and reduction macros into your working serial UDF. Failure to do so will result in fluent running slow at best or immediately crashing at worst.  The end result will be a single UDF that runs efficiently when fluent is used in both serial and parallel mode.  The subject is described in detail under Part I: Chapter 7: Parallel Considerations of the Ansys 2024 Fluent Customization Manual which can be accessed here.

==== DPM ====
UDFs can be used to customize Discrete Phase Models (DPM) as described in Part III: Solution Mode | Chapter 24: Modeling Discrete Phase | 24.2 Steps for Using the Discrete Phase Models| 24.2.6 User-Defined Functions of the 2024R2 Fluent Users Guide and section Part I: Creating and Using User Defined Functions | Chapter 2: DEFINE Macros | 2.5 Discrete Phase Model (DPM) DEFINE Macros of the 2024R2 Fluent Customization Manual. Before a DMP based UDF can be worked into a simulation, the injection of a set of particles must be defined by specifying "Point Properties" with variables such as source position, initial trajectory, mass flow rate, time duration, temperature and so forth depending on the injection type.  This can be done in the gui by clicking the Physics panel, Discrete Phase to open the Discrete Phase Model box and then clicking the Injections button.  Doing so will open an Injections dialog box where one or more injections can be created by clicking the Create button.   The "Set Injection Properties" dialog which appears will contain an "Injection Type" pulldown with first four types available are "single, group, surface, flat-fan-atomizer". If you select any of these then you can then the "Point Properties" tab can be selected to input the corresponding Value fields.  Another way to specify the "Point Properties" would be to read an injection text file.  To do this select "file" from the Injection Type pulldown, specify the Injection Name to be created and then click the File button (located beside the OK button at the bottom of the  "Set Injection Properties" dialog).   Here either an Injection Sample File (with .dpm extension) or a manually created injection text file can be selected.   To Select the File in the Select File dialog box that change the File of type pull down to All Files (*), then highlight the file which could have any arbitrary name but commonly does have a .inj extension, click the OK button.   Assuming there are no problems with the file, no Console error or warning message will appear in fluent.   As you will be returned to the "Injections" dialog box, you should see the same Injection name that you specified in the "Set Injection Properties" dialog and be able to List its Particles and Properties in the console.  Next open the Discrete Phase Model Dialog Box and select Interaction with Continuous Phase which will enable updating DPM source terms every flow iteration.  This setting can be saved in your cas file or added via the journal file as shown.  Once the injection is confirmed working in the gui the steps can be automated by adding commands to the journal file after solution initialization, for example:
 /define/models/dpm/interaction/coupled-calculations yes
 /define/models/dpm/injections/delete-injection injection-0:1
 /define/models/dpm/injections/create injection-0:1 no yes file no zinjection01.inj no no no no
 /define/models/dpm/injections/list-particles injection-0:1
 /define/models/dpm/injections/list-injection-properties injection-0:1
where a basic manually created injection steady file format might look like:
  $ cat  zinjection01.inj
  (z=4 12)
  ( x          y        z    u         v    w    diameter  t         mass-flow  mass  frequency  time name )
  (( 2.90e-02  5.00e-03 0.0 -1.00e-03  0.0  0.0  1.00e-04  2.93e+02  1.00e-06   0.0   0.0        0.0 ) injection-0:1 )
noting that injection files for DPM simulations are generally setup for either steady or unsteady particle tracking where the format of the former is described in subsection Part III: Solution Mode | Chapter 24: Modeling Discrete Phase | 24.3. Setting Initial Conditions for the Discrete Phase | 24.3.13 Point Properties for File Injections | 24.3.13.1 Steady File Format of the 2024R2 Fluent Customization Manual.

== CFX ==

=== Slurm scripts ===

A summary of command-line options can be printed by running cfx5solve -help where the same module version thats loaded in your slurm script should be first manually loaded.  By default cfx5solve will run in single precision (-single).  To run cfx5solve in double precision add the -double option noting that doing so will also double memory requirements.  By default cfx5solve can support meshes with up to 80 million elements (structured) or 200 million elements (unstructured).  For larger meshes with up to 2 billion elements, add the -large option.  Various combinations of these options can be specified for the Partitioner, Interpolator or Solver.  Consult the ANSYS CFX-Solver Manager User's Guide for further details.

== Workbench ==

Before submitting a Workbench job to the queue with a slurm script, you must initialize it once as described in the following steps.
# On the cluster where you will submit workbench jobs (Nibi for example) open an OnDemand desktop.  For the purpose of this section it will be sufficient and fastest to select either a Compute Desktop (without a GPU) or a Basic Desktop resource.
# Once the desktop appears, open a terminal window and cd into your directory containiong your YOURPROJECT.wbpj file.
# Remove the old project cache directory by running rm -rf _ProjectScratch as this can be very large from previous runs.
# Open a terminal window and load the module version that you will be using in your slurm script for example module load ansys/2025R2.04
# Open the Workbench gui with your project file.  This can be done by issuing runwb2 -f YOURPROJECT.wbpj directly from the command line.  If and when a popup appears asking "Do you want to recover the project before opening ? (Any changes made since the last save will be lost.)" answer No.
# In the context menu popup that should appear in the center Project Schematic window, right-click on Model and select Reset.  When Ansys Workbench pops up a warning that "This operation will delete the operations local and generated data" click Ok to accept and proceed.
# In the top menu bar pulldown, select File -> Save then File -> Exit to shutdown Workbench.
# In the Ansys Workbench popup, when asked The current project has been modified. Do you want to save it?, click on the No button.
# Quit Workbench and submit your job using one of the Slurm scripts shown below.

Since a Compute Node with upto 96cores, 768GB memory and 8hours runtime can now be reserved for an OnDemand desktop session, consider running your Workbench simulations directly from within the Workbench native gui when possible as a more intuitive option compared to submitting the job to the queue with a slurm script.

=== Slurm scripts ===

A project file can be submitted to the queue by customizing one of the following scripts and then running the sbatch script-wbpj-202X.sh command:

To avoid writing the solution when a running job successfully completes change Save(Overwrite=True) to Save(Overwrite=False) in the last line of the above slurm script.  Doing this will make it easier to determine how well the simulation scales when #SBATCH --ntasks is increased since the initialized solution will not be overwritten by each test job.

== Mechanical ==

The input file can be generated from within your interactive Workbench Mechanical session by clicking Solution -> Tools -> Write Input Files then specify File name: YOURAPDLFILE.inp and Save as type: APDL Input Files (*.inp).  APDL jobs can then be submitted to the queue by running the sbatch script-name.sh command.

=== Slurm scripts ===

In the following slurm scripts, lines beginning with ##SBATCH are commented.

Ansys allocates 1024 MB total memory and 1024 MB database memory by default for APDL jobs. These values can be manually specified (or changed) by adding arguments -m 1024 and/or -db 1024 to the mapdl command line in the above scripts. When using a remote institutional license server with multiple Ansys licenses, it may be necessary to add -p aa_r or -ppf anshpc, depending on which Ansys module you are using. As always, perform detailed scaling tests before running production jobs to ensure that the optimal number of cores and minimum amount memory is specified in your scripts. The single node (SMP Shared Memory Parallel) scripts will typically perform better than the multinode (DIS Distributed Memory Parallel) scripts and therefore should be used whenever possible. To help avoid compatibility issues the Ansys module loaded in your script should ideally match the version used to generate the input file:

 [gra-login2:~/testcase] cat YOURAPDLFILE.inp | grep version
 ! ANSYS input file written by Workbench version 2019 R3

== Rocky ==

This section provides sample slurm scripts to solve standalone non-coupled Rocky simulations in a cluster queue. Both scripts are configured with RESUME=0 so simulations are solved from the beginning by default.  To restart a partially completed simulation set RESUME=1 and resubmit the script to the queue.  To get a full listing of command line options run Rocky -h on the command line after loading the ansys module.  Since a lock file is generated every time a simulation is started, only one job should be submitted at a time from the same directory. Regarding which script to use, while all simulations should be tested independently, for a basic test case the GPU only script was found to outperform the CPU only script by a factor of 3.5x. Further increases in resources beyond 6cpus (for the CPU only script) or 2cpu + 1g (1/7 of a H100 gpu for the GPU based script) provided no further speedup based on scaling testing for either script.   Given these results it appears likely the GPU based script will provide significantly faster solution times compared to just using CPUS for other standalone Rocky simulations.  As shown in on each cluster wiki page or as summarized on in https://docs.alliancecan.ca/wiki/Allocations_and_compute_scheduling#Ratios_in_bundles all clusters but narval have H100 gpus.  Therefore when using the GPU script on Narval the --gpus slurm option should be changed to instead request an a100 gpu.  Note that at this time only Rocky with the ansys/2025R2|2.04 modules have been tested but not the ansys/2025R1|1.02 modules yet.

=== Slurm scripts ===

== Electronics ==

Slurm scripts for using AnsysEDT is provided in a separate wiki page here.

= Graphical use =

To run Ansys programs in graphical mode using an OnDemand or Jupyterhub desktop click one of the following links :

 NIBI: https://ondemand.sharcnet.ca
 FIR: https://jupyterhub.fir.alliancecan.ca
 RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
 NARVAL:  https://jupyterhub.narval.alliancecan.ca/
 TRILLIUM: https://ondemand.scinet.utoronto.ca

A job submission web page should appear in your browser.  Configure the resources required for your interactive desktop session and click Launch or Start.  If either accelerated graphics or computations will be conducted from within your desktop session then be sure to specify a GPU resource.  Once the desktop load an ansys module.  If you started a Juypter Lab powered desktop then this can be done by clicking the left hand menu, or if you started an OnDemand desktop manually type module load ansys/version on the command line.  To start one the common Ansys programs such as fluent, cfx, workbench and so forth refer to the following section which provides advice for setting environment variables and arguments required by virtualgl or mesa based graphical environments depending on whether a node with a GPU resource was specified or not.

=== Fluent ===

To start Ansys Fluent from the command line of an On Demand Desktop, open a terminal window and run the commands:

::: module load StdEnv/2023 ansys/2025R2.04
::: fluent

When the Fluent Launcher popup selector panel appears, click the Environment Tab and copy/paste the following environment variable settings, depending on whether you started your On Demand session with a GPU for graphical acceleration. Do not include the text between the round brackets (as these are comments) and do not put export in front of any variable names.  If the graphics console window becomes corrupted when starting the gui, restart fluent setting HOOPS_PICTURE=null to disable creation of the Graphics panel.

Compute Node (no GPU requested)

::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on nibi w/ intelmpi)
::: HOOPS_PICTURE=opengl2-mesa    (version 2025R1 or newer)
::: HOOPS_PICTURE=x11/lin                (version 2024R2.04 or older)
::: Click the Start button

Compute Node (with GPU requested)

To use hardware accelerated graphics with fluent on nibi cluster choose a t4 (15GB) from the GPU selector pulldown list for your OnDemand desktop session.  Doing this will ensure the environment variables used by VirtualGL to enable accelerated OpenGL graphics calls are automatically setup inside your Deskop environment for the current session.  Once your desktop appears, open a terminal window and start workbench as follows :
::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on nibi)
::: HOOPS_PICTURE=opengl2    (version 2025R1 or newer)
::: HOOPS_PICTURE=opengl                 (version 2024R2.04 or older)
::: Click the Start button

NOTE: When running fluent on the Nibi cluster, the environment variable I_MPI_HYDRA_BOOTSTRAP=ssh must be manually set; otherwise, fluent will crash when started inside OOD Compute Desktop sessions when intelmpi is used.  Error output such as the following will be created.  Should this occur, completely exit fluent, cleanly shut down workbench and start over again.
 [mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
 [mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
 [mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
 [mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
 [mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

=== CFX ===

When starting CFX from an On Demand Desktop the following arguments maybe specified on the terminal window command line depending on whether a GPU was requested when the Desktop was started.

::: module load StdEnv/2023 ansys/2025R1  (or older)
::: cfx5 -graphics mesa   (no GPU requested)
::: cfx5 -graphics ogl    (with GPU requested)

=== Mapdl ===

The following steps for starting the Mechanical APDL gui from the command line of a terminal window should work regardless if you have started your On Demand Desktop on a Compute node with or without a gpu.

::: module load StdEnv/2023 ansys/2022R2 (or newer versions)
::: mapdl -g, or,
::: launcher then click RUN button

=== Workbench ===

This sections shows howto start workbench (and optionally fluent) on either an On Demand Desktop or Jupyter Lab Desktop.

==== OnDemand Desktop ====

Compute Node (no GPU requested) or Basic Desktop

If accelerated graphics is not required for your desktop session then specify GPU Node to select a Compute Node without a GPU for your OOD session.  Doing this will use mesa software emulation for opengl calls instead of running on a more expensive and difficult to reserve GPU node :
::: module load StdEnv/2023 ansys/2025R2.04
::: runwb2

To start fluent from within workbench click Fluid Flow (Fluent) or (Fluent with Fluent Meshing) in the left hand Analysis Menu, then click Setup in the center canvas Fluid Flow (Fluent) popup.  Once the Fluent Launcher selector panel popup appears, click the Environment Tab and copy/paste the following environment variable settings:
::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on nibi cluster only)
::: HOOPS_PICTURE=opengl2-mesa    (optional for 2025R1 or newer)
::: Click the Start button

Compute Node (with GPU requested)

If accelerated graphics is required on nibi cluster then choose t4 (15GB) from the GPU selector pulldown list for your OnDemand desktop session.  Doing this will ensure the environment variables used by VirtualGL to enable accelerated OpenGL graphics calls are automatically setup inside your Deskop environment for the current session.  Once your desktop appears, open a terminal window and start workbench as follows :
::: module load StdEnv/2023 ansys/2025R2.04
::: runwb2

To start fluent from within workbench, click Fluid Flow (Fluent) or (Fluent with Fluent Meshing) in the left hand Analysis Menu, then click Setup in the center canvas Fluid Flow Fluent) popup.  Once the Fluent Launcher selector panel popup appears, click the Environment Tab and copy/paste the following environment variable settings.
::: I_MPI_HYDRA_BOOTSTRAP=ssh     (required on nibi cluster only)
::: HOOPS_PICTURE=opengl2             (optional for 2025R1 or newer)
::: Click the Start button

When using nibi cluster I_MPI_HYDRA_BOOTSTRAP=ssh must be manually set when the default intelmpi is used otherwiose fluent will crash on startup producing error output such as the following.  To recover from this close fluent, shutdown workbench and try again.
 [mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
 [mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
 [mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
 [mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
 [mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

==== Jupyterhub Desktop ====

Compute Node (no GPU requested)

::: Click to load ansys/2025R1 (or newer version) in the Desktop left hand side menu
::: Click the "Workbench (VNC)" icon located in the Jupyter Lab desktop center window.
:::: If the graphics of any application (such as fluent) started within workbench
:::: appear unusable due to corrupted graphics then try carrying out the following
:::: steps.  They will create a custom runwb2 desktop icon so that workbench
:::: can be started mesa mode.  If the one of the applications that you will be starting
:::: in workbench is fluent then when the Fluent launcher starts you may also try setting
:::: HOOPS_PICTURE=opengl2-mesa variable in the Fluent Launcher window.
::: To proceed, exit Workbench and then open a terminal window.  Copy paste the following
::: command into the Remote Clipboard located in the top right corner of your jupyter desktop.
::: Now the commands can be pasted into terminal ie)
::: cd ~/Desktop; cp -p $(realpath workbench.desktop) workbench-mesa.desktop
::: Open the newly created file in a text editor such as nano by doing the following:
::: nano ~/Desktop/workbench-mesa.desktop.  Change all instances of runwb2
::: to  runwb2 -oglmesa and then exit the editor saving the changes.  Now REFRESH
::: the Jupyter desktop by pressing the key combination control-R.  The new icon should now
::: appear in the desktop along with the original workbench icon. Double click it to start workbench.
::: The new icon will persist for future sessions until manually deleted with the command
::: rm -f ~/Desktop/workbench-mesa.desktop.

Compute Node (with GPU requested)

::: Click to load ansys/2025R1 (or newer version) in the Desktop left hand side menu
::: Click the Workbench (VNC) icon located in the Jupyter Lab desktop center window

=== Ensight ===
::: module load StdEnv/2023 ansys/2022R2; A=222; B=5.12.6
::: export LD_LIBRARY_PATH=$EBROOTANSYS/v$A/CEI/apex$A/machines/linux_2.6_64/qt-$B/lib
::: ensight -X

=== Rocky ===
::: module load StdEnv/2023 ansys/2025R2.04 (or 2025R1, 2025R1.02, 2025R2)
::: Rocky The Rocky command starts rocky in standalone gui mode
::: RockySolver Run the solver directly from command line (untested)
::: RockySchedular Gui to interactively submit/run jobs on present node (untested)
::: o The ansys module handles reading your ~/licenses/ansys.lic file
::: o The SHARCNET ansys license includes Rocky thus free to use

== Electronics ==

Information describing howto run AnsysEDT in graphical mode maybe found here here.

= Site-specific usage =

== SHARCNET license ==

The SHARCNET Ansys license is free for academic use by any Alliance researcher on any Alliance system.   The installed software does not have any solver or geometry limits.  The SHARCNET license may be used for Publishable Academic Research but not for any private/commercial purposes as this is strictly prohibited by the license terms.  The SHARCNET Ansys license is based on the Multiphysics Campus Solution and includes products such as: HF, EM, Electronics HPC, Mechanical, CFD, ROCKY and LS-DYNA as described here. Lumerical software is included in recent ansys module versions however it is NOT covered by the SHARCNET license.  SpaceClaim software is not installed with any ansys module since there is no linux version available however it is technically covered by the SHARCNET license.

 ⚖️ Scaling tests should be run before launching long jobs to the determine optimal scalable job size so that the limited licenses and hardware is used as efficiently as possible and total job run and startup times are minimized.  Parallel jobs that do not achieve at least 50% CPU utilization will probably be flagged by the system, resulting in a followup by an Alliance team member.

The SHARCNET Ansys license is made available on a first come first serve basis.  It currently permits each researcher to run a maximum of simultaneous 16 jobs using a total of upto 512 hpc cores across all clusters, therefore any of the following maximum job size combinations can be run simultaneously: 1x512, 2x256, 4x128, 8x64, 16x32 or more commonly one of these full node combinations: 1x384, 2x192 or 1x192 cores.  Note however the SHARCNET license is oversubscribed so there is potential for jobs to fail on startup if all (or nearly all) of the 1986 anshpc licenses in the SHARCNET license pool are in use.  Should this occur you will need to manually resubmit your job to the queue.   If over time there is an increasing number of license shortage instances then the total anshpc core limit per researcher maybe decreased from 512 to 384.  If you need more than 512 hpc cores for your research then consider using the local ANSYS License server at your institution if one is available OR open a ticket to request help purchasing additional licenses for the SHARCNET license in which case your maximum job size anshpc limit would be increased respectively.

==== License file ====

As of February 2026 the old license3.sharcnet.ca license server has been permanently shutdown.  To use the SHARCNET Ansys license on any Alliance cluster, simply configure your ansys.lic file as follows instead:

[username@cluster:~] cat ~/.licenses/ansys.lic
setenv("ANSYSLMD_LICENSE_FILE", "1055@license1.computecanada.ca")

==== License query  ====

To show the number of ansys licenses in use by your username and the total in use by all users, run:

ssh nibi.alliancecan.ca
module load ansys
$EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil \
lmstat -c $ANSYSLMD_LICENSE_FILE -a | grep "Users of\|$USER" | grep -v " Total of 0 licenses in use"

==== Example  ====

Consider the case where a user submits a 8core fluent job and 32core fluent job.  Once both jobs start running, the user runs the lmutil queuery command and the output shown below is generated.  Here it can be seen that a total of (8-4) + (32-4) = 32 anshpc licenses are used by the two jobs.  As a result the total number of anshpc licenses increases from 1568 to 1600 so that only (1986-1600) = 386 anshpc licenses remain available for additional jobs submitted by all users.  Therefore if a 400 core parallel job attempts to start at this moment, it will fail to start since (400-4) = 396 anshpc licenses would be required.   The user has two options, wait for a sufficient number of  anshpc licenses to come available OR reduce the job size to 390 cores or less and resubmit immediately.  This example focuses on the anshpc feature since it is most generously overcommitted to allow any user to submit the largest job possible, but it also shows that the actual number of anshpc licenses available per user may sometimes be far less than the 512 per user limit would suggest.

 [l2(nibi):~] sq
            JOBID     USER        ACCOUNT           NAME  ST  TIME_LEFT NODES CPUS MIN_MEM NODELIST (REASON)
         10161023  roberpj   cc-debug_cpu script-flu-int   R    2:57:19     4    8     N/A      4G c[630-633] (None)
         10161033  roberpj   cc-debug_cpu script-flu-int   R    2:58:25    16   32     N/A      4G c[627-628,630-633,637,642,645,655,657,662,665,667,669,682] (None)
 [l2(nibi):~]
 [l2(nibi):~] module load ansys
 [l2(nibi):~]
 [l2(nibi):~] $EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil  \
              lmstat -c $ANSYSLMD_LICENSE_FILE -a | grep "Users of\|$USER" | grep -v " Total of 0 licenses in use"
 Users of anshpc:  (Total of 1986 licenses issued;  Total of 1600 licenses in use)
    roberpj c630 c630.nibi.sharcnet 1238925 (v2025.0506) (license1.computecanada.ca/1055 2579), start Wed 3/11 16:46, 4 licenses, PID: 1239140
    roberpj c627 c627.nibi.sharcnet 509821 (v2025.0506) (license1.computecanada.ca/1055 5716), start Wed 3/11 16:48, 28 licenses, PID: 510058
 Users of cfd_base:  (Total of 275 licenses issued;  Total of 19 licenses in use)
    roberpj c630 c630.nibi.sharcnet 1238925 (v2025.0506) (license1.computecanada.ca/1055 10327), start Wed 3/11 16:46, PID: 1239140
    roberpj c627 c627.nibi.sharcnet 509821 (v2025.0506) (license1.computecanada.ca/1055 7171), start Wed 3/11 16:47, PID: 510058
 Users of cfd_preppost:  (Total of 275 licenses issued;  Total of 1 license in use)
 Users of cfd_preppost_pro:  (Total of 275 licenses issued;  Total of 1 license in use)
 Users of cfd_solve_level1:  (Total of 275 licenses issued;  Total of 18 licenses in use)
    roberpj c630 c630.nibi.sharcnet 1238925 (v2025.0506) (license1.computecanada.ca/1055 7994), start Wed 3/11 16:46, PID: 1239140
    roberpj c627 c627.nibi.sharcnet 509821 (v2025.0506) (license1.computecanada.ca/1055 6200), start Wed 3/11 16:47, PID: 510058
 Users of cfd_solve_level2:  (Total of 275 licenses issued;  Total of 18 licenses in use)
    roberpj c630 c630.nibi.sharcnet 1238925 (v2025.0506) (license1.computecanada.ca/1055 10520), start Wed 3/11 16:46, PID: 1239140
    roberpj c627 c627.nibi.sharcnet 509821 (v2025.0506) (license1.computecanada.ca/1055 375), start Wed 3/11 16:47, PID: 510058
 Users of elec_solve_hfss:  (Total of 275 licenses issued;  Total of 1 license in use)
 Users of elec_solve_level1:  (Total of 275 licenses issued;  Total of 1 license in use)
 Users of elec_solve_level2:  (Total of 275 licenses issued;  Total of 1 license in use)

 🕵 A rare situation can occur where the output from the License query command reveals there are some Ansys licenses unexpectedly still in use by your username on some desktop or compute node.  For instance if an ansys gui program run on a remote desktop node was not shutdown cleanly leaving some ansys processes still running.  Or an ansys program crashes on a cluster compute node inside an salloc session that was being run interactively from the command line, once again leaving some rogue ansys processes still running.  To kill all potentially responsible ansys rogue processes either close the desktop, scancel the salloc session, or simply open a terminal window on the effected node and issue the  command pkill -9 -e -u $USER -f "ansys".  Any ansys licenses that were being held open should immediately be returned to the SHARCNET license server and become available for use again by yourself or other researchers.

= Additive Manufacturing =

To get started configure your ~/.licenses/ansys.lic file to point to a license server that has a valid Ansys Mechanical License.  This must be done on all systems where you plan to run the software.

== Enable Additive ==

This section describes how to make the Ansys Additive Manufacturing ACT extension available for use in your project. The steps must be performed on each cluster for each ansys module version where the extension will be used. Any extensions needed by your project will also need to be installed on the cluster as described below.  If you get warnings about missing un-needed extensions (such as ANSYSMotion) then uninstall them from your project.

=== Download Extension ===
* download AdditiveWizard.wbex from https://catalog.ansys.com/
* upload AdditiveWizard.wbex to the cluster where it will be used

=== Start Workbench ===
* follow the Workbench section in Graphical use above.
* File -> Open your project file (ending in .wbpj) into Workbench gui

===  Open Extension Manager ===
* click ACT Start Page and the ACT Home page tab will open
* click Manage Extensions and the Extension Manager will open

=== Install Extension ===
* click the box with the large + sign under the search bar
* navigate to select and install your AdditiveWizard.wbex file

=== Load Extension ===
* click to highlight the AdditiveWizard box (loads the AdditiveWizard extension for current session only)
* click lower right corner arrow in the AdditiveWizard box and select Load extension (loads the extension for current AND future sessions)

=== Unload Extension ===
* click to un-highlight the AdditiveWizard box (unloads extension for the current session only)
* click lower right corner arrow in the AdditiveWizard box and select Do not load as default (extension will not load for future sessions)

== Run Additive ==

=== OnDemand ===

A user can run a single Ansys Additive Manufacturing job in an graphical OnDemand session by doing:

* Start Workbench as described above in Enable Additive.
* click File -> Open and select test.wbpj then click Open
* click View -> reset workspace if you get a grey screen
* start Mechanical, Clear Generated Data, tick Distributed, specify Cores
* click File -> Save Project -> Solve

Check utilization:
* open another terminal and run: top -u $USER   **OR**  ps u -u $USER | grep ansys
* kill rogue processes from previous runs:  pkill -9 -e -u $USER -f "ansys|mwrpcss|mwfwrapper|ENGINE"

Please note that rogue ansys related processes can persistently continue tie up valuable licenses inside a running OnDemand login node sessions if an ansys gui session (fluent, workbench, mechanical, etc) is not cleanly terminated by the user or is terminated unexpectedly by a network outage or hung filesystem.  If the latter is to blame the processes may not by killable until normal disk access is restored.

===Cluster===

Project preparation:

Before submitting a newly uploaded Additive project to a cluster queue (with sbatch scriptname) certain preparations must be done.  To begin, open your simulation with Workbench gui (as described in the Enable Additive section above) in the same directory that your job will be submitted from and then save it again. Be sure to use the same ansys module version that will be used for the job.  Next create a Slurm script (as explained in the Cluster Batch Job Submission - WORKBENCH section above).  To perform parametric studies, change Update() to UpdateAllDesignPoints() in the Slurm script.  Determine the optimal number of cores and memory by submitting several short test jobs.  To avoid needing to manually clear the solution and recreate all the design points in Workbench between each test run, either 1) change Save(Overwrite=True) to Save(Overwrite=False) or 2) save a copy of the original YOURPROJECT.wbpj file and corresponding YOURPROJECT_files directory.  Optionally create and then manually run a replay file on the cluster in the respective test case directory between each run, noting that a single replay file can be used in different directories by opening it in a text editor and changing the internal FilePath setting.

 module load ansys/2019R3
 rm -f test_files/.lock
 runwb2 -R myreplay.wbjn

Resource utilization:

Once your additive job has been running for a few minutes, a snapshot of its resource utilization on the compute node(s) can be obtained with the following srun command.  Sample output corresponding to an eight core submission script is shown next.  It can be seen that two nodes were selected by the scheduler:

 [gra-login1:~] srun --overlap --jobid=myjobid top -bn1 -u $USER | grep R | grep -v top
   PID USER   PR  NI    VIRT    RES    SHR S  %CPU %MEM    TIME+  COMMAND
 22843 demo   20   0 2272124 256048  72796 R  88.0  0.2  1:06.24  ansys.e
 22849 demo   20   0 2272118 256024  72822 R  99.0  0.2  1:06.37  ansys.e
 22838 demo   20   0 2272362 255086  76644 R  96.0  0.2  1:06.37  ansys.e
   PID USER   PR  NI    VIRT    RES    SHR S  %CPU %MEM    TIME+  COMMAND
  4310 demo   20   0 2740212 271096 101892 R 101.0  0.2  1:06.26  ansys.e
  4311 demo   20   0 2740416 284552  98084 R  98.0  0.2  1:06.55  ansys.e
  4304 demo   20   0 2729516 268824 100388 R 100.0  0.2  1:06.12  ansys.e
  4305 demo   20   0 2729436 263204 100932 R 100.0  0.2  1:06.88  ansys.e
  4306 demo   20   0 2734720 431532  95180 R 100.0  0.3  1:06.57  ansys.e

Scaling tests:

After a job completes, its "Job Wall-clock time" can be obtained from seff myjobid.  Using this value, scaling tests can be performed by submitting short test jobs with an increasing number of cores.  If the Wall-clock time decreases by ~50% when the number of cores is doubled, additional cores may be considered.

= Help resources =

The official full documentation for recent versions Ansys 202[4|5]R[1|2] is available here.  Documentation for older versions such as Ansys 2023R[1|2] however requires login.  Developer documentation can be found in the Ansys Developer Portal. Additional learning resources include the Ansys HowTo videos, the Ansys Educator Educator Hub and the Ansys Webinar series.

XoverSSH Legacy Note: Some programs can be run remotely on a cluster compute node by forwarding X over SSH to your local desktop.  Unlike VNC, this approach is untested and unsupported since it relies on a properly setup X display server for your particular operating system OR the selection, installation and configuration of a suitable X client emulator package such as MobaXterm.  Most users will find interactive response times unacceptably slow for basic menu tasks let alone performing more complex tasks such as those involving graphics rendering.  Startup times for GUI programs can also be very slow depending on your Internet connection. For example, in one test it took 40 minutes to fully start the gui up over SSH while starting it with vncviewer required only 34 seconds.  Despite the potential slowness, using this method to connect may still be of interest if your only goal is to open a simulation and perform some basic menu operations or run some calculations and response delays can be tolerated. The basic steps are given here as a starting point: 1) ssh -Y username@alliancecan.ca 2) salloc --x11 --time=1:00:00 --mem=16G --cpus-per-task=4 [--gpus-per-node=1] --account=def-mygroup; 3) once connected onto a compute node try running xclock.  If the clock appears on your desktop, proceed to load the desired Ansys module and try running the program.