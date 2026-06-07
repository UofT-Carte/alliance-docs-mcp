---
title: "Ansys/en"
url: "https://docs.alliancecan.ca/wiki/Ansys/en"
category: "General"
last_modified: "2026-05-30T15:02:01Z"
page_id: 4948
display_title: "Ansys"
---

TRANSLATOR'S NOTE FROM JUNE 2026: This page is currently being reviewed.

Ansys is a software suite for engineering simulation and 3-D design. It includes packages such as Ansys Fluent and Ansys CFX.

= Licensing =
The Alliance is a hosting provider for Ansys. This means that we have the software installed on our clusters, but we do not provide a generic license accessible to everyone. However, many institutions, faculties, and departments already have licenses that can be used on our clusters.  Once the legal aspects are worked out for licensing, there will be remaining technical aspects. The license server on your end will need to be reachable by our compute nodes. This will require our technical team to get in touch with the technical people managing your license software. In some cases, this has already been done. You should then be able to load the Ansys module, and it should find its license automatically. If this is not the case, please contact our technical support to arrange this.

== Configuring your license file ==
Our module for Ansys is designed to look for license information in a few places. One of those places is your /home folder. You can specify your license server by creating a file named $HOME/.licenses/ansys.lic as shown below.  Customize the file by replacing FLEXPORT and LICSERVER with the appropriate values for your server.

 FILE: ansys.lic

setenv("ANSYSLMD_LICENSE_FILE", "FLEXPORT@LICSERVER")

The following table provides established values for the CMC and SHARCNET license servers.  To use a different server, locate the corresponding value as explained in Local license servers below.

 TABLE: Preconfigured license servers

License 	System/Cluster                  	LICSERVER                	FLEXPORT	NOTES
CMC     	Fir                             	172.26.0.101             	6624    	Discontinue use (shut down April 23, 2026)
CMC     	Narval/Rorqual                  	10.100.64.10             	6624    	Discontinue use (shut down April 23, 2026)
CMC     	Nibi                            	10.25.1.56               	6624    	Discontinue use (shut down April 23, 2026)
CMC     	Trillium                        	scinet-cmc               	6624    	Discontinue use (shut down April 23, 2026)
SHARCNET	Nibi/Fir/Narval/Rorqual/Trillium	license1.computecanada.ca	1055

=== Local license servers  ===

Before a local institutional Ansys license server can be used on our clusters, firewall changes will need to be done on both the server and the cluster sides.  For many Ansys servers, this work has already been done and they can be used by following the steps in the Ready to use section below.  For Ansys servers that have never been used on our clusters, an additional step must be done as shown in the Setup required section also below.

==== Ready to use ====

To use a local institutional Ansys license server with an Alliance cluster whose network/firewall connections have already been set up, contact your Ansys server administrator and get the following pieces of information for the license server:
 1) the Ansys flex port (FLEXPORT) number, commonly 1055
 2) the fully qualified hostname (LICSERVER)
Now, configure your ~/.licenses/ansys.lic file by plugging in the values, and you are done.

==== Setup required ====

To use a local Ansys license server with an Alliance cluster whose network/firewall connection have never been set up before, you will also need to get the following from your ANSYS server administrator:
  3) the statically configured Ansys vendor port (VENDPORT) number.
Send items 1 → 3 by email to technical support and mention which Alliance cluster you want to run Ansys jobs on.  An Alliance system administrator will then open the outbound cluster firewall (if necessary) so license checkout requests can reach your license server from the cluster's compute nodes.  A range of IP addresses (known as cluster NAT nodes) will then be sent back to you.  Give these IP addresses to your local network administrator and request the local server firewall FLEXPORT and VENDPORT ports be opened to allow connections from all of them.  Also ask the administrator to check that the line containing SERVER    found at the top of the Ansys license file contains either LICSERVER or IP_ADDRESS for the  value as this must be resolvable from the remote cluster.

== Checking out a license ==

To test if your ansys.lic is configured and working properly with your license server, run the following sequence of commands on the cluster where you will be submitting jobs.

 [login-node:~] cd /tmp
 [login-node:/tmp] salloc --time1:0:0 --mem1000M --accountdef-YOURUSERID
 [compute-node/tmp] module load StdEnv/2023; module load ansys/2025R2.04
 [compute-node:/tmp] $EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil lmstat -c $ANSYSLMD_LICENSE_FILE | grep "ansyslmd: UP" 1> /dev/null && echo Success  echo Fail
Success output indicates license checkouts should work when jobs are submitted to the queue.
Fail output indicates a problem with the licensing setup somewhere, and jobs will likely fail.

If there is an Ansys license server checkout problem, the following message will appear in Slurm output files when Fluent jobs are started by Slurm scripts in the queue *OR* when Fluent is started interactively, simply by doing the following:

 [compute-node:/tmp] fluent -g 2d -n 2
 Connected License Server List:
 Hit return to exit.

= Version compatibility =

Ansys simulations are typically forward compatible, but NOT backward compatible.  This means that simulations created using an older version of Ansys can be expected to load and run fine with any newer version.  For example, a simulation created and saved with ansys/2022R2 should load and run smoothly with ansys/2023R2. but NOT the other way around.  While it may be possible to start a simulation running with an older version, random error messages or crashing will likely occur.  Regarding Fluent simulations, if you cannot recall which version of Ansys was used to create your case file, try grepping it as follows to look for clues:

 $ grep -ia fluent combustor.cas
   (0 "fluent15.0.7  build-id: 596")

 $ grep -ia fluent cavity.cas.h5
   ANSYS_FLUENT 24.1 Build 1018

== Platform support ==

Ansys provides detailed platform support information describing software/hardware compatibility for the current and previous releases. This is of special interest since it shows which packages are supported under Windows, but not under Linux, and thus not on the Alliance clusters (e.g., SpaceClaim).

== What's new ==

Information for the latest Ansys release can be found here (Ansys 2026 R1, as of May 2026).  Posts for previous releases can be found on the Ansys blog and then scrolling down to the FILTERS search bar. Inputting for example What’s New Fluent 2024 GPU should pull up a document containing the latest GPU support information for that release. The Press Release search bar is also a good way to find release-specific information.

== Service packs ==

Starting with Ansys 2024, a separate Ansys module will appear on the clusters with a decimal and two digits following the release number whenever a service pack is installed over the initial release.  For example, the initial 2024 release with no service pack applied may be loaded with  module load ansys/2024R1 while a module with service pack 3 applied will be loaded with module load ansys/2024R1.03.  If a service pack is already available by the time a new release is to be installed, only a module for that service pack number will most likely be installed, unless a request to install the initial release is also received.

Most users will likely want to load the latest module version equipped with the latest installed service pack, which can be achieved with module load ansys.  While it's not expected service packs will impact numerical results, the changes they make are extensive and so, if computations have already been done with the initial release or an earlier service pack, some groups may prefer to continue using it. Having separate modules for each service pack makes this possible.  Starting with Ansys 2024R1, a detailed description of what each service pack does can be found by searching this link for Service Pack Details. Future versions will presumably be similarly searchable by manually modifying the version number.

= Cluster batch job submission =
The Ansys software suite comes with multiple implementations of MPI to support parallel computation. Unfortunately, none of them support our Slurm scheduler. For this reason, we need special instructions on how to start a parallel job for each Ansys package. In the sections below, we give examples of submission scripts for some of the packages.  While Slurm scripts should work on all clusters, Trillium users may need to make some additional changes covered here.

== Fluent ==
Typically, you would use the following procedure to run Fluent on one of our clusters:

# Prepare your Fluent job using Fluent from the Ansys Workbench on your desktop machine, up to the point where you would run the calculation.
# Export the case file with File > Export > Case… or find the folder where Fluent saves your project's files. The case file will often have a name like FFF-1.cas.gz.
# If you already have data from a previous calculation, which you want to continue, export a data file as well (File > Export > Data…) or find it in the same project folder (FFF-1.dat.gz).
# Transfer the case file (and if needed the data file) to a directory on the /project or /scratch filesystem on the cluster.  When exporting, you can save the file(s) under a more instructive name than FFF-1.*, or rename them when they are uploaded.
# Now you need to create a journal file. Its purpose is to load the case file (and optionally the data file), run the solver, and finally write the results.  See examples below and remember to adjust the filenames and desired number of iterations.
# If jobs frequently fail to start due to license shortages and manual resubmission of failed jobs is not convenient, consider modifying your script to requeue your job (up to 4 times) as shown under the by node + requeue tab further below.  Be aware that doing this will also requeue simulations that fail due to other related issues (such as divergence), resulting in wasted compute time.  Therefore, it is strongly recommended to monitor and inspect each Slurm output file to confirm that each requeue attempt is license-related.  When it is determined that a job is requeued due to a simulation issue, immediately kill the job progression manually with scancel jobid and correct the problem.
# After running the job, you can download the data file and import it back into Fluent with File > Import > Data….

=== Slurm scripts ===

==== General purpose ====

Most Fluent jobs should use the following by node script to minimize solution latency and maximize performance over as few nodes as possible. Very large jobs might wait less in the queue if they use a by core script; however, the startup time of a job using many nodes can be significantly longer, thus offsetting some of the benefits. In addition, be aware that running large jobs over an unspecified number of very many nodes will make them far more vulnerable to crashing if any of the compute nodes fail during the simulation. The scripts will ensure Fluent uses shared memory for communication when run on a single node, and distributed memory (utilizing MPI and the appropriate HPC interconnect) when run over multiple nodes.  The two Narval tabs may be useful to provide a more robust alternative if Fluent crashes during the initial automatic mesh partitioning phase when using the standard intel-based scripts with the parallel solver.  The other option would be to manually perform the mesh partitioning in the Fluent GUI, then try to run the job again on the cluster with the intel scripts.  Doing so will allow you to inspect the partition statistics and specify the partitioning method to obtain an optimal result.  The number of mesh partitions should be an integral multiple of the number of cores; for optimal efficiency, ensure at least 10000 cells per core.

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

The scripts in this section should only be used with Fluent jobs that are known to complete normally without generating any errors in the output, but typically require multiple requeue attempts to check out licenses.  They are not recommended for Fluent jobs that may 1) run for a long time before crashing 2) run to completion but contain unresolved journal file warnings, since in both cases the simulations will be repeated from the beginning until the maximum number of requeue attempts specified by the array value is reached.  For these types of jobs, the general purpose scripts above should be used instead.

==== Solution restart ====

The following scripts are provided to automate restarting very large jobs that require more than the typical seven-day maximum runtime window available on most clusters. Jobs are restarted from the most recently saved timestep files. A fundamental requirement is that the first timestep can be completed within the requested job array time limit (specified at the top of your Slurm script) when starting a simulation from an initialized solution field. It is assumed that a standard fixed timestep size is being used. To begin, a working set of sample.cas, sample.dat and sample.jou files must be present. Next, edit your sample.jou file to contain /solve/dual-time-iterate 1 and /file/auto-save/data-frequency 1. Then, create a restart journal file with cp sample.jou sample-restart.jou and edit the sample-restart.jou file to contain /file/read-cas-data sample-restart instead of /file/read-cas-data sample. Also comment out the initialization line with a semicolon, for example ;/solve/initialize/initialize-flow. If your second and subsequent timesteps are known to run twice as fast as the initial timestep, edit the sample-restart.jou file to add /solve/dual-time-iterate 2. By adding this specification, the solution will only be restarted after two timesteps have been completed following the initial timestep. An output file for each timestep will still be saved in the output subdirectory. The value 2 is arbitrary but should be chosen so that the time for 2 steps fits within the job array time limit. Doing so minimizes the number of solution restarts which are computationally expensive. If the first timestep performed by sample.jou starts from a converged (previous) solution, choose 1 instead of 2, since likely all timesteps will require a similar amount of walltime to complete. Assuming 2 is chosen, the total time of simulation to be completed will be 1*Dt+2*Nrestart*Dt where Nrestart is the number of solution restarts specified in the script. The total number of timesteps (and hence the number of output files generated) will therefore be 1+2*Nrestart. The value for the time resource request should be chosen so that the initial timestep and subsequent timesteps will complete comfortably within the Slurm time window specifiable up to a maximum of #SBATCH --time=07-00:00 days.

=== Journal files ===

Fluent journal files can include basically any command from Fluent's Text User Interface (TUI); commands can be used to change simulation parameters like temperature, pressure, and flow speed. You can then run a series of simulations under different conditions with a single case file, by only changing the parameters in the journal file. Refer to the Fluent User's Guide for more information, and a list of all commands that can be used.  The following journal files are set up with /file/cff-files no to use the legacy .cas/.dat file format (the default in module versions 2019R3 or older).  Set this to /file/cff-files yes instead to use the more efficient .cas.h5/.dat.h5 file format (the default in module versions 2020R1 or newer).

=== UDFs ===

The first step is to transfer your user-defined function or UDF (namely the sampleudf.c source file and any additional dependency files) to the cluster.  When uploading from a Windows machine, be sure the text mode setting of your transfer client is used, otherwise Fluent won't be able to read the file properly on the Linux cluster.  The UDF should be placed in the directory where your journal, cas, and dat files reside.  Next, add one of the following commands into your journal file before the commands that read in your simulation cas/dat files.   Regardless of whether you use the interpreted or compiled UDF approach,  before uploading your cas file onto the cluster, please check that neither the Interpreted UDFs dialog box or the UDF Library Manager dialog box are configured to use any UDF; this will ensure that only the journal file commands are in control when jobs are submitted.

==== Interpreted ====

To tell Fluent to interpret your UDF at runtime, add the following command line into your journal file before the cas/dat files are read or initialized. The filename sampleudf.c should be replaced with the name of your source file.  The command remains the same whether the simulation is being run in serial or parallel.  To ensure the UDF can be found in the same directory as the journal file, open your cas file in the Fluent GUI, remove any managed definitions, and resave it.   Doing this ensures only the following command/method is in control when Fluent runs. To use an interpreted UDF with parallel jobs, it will need to be parallelized as described in the section below.

 define/user-defined/interpreted-functions "sampleudf.c" "cpp" 10000 no

==== Compiled ====

To use this approach, your UDF must be compiled on an Alliance cluster at least once.  Doing so will create a libudf subdirectory structure containing the required libudf.so shared library.   The libudf directory cannot simply be copied from a remote system (such as your laptop) to the cluster since the library dependencies of the shared library will not be satisfied, resulting in Fluent crashing on startup.  That said, once you have compiled your UDF on an Alliance cluster, you can transfer the newly created libudf to any other Alliance cluster, providing your account loads the same StdEnv environment module version.  Once copied, the UDF can be used by uncommenting the second (load) libudf line below in your journal file when submitting jobs to the cluster.  Both (compile and load) libudf lines should not be left uncommented in your journal file when submitting jobs on the cluster, otherwise your UDF will automatically be (re)compiled for each and every job.  Not only is this highly inefficient, but it will also lead to racetime-like build conflicts if multiple jobs are run from the same directory. Besides configuring your journal file to build your UDF, the Fluent GUI may also be used.  To do this, navigate to the Compiled UDFs dialog box, add the UDF source file and click on Build.   When using a compiled UDF with parallel jobs, your source file should be parallelized as discussed in the section below.

 define/user-defined/compiled-functions compile libudf yes sampleudf.c "" ""

and/or

 define/user-defined/compiled-functions load libudf

==== Parallel ====

Before a UDF can be used with a Fluent parallel job (single node SMP and multinode MPI), it will need to be parallelized.  By doing this we control how/which processes (host and/or compute) run specific parts of the UDF code when Fluent is run in parallel on the cluster. The instrumenting procedure involves adding compiler directives, predicates, and reduction macros into your working serial UDF. Failure to do so will result in Fluent running slow at best, or immediately crashing at worst.  The end result will be a single UDF that runs efficiently when Fluent is used in both serial and parallel mode.  The topic is described in detail in Parallel Considerations] .

==== DPM ====
UDFs can be used to customize Discrete Phase Models (DPM) as described in
* 2024R2 Fluent Users Guide: Part III: Solution Mode | Chapter 24: Modeling Discrete Phase | 24.2 Steps for Using the Discrete Phase Models| 24.2.6 User-Defined Functions, and
* 2024R2 Fluent Customization Manual: Part I: Creating and Using User Defined Functions | Chapter 2: DEFINE Macros | 2.5 Discrete Phase Model (DPM) DEFINE Macros.
Before a DMP-based UDF can be worked into a simulation, the injection of a set of particles must be defined by specifying Point Properties with variables such as source position, initial trajectory, mass flow rate, time duration, temperature, and so forth, depending on the injection type.  This can be done in the GUI by clicking on Physics panel --> Discrete Phase to open the Discrete Phase Model box and then clicking on the Injections button.  Doing so will open an Injections dialog box where one or more injections can be created by clicking on the Create button. The Set Injection Properties dialog which appears will contain an Injection Type pulldown where available types are single, group, surface, and flat-fan-atomizer. If you select any of these, you can then select the Point Properties tab to input the corresponding value fields.  Another way to specify the Point Properties would be to read an injection text file.  To do this, select File from the Injection Type pulldown, specify the Injection Name to be created, and click on the File button (located beside the OK button at the bottom of the dialog).  Here, either an Injection Sample File (with a .dpm extension) or a manually created injection text file can be selected. To select the file in the Select File dialog box that change the File of type pull down to All Files (*), then highlight the file which could have any arbitrary name but commonly has an .inj extension, click the OK button.   Assuming there are no problems with the file, no console error or warning message will appear.   As you will be returned to the Injections dialog box, you should see the same injection name that you specified in the Set Injection Properties dialog and be able to list its particles and properties in the console.  Next, open the Discrete Phase Model dialog box and select Interaction with Continuous Phase which will enable updating DPM source terms every flow iteration.  This setting can be saved in your cas file or added via the journal file as shown.  Once the injection is confirmed working in the GUI, the steps can be automated by adding commands to the journal file after the solution initialization, for example
 /define/models/dpm/interaction/coupled-calculations yes
 /define/models/dpm/injections/delete-injection injection-0:1
 /define/models/dpm/injections/create injection-0:1 no yes file no zinjection01.inj no no no no
 /define/models/dpm/injections/list-particles injection-0:1
 /define/models/dpm/injections/list-injection-properties injection-0:1
where a basic manually created injection steady file format might look like
  $ cat  zinjection01.inj
  (z=4 12)
  ( x          y        z    u         v    w    diameter  t         mass-flow  mass  frequency  time name )
  (( 2.90e-02  5.00e-03 0.0 -1.00e-03  0.0  0.0  1.00e-04  2.93e+02  1.00e-06   0.0   0.0        0.0 ) injection-0:1 )
Note that injection files for DPM simulations are generally set up for either steady or unsteady particle tracking where the format of the former is described in 2024R2 Fluent Customization Manual Part III: Solution Mode | Chapter 24: Modeling Discrete Phase | 24.3. Setting Initial Conditions for the Discrete Phase | 24.3.13 Point Properties for File Injections | 24.3.13.1 Steady File Format.

== CFX ==

=== Slurm scripts ===

A summary of command-line options can be printed by running cfx5solve -help where the same module version loaded in your Slurm script should be first manually loaded.  By default cfx5solve will run in single precision (-single).  To run  in double precision add the -double option, noting that doing so will also double memory requirements.  By default cfx5solve can support meshes with up to 80 million elements (structured) or 200 million elements (unstructured).  For larger meshes with up to 2 billion elements, add the -large option.  Various combinations of these options can be specified for the Partitioner, Interpolator or Solver.  Consult the ANSYS CFX-Solver Manager User's Guide for further details.

== Workbench ==

Before submitting a Workbench job to the queue with a Slurm script, you must initialize it once as described in the following steps.
# On the cluster where you will submit Workbench jobs, start an OnDemand desktop.
# Once the desktop appears, open a terminal window and cd into the directory containing your YOURPROJECT.wbpj file.
# Remove the old project cache directory by running rm -rf _ProjectScratch as this can be very large from previous runs.
# Open a terminal window and load the module version that you will be using in your Slurm script for example module load ansys/2025R2.04.
# Open the Workbench GUI with your project file.  This can be done by issuing runwb2 -f YOURPROJECT.wbpj directly from the command line.  If and when a popup appears asking Do you want to recover the project before opening ? (Any changes made since the last save will be lost.) answer No.
# In the context menu popup that should appear in the centre Project Schematic window, right-click on Model and select Reset.  When Ansys Workbench pops up a warning that This operation will delete the operations local and generated data click on Ok to accept and proceed.
# In the top menu bar pulldown, select File -> Save then File -> Exit to shut down Workbench.
# In the Ansys Workbench popup, when asked The current project has been modified. Do you want to save it?, click on the No button.
# Quit Workbench and submit your job using one of the Slurm scripts shown below.

Since a compute node with up to 96cores, 768GB memory and 8hours runtime can now be reserved for an OnDemand desktop session, consider running your Workbench simulations directly from within the Workbench native GUI when possible. This is a more intuitive option compared to submitting the job to the queue with a Slurm script.

=== Slurm scripts ===

A project file can be submitted to the queue by customizing one of the following scripts and then running the sbatch script-wbpj-202X.sh command.

To avoid writing the solution when a running job successfully completes, change Save(Overwrite=True) to Save(Overwrite=False) in the last line of the above Slurm script.  Doing this makes it easier to determine how well the simulation scales when #SBATCH --ntasks is increased, since the initialized solution will not be overwritten by each test job.

== Mechanical ==

The input file can be generated from within your interactive Workbench Mechanical session by clicking on Solution -> Tools -> Write Input Files then specifying File name: YOURAPDLFILE.inp and Save as type: APDL Input Files (*.inp).  APDL jobs can then be submitted to the queue with the sbatch script-name.sh command.

=== Slurm scripts ===

In the following scripts, lines beginning with ##SBATCH are commented.

Ansys allocates 1024 MB total memory and 1024 MB database memory by default for APDL jobs. These values can be manually specified (or changed) by adding arguments -m 1024 and/or -db 1024 to the mapdl command line in the above scripts. When using a remote institutional license server with multiple Ansys licenses, it may be necessary to add -p aa_r or -ppf anshpc, depending on which Ansys module you are using. As always, perform detailed scaling tests before running production jobs to ensure that the optimal number of cores and minimum amount memory is specified in your scripts. The single node (SMP shared memory parallel) scripts will typically perform better than the multinode (DIS distributed memory parallel) scripts and therefore should be used whenever possible. To help avoid compatibility issues, the Ansys module loaded in your script should ideally match the version used to generate the input file.

  [gra-login2:~/testcase] cat YOURAPDLFILE.inp | grep version
 ! ANSYS input file written by Workbench version 2019 R3

== Rocky ==

This section provides sample Slurm scripts to solve standalone non-coupled Rocky simulations in a cluster queue. Both scripts are configured with RESUME=0 so simulations are solved from the beginning by default.  To restart a partially completed simulation, set RESUME=1 and resubmit the script to the queue.  To get a full listing of command line options, run Rocky -h on the command line after loading the Ansys module.  Since a lock file is generated every time a simulation is started, only one job should be submitted at a time from the same directory. Regarding which script to use, while all simulations should be tested independently, for a basic test case the GPU only script was found to outperform the CPU only script by a factor of 3.5x. Further increases in resources beyond 6cpus (for the CPU only script) or 2cpu + 1g (1/7 of a H100 GPU for the GPU based script) provided no further speedup based on scaling testing for either script.   Given these results, it appears likely that the GPU-based script will provide significantly faster solution times compared to just using CPUs for other standalone Rocky simulations.  As shown in on each cluster wiki page or as summarized under Ratios in bundles, all clusters but Narval have H100 GPUs.  Therefore, when using the GPU script on Narval, the --gpus Slurm option should be changed to request an a100 GPYU instead.  Note that as of May 2026, only Rocky with the ansys/2025R2|2.04 modules have been tested but not the ansys/2025R1|1.02 modules yet.

=== Slurm scripts ===

== Electronics ==

Slurm scripts for using AnsysEDT are provided in this specific page.

= Graphical use =

To run Ansys programs in graphical mode using an OnDemand or JupyterHub desktop, click on one of the following links:

  NIBI: https://ondemand.sharcnet.ca
 FIR: https://jupyterhub.fir.alliancecan.ca
 RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
 Narval:  https://jupyterhub.narval.alliancecan.ca/
 TRILLIUM: https://ondemand.scinet.utoronto.ca

A job submission web page should appear in your browser.  Configure the resources required for your interactive desktop session and click on Launch or Start.  If either accelerated graphics or computations will be conducted from within your desktop session, be sure to specify a GPU resource.  Load an Ansys module on the desktop.  If you started a JuypterLab powered desktop, this can be done by clicking on the left-hand menu, or if you started an OnDemand desktop manually, type module load ansys/version on the command line.  To start one of the common Ansys programs such as Fluent, CFX, Workbench, and so forth, refer to the following section which provides advice for setting environment variables and arguments required by VirtualGL or Mesa-based graphical environments, depending on whether a node with a GPU resource was specified or not.

=== Fluent ===

To start Ansys Fluent from the command line on an OnDemand desktop, open a terminal window and run

::: module load StdEnv/2023 ansys/2025R2.04
::: fluent

When the Fluent Launcher popup selector panel appears, click on the Environment tab and copy/paste the following environment variable settings, depending on whether you started your OnDemand session with a GPU for graphical acceleration. Do not include the text in parentheses as these are comments, and do not put export in front of any variable name.  If the graphics console window becomes corrupted when starting the GUI, restart Fluent setting HOOPS_PICTURE=null to disable the creation of the graphics panel.

Compute node (no GPU requested)

::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on Nibi w/ intelmpi)
::: HOOPS_PICTURE=opengl2-mesa    (version 2025R1 or newer)
::: HOOPS_PICTURE=x11/lin                (version 2024R2.04 or older)
::: Click on the Start button.

Compute node (with GPU requested)

To use hardware accelerated graphics with Fluent on Nibi, choose a t4 (15GB) from the GPU selector pulldown list for your OnDemand desktop session.  Doing this ensures that the environment variables used by VirtualGL to enable accelerated OpenGL graphics calls are automatically set up inside your desktop environment for the current session.  Once your desktop appears, open a terminal window and start Workbench as follows
::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on Nibi)
::: HOOPS_PICTURE=opengl2    (version 2025R1 or newer)
::: HOOPS_PICTURE=opengl                 (version 2024R2.04 or older)
::: Click on the Start button.

NOTE: When running Fluent on Nibi, the environment variable I_MPI_HYDRA_BOOTSTRAP=ssh must be manually set; otherwise, Fluent will crash when started inside OOD Compute Desktop sessions when intelmpi is used.  Error output such as the following will be created.  Should this occur, completely exit Fluent, cleanly shut down Workbench and start over.
 [mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
 [mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
 [mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
 [mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
 [mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

=== CFX ===

When starting CFX from an OnDemand desktop, the following arguments may be specified on the terminal window command line, depending on whether a GPU was requested when the desktop was started.

::: module load StdEnv/2023 ansys/2025R1  (or older)
::: cfx5 -graphics mesa   (no GPU requested)
::: cfx5 -graphics ogl    (with GPU requested)

=== Mapdl ===

The following steps for starting the Mechanical APDL GUI from the command line of a terminal window should work regardless if you have started your OnDemand desktop on a compute node with or without a GPU.

::: module load StdEnv/2023 ansys/2022R2 (or newer versions)
::: mapdl -g, or,
::: launcher then click on the RUN button

=== Workbench ===

This section shows how to start Workbench (and optionally Fluent) on either an OnDemand desktop or a JupyterLab desktop.

==== OnDemand desktop ====

Compute node (no GPU requested) or basic desktop

If accelerated graphics are not required for your desktop session, specify GPU Node to select a compute node without a GPU for your OOD session.  Doing this uses Mesa software emulation for opengl calls, instead of running on a more expensive and difficult to reserve GPU node.
::: module load StdEnv/2023 ansys/2025R2.04
::: runwb2

To start Fluent from within Workbench, click on Fluid Flow (Fluent) or Fluent with Fluent Meshing in the left-hand Analysis menu, and click on Setup in the centre canvas Fluid Flow (Fluent) popup.  Once the Fluent Launcher selector panel popup appears, click on the Environment tab and copy/paste the following environment variable settings:
::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on the Nibi cluster only)
::: HOOPS_PICTURE=opengl2-mesa    (optional for 2025R1 or newer)
::: Click on the Start button.

Compute node (with GPU requested)

If accelerated graphics are required on the Nibi cluster, choose t4 (15GB) from the GPU selector pulldown list for your OnDemand desktop session.  Doing this will ensures that the environment variables used by VirtualGL to enable accelerated OpenGL graphics calls are automatically set up inside your deskop environment for the current session.  Once your desktop appears, open a terminal window and start Workbench as follows
::: module load StdEnv/2023 ansys/2025R2.04
::: runwb2

To start Fluent from within Workbench, click on Fluid Flow (Fluent) or 'Fluent with Fluent Meshing in the left-hand Analysis menu, and click on Setup in the centre canvas Fluid Flow Fluent popup.  Once the Fluent Launcher selector panel popup appears, click on the Environment tab and copy/paste the following environment variable settings.
::: I_MPI_HYDRA_BOOTSTRAP=ssh     (required on the Nibi cluster only)
::: HOOPS_PICTURE=opengl2             (optional for 2025R1 or newer)
::: Click on the Start button.

When using the Nibi cluster, I_MPI_HYDRA_BOOTSTRAP=ssh must be manually set when the default intelmpi is used, otherwise Fluent will crash on startup producing error output such as the following. To recover from this, close Fluent, shut down Workbench, and try again.
 [mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
 [mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
 [mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
 [mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
 [mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

==== Jupyterhub desktop ====

Compute node (no GPU requested)

::: Click to load ansys/2025R1 (or newer version) in the Desktop left hand side menu
::: Click on the Workbench (VNC) icon located in the JupyterLab desktop centre window.
:::: If the graphics of any application (such as Fluent) started within Workbench
:::: appear unusable because they seem corrupted, try carrying out the following
:::: steps.  They will create a custom runwb2 desktop icon so that Workbench
:::: can be started in Mesa mode.  If one of the applications that you will be starting
:::: in Workbench is Fluent, you may also try setting
:::: HOOPS_PICTURE=opengl2-mesa variable in the Fluent Launcher window when the Fluent launcher starts.
:::: HOOPS_PICTURE=opengl2-mesa variable in the Fluent Launcher window.
::: To proceed, exit Workbench and open a terminal window.  Copy/paste the following
::: command into the Remote Clipboard located in the top right corner of your Jupyter desktop.
::: Now the commands can be pasted into the terminal i.e.
::: cd ~/Desktop; cp -p $(realpath workbench.desktop) workbench-mesa.desktop
::: Open the newly created file in a text editor such as nano by doing the following:
::: nano ~/Desktop/workbench-mesa.desktop.  Change all instances of runwb2
::: to  runwb2 -oglmesa and exit the editor, saving the changes.  Now REFRESH
::: the Jupyter desktop by pressing the key combination control-R.  The new icon should now
::: appear in the desktop along with the original Workbench icon. Double-click on it to start Workbench.
::: The new icon will persist for future sessions until manually deleted with the command
::: rm -f ~/Desktop/workbench-mesa.desktop.

Compute node (with GPU requested)

::: Click to load ansys/2025R1 (or newer version) in the Desktop left-hand side menu.
::: Click the Workbench (VNC) icon located in the JupyterLab desktop centre window.

=== Ensight ===
::: module load StdEnv/2023 ansys/2022R2; A=222; B=5.12.6
::: export LD_LIBRARY_PATH=$EBROOTANSYS/v$A/CEI/apex$A/machines/linux_2.6_64/qt-$B/lib
::: ensight -X

=== Rocky ===
::: module load StdEnv/2023 ansys/2025R2.04 (or 2025R1, 2025R1.02, 2025R2)
::: Rocky The Rocky command starts Rocky in standalone GUI mode
::: RockySolver Run the solver directly from the command line (not tested)
::: RockySchedular GUI to interactively submit/run jobs on present node (not tested)
::: o The Ansys module handles reading your ~/licenses/ansys.lic file
::: o The SHARCNET Ansys license includes Rocky and is therefore free to use.

== Electronics ==

Information describing how to run AnsysEDT in graphical mode may be found in this page.

= Site-specific usage =

== SHARCNET license ==

The SHARCNET Ansys license is free for academic use by any Alliance researcher on any Alliance system.   The installed software does not have any solver or geometry limits.  The SHARCNET license may be used for Publishable Academic Research, but not for any private/commercial purposes as this is strictly prohibited by the license terms.  The SHARCNET Ansys license is based on the Multiphysics Campus Solution and includes products such as: HF, EM, Electronics HPC, Mechanical, CFD, ROCKY and LS-DYNA as described here. Lumerical software is included in recent Ansys module versions, however it is NOT covered by the SHARCNET license.  SpaceClaim software is not installed with any Ansys module since there is no Linux version available; it is technically covered by the SHARCNET license however.

 ⚖️ Scaling tests should be run before launching long jobs to determine the optimal scalable job size so that the limited licenses and hardware is used as efficiently as possible, and total job run and startup times are minimized.  Parallel jobs that do not achieve at least 50% CPU utilization will probably be flagged by the system, resulting in a follow up by an Alliance team member.

==== License limits ====

The SHARCNET Ansys license is made available on a first come first serve basis.  It currently permits each researcher to run a maximum of simultaneous 16 jobs using a total of up to 512 HPC cores across all clusters, therefore any of the following maximum job size combinations can be run simultaneously: 1x512, 2x256, 4x128, 8x64, 16x32 or more commonly one of these full node combinations: 1x384, 2x192 or 1x192 cores.  Note however that the SHARCNET license is oversubscribed so there is potential for jobs to fail on startup if all (or nearly all) of the 1986 anshpc licenses in the SHARCNET license pool are in use.  Should this occur, you will need to manually resubmit your job to the queue.   As there have been an increasing number of license shortage (DENIED) instances where jobs fail on startup, the total anshpc core limit per researcher will be decreased from 512 to 384 on April 1, 2026.  If you need to use more than 384 HPC cores for your research, either use the local Ansys License server at your institution if one is available, OR open a ticket to request purchasing additional licenses for the SHARCNET license and these would be reserved for your own or your groups exclusive use.

==== License file ====

As of February 2026, the license3.sharcnet.ca license server has been permanently shut down.  To use the SHARCNET Ansys license on any Alliance cluster, simply configure your ansys.lic file as follows

[username@cluster:~] cat ~/.licenses/ansys.lic
setenv("ANSYSLMD_LICENSE_FILE", "1055@license1.computecanada.ca")

==== License query  ====

To show the number of Ansys licenses in use by your username and the total in use by all users, run

ssh nibi.alliancecan.ca
module load ansys
$EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil \
lmstat -c $ANSYSLMD_LICENSE_FILE -a | grep "Users of\|$USER" | grep -v " Total of 0 licenses in use"

==== Example  ====

Consider the case where a user submits an 8-core Fluent job and 32-core Fluent job.  Once both jobs start running, the user runs the lmutil query command and the output shown below is generated.  Here, we see that a total of (8-4) + (32-4) = 32 anshpc licenses are used by the two jobs.  As a result the total number of licenses increases from 1568 to 1600 so that only (1986-1600) = 386 of them remain available for additional jobs submitted by all users.  Therefore, if a 400-core parallel job attempts to start at that moment, it will fail to start since (400-4) = 396 anshpc licenses would be required. The user has two options, either wait for a sufficient number of   licenses to come available OR reduce the job size to 390 cores or less and resubmit immediately.  This example focuses on the anshpc feature since it is most generously overcommitted to allow any user to submit the largest job possible, but it also shows that the actual number of licenses available per user may sometimes be far less than the 512 per user limit would suggest.

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

 🕵 A rare situation can occur where the output from the license query command reveals there are some Ansys licenses unexpectedly still in use by your username on some desktop or compute node. This would happen if for instance an Ansys GUI program run on a remote desktop node was not shut down cleanly, leaving some Ansys processes still running, or an Ansys program crashes on a cluster compute node inside an salloc session that was being run interactively from the command line, once again leaving some rogue Ansys processes still running.  To kill all potentially responsible Ansys rogue processes, either close the desktop, scancel the salloc session, or simply open a terminal window on the affected node and issue the pkill -9 -e -u $USER -f "ansys" command.  Any Ansys licenses that were being held open should immediately be returned to the SHARCNET license server and become available for use again by yourself or other researchers.

= Additive Manufacturing =

To get started, configure your ~/.licenses/ansys.lic file to point to a license server that has a valid Ansys Mechanical license.  This must be done on all systems where you plan to run the software.

== Enabling Additive ==

This section describes how to make the Ansys Additive Manufacturing ACT extension available for use in your project. The steps must be performed on each cluster for each Ansys module version where the extension will be used. Any extensions needed by your project will also need to be installed on the cluster as described below.  If you get warnings about missing un-needed extensions (such as ANSYSMotion), uninstall them from your project.

=== Downloading extensions ===
* download AdditiveWizard.wbex from https://catalog.ansys.com/,
* upload AdditiveWizard.wbex to the cluster where it will be used.

=== Starting Workbench ===
* follow the Workbench section in Graphical use above,
* File -> Open your project file (ending in .wbpj) into the Workbench GUI.

===  Opening the extensions manager ===
* click on the ACT start page and the ACT home page tab will open,
* click Manage Extensions and the extensions manager will open.

=== Installing extensions ===
* click on the box with the large + sign under the search bar,
* navigate to select and install your AdditiveWizard.wbex file.

=== Loading extensions ===
* click to highlight the AdditiveWizard box (loads the AdditiveWizard extension for the current session only),
* click on the lower right corner arrow in the AdditiveWizard box and select Load extension (loads the extension for current AND future sessions).

=== Unloading extensions ===
* click to un-highlight the AdditiveWizard box (unloads extension for the current session only),
* click on the lower right corner arrow in the AdditiveWizard box and select Do not load as default (extension will not load for future sessions).

== Running Additive ==

=== OnDemand ===

You can run a single Ansys Additive Manufacturing job in a graphical OnDemand session by following these steps:

* Start Workbench as described above in Enabling Additive;
* click on File -> Open, select test.wbpj and click on Open;
* click on View -> reset workspace if you get a grey screen;
* start Mechanical, clear generated data, tick Distributed, specify cores;
* click on File -> Save Project -> Solve.

Check utilization
* open another terminal and run  top -u $USER   **OR**  ps u -u $USER | grep ansys,
* kill rogue processes from previous runs with  pkill -9 -e -u $USER -f "ansys|mwrpcss|mwfwrapper|ENGINE".

Please note that rogue Ansys-related processes can persistently tie up valuable licenses inside a running OnDemand login node session if an Ansys GUI session (Fluent, Workbench, Mechanical, etc.) is not cleanly terminated or is terminated unexpectedly by a network outage or a hung filesystem.  If the latter is to blame, the processes may not by killable until normal disk access is restored.

===Cluster===

Project preparation

Before submitting a newly uploaded Additive project to a cluster queue (with sbatch scriptname), certain preparations must be done.  To begin, open your simulation with the Workbench GUI (as described in the Enabling Additive section above) in the same directory that your job will be submitted from and then save it again. Be sure to use the same Ansys module version that will be used for the job.  Next, create a Slurm script (as explained in the Cluster Batch Job Submission - WORKBENCH section above). To perform parametric studies, change Update() to UpdateAllDesignPoints() in the Slurm script.  Determine the optimal number of cores and memory by submitting several short test jobs.  To avoid needing to manually clear the solution and recreate all the design points in Workbench between each test run, either 1) change Save(Overwrite=True) to Save(Overwrite=False) or 2) save a copy of the original YOURPROJECT.wbpj file and corresponding YOURPROJECT_files directory.  Optionally, create and then manually run a replay file on the cluster in the respective test case directory between each run, noting that a single replay file can be used in different directories by opening it in a text editor and changing the internal FilePath setting.

 module load ansys/2019R3
 rm -f test_files/.lock
 runwb2 -R myreplay.wbjn

Resource utilization

Once your Additive job has been running for a few minutes, a snapshot of its resource utilization on the compute node(s) can be obtained with the srun command.  Sample output corresponding to an eight-core submission script is shown next.  We see that two nodes were selected by the scheduler:

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

Scaling tests'

After a job completes, its wall-clock time can be obtained with seff myjobid.  Using this value, scaling tests can be performed by submitting short test jobs with an increasing number of cores.  If the wall-clock time decreases by ~50% when the number of cores is doubled, additional cores may be considered.

= Help resources =

The official full documentation for recent versions Ansys 202[4|5]R[1|2] is available here.  Documentation for older versions such as Ansys 2023R[1|2] however requires login.  Developer documentation can be found in the Ansys Developer Portal. Additional learning resources include the Ansys HowTo videos, the Ansys Educator Hub and the Ansys Webinar series.

XoverSSH Legacy Note: Some programs can be run remotely on a cluster compute node by forwarding X over SSH to your local desktop.  Unlike VNC, this approach is not tested and not supported since it relies on a properly set up X display server for your particular operating system OR the selection, installation and configuration of a suitable X client emulator package such as MobaXterm.  Most users will find interactive response times unacceptably slow for basic menu tasks, let alone for more complex tasks such as those involving graphics rendering.  Startup times for GUI programs can also be very slow depending on your Internet connection. For example, in one test it took 40 minutes to fully start the GUI over SSH while starting it with vncviewer required only 34 seconds.  Despite the potential slowness, using this method to connect may still be of interest if your only goal is to open a simulation and perform some basic menu operations or run some calculations, and response delays can be tolerated. The basic steps are given here as a starting point: 1) ssh -Y username@alliancecan.ca 2) salloc --x11 --time=1:00:00 --mem=16G --cpus-per-task=4 [--gpus-per-node=1] --account=def-mygroup; 3) once connected onto a compute node, try running xclock.  If the clock appears on your desktop, proceed to load the desired Ansys module and try running the program.