---
title: "Cluster batch job submission with Ansys/en"
url: "https://docs.alliancecan.ca/wiki/Cluster_batch_job_submission_with_Ansys/en"
category: "General"
last_modified: "2026-08-14T18:24:46Z"
page_id: 34366
display_title: "Cluster batch job submission with Ansys"
---

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