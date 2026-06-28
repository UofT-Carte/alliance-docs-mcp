---
title: "AMS/en"
url: "https://docs.alliancecan.ca/wiki/AMS/en"
category: "General"
last_modified: "2026-06-23T14:16:55Z"
page_id: 15810
display_title: "AMS"
---

==Introduction==
AMS (Amsterdam Modeling Suite), originally named ADF (Amsterdam Density Functional), is the SCM Software for Chemistry and Materials. AMS offers powerful computational chemistry tools for many research areas such as homogeneous and heterogeneous catalysis, inorganic chemistry, heavy element chemistry, various types of spectroscopy, and biochemistry.

The full SCM module products are available:
*ADF
*ADF-GUI
*BAND
*BAND-GUI
*DFTB
*ReaxFF
*COSMO-RS
*QE-GUI
*NBO6

==Running AMS on Nibi==
The ams module is installed on Nibi. The license is an Academic Computing Center license owned by SHARCNET. You may not use the Software for consulting services nor for purposes that have a commercial nature. To check what versions are available, use the module spider command as follows:

 [name@server $] module spider ams

For module commands, please see Using modules.

===Job submission===

The clusters use the Slurm scheduler; for details about submitting jobs, see Running jobs.

====Example scripts for an AMS job ====
This H2O_adf.sh example script is to request 32 CPUs on one node.  Please use a reasonable number of CPUs instead of simply running a full-node job on Nibi, unless you have demonstrated that your job can scale efficiently to 192 CPUs.

This is the input file used in the script:

====Example scripts for a band job====

===Notes===
# The input for AMS is different from ADF, the previous ADF input file will not run for the new AMS. Some examples can be found in /opt/software/ams/2025.102/examples/
# Except the output .log file, other files are all saved in a subdirectory AMS_JOBNAME.results. If AMS_JOBNAME is not defined in the input .run file, the default name is ams.results
# The restart file name is ams.rkf instead of the TAPE13 in previous ADF versions
For more usage information, please check the manuals in SCM Support

==Running AMS-GUI on Nibi==

AMS can be run graphically on Nibi using an OnDemand Compute Node Desktop as follows:

# Log into ondemand.sharcnet.ca
# Select Compute Node then Compute Desktop from the top menu pulldown
# Specify Computers=1, Cores=1, GPU=None for visualization then press Launch
# Once the Desktop changes from Queued to Running press Launch Nibi Desktop
# When your Desktop starts click Applications -> System Tools -> MATE Terminal
# module unload openmpi
# module load ams,  (loads the latest version)
# export SCM_OPENGL_SOFTWARE=1 (enables software rendering)
: 9a. amsinput or amsview

If you specified GPU=t4 (15GB) when starting your OnDemand Nibi Desktop then instead do :

: 9b. LD_PRELOAD= amsinput or LD_PRELOAD= amsview

☞ To select one or more atoms in the gui press SHIFT then click.