---
title: "GROMACS/en"
url: "https://docs.alliancecan.ca/wiki/GROMACS/en"
category: "General"
last_modified: "2026-07-14T19:38:46Z"
page_id: 4167
display_title: "GROMACS"
---

=General=

GROMACS is a versatile package to perform molecular dynamics for systems with hundreds to millions of particles.
It is primarily designed for biochemical molecules like proteins, lipids and nucleic acids that have a lot of complicated bonded interactions,
but since GROMACS is extremely fast at calculating the nonbonded interactions
(that usually dominate simulations) many groups are also using it for research on non-biological systems, e.g. polymers.

== Strengths ==

* GROMACS provides extremely high performance compared to all other programs.
* Since GROMACS 4.6, we have excellent CUDA-based GPU acceleration on GPUs that have Nvidia compute capability >= 2.0 (e.g. Fermi or later).
* GROMACS comes with a large selection of flexible tools for trajectory analysis.
* GROMACS can be run in parallel, using either the standard MPI communication protocol, or via our own "Thread MPI" library for single-node workstations.
* GROMACS is free software, available under the GNU Lesser General Public License (LGPL), version 2.1.

== Weak points ==

* To get very high simulation speed, GROMACS does not do much additional analysis and / or data collection on the fly. It may be a challenge to obtain somewhat non-standard information about the simulated system from a GROMACS simulation.

* Different versions may have significant differences in simulation methods and default parameters. Reproducing results of older versions with a newer version may not be straightforward.

* Additional tools and utilities that come with GROMACS are not always of the highest quality, may contain bugs and may implement poorly documented methods. Reconfirming the results of such tools with independent methods is always a good idea.

== GPU support ==

The top part of any log file will describe the configuration,
and in particular whether your version has GPU support compiled in.
GROMACS will automatically use any GPUs it finds.

GROMACS uses both CPUs and GPUs; it relies on a reasonable balance between CPU and GPU performance.

The new neighbour structure required the introduction of a new variable called "cutoff-scheme" in the mdp file.
The behaviour of older GROMACS versions (before 4.6) corresponds to cutoff-scheme = group, while in order to use
GPU acceleration you must change it to cutoff-scheme = verlet, which has become the new default in version 5.0.

= Quickstart guide =
This section summarizes configuration details.

== Environment modules ==

The following versions have been installed:

GROMACS version	modules for running on CPUs                         	modules for running on GPUs (CUDA)                             	Notes
gromacs/2025.4 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2025.4	StdEnv/2023 gcc/12.3  openmpi/4.1.5  cuda/12.6  gromacs/2025.4 	GCC, FlexiBLAS & FFTW
gromacs/2024.6 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2024.6	StdEnv/2023 gcc/12.3  openmpi/4.1.5  cuda/12.6  gromacs/2024.6 	GCC, FlexiBLAS & FFTW
gromacs/2024.4 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2024.4	StdEnv/2023 gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs/2024.4 	GCC, FlexiBLAS & FFTW
gromacs/2024.1 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2024.1	StdEnv/2023 gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs/2024.1 	GCC, FlexiBLAS & FFTW
gromacs/2023.5 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2023.5	StdEnv/2023  gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs/2023.5	GCC, FlexiBLAS & FFTW
gromacs/2023.3 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2023.3	StdEnv/2023 gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs/2023.3 	GCC, FlexiBLAS & FFTW

GROMACS version	modules for running on CPUs                          	modules for running on GPUs (CUDA)                              	Notes
gromacs/2023.2 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2023.2	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2023.2	GCC, FlexiBLAS & FFTW
gromacs/2023   	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2023  	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2023  	GCC, FlexiBLAS & FFTW
gromacs/2022.3 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2022.3	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2022.3	GCC, FlexiBLAS & FFTW
gromacs/2022.2 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2022.2	                                                                	GCC, FlexiBLAS & FFTW
gromacs/2021.6 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2021.6	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2021.6	GCC, FlexiBLAS & FFTW
gromacs/2021.4 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2021.4	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2021.4	GCC, FlexiBLAS & FFTW
gromacs/2021.2 	                                                     	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2021.2	GCC, FlexiBLAS & FFTW
gromacs/2021.2 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2021.2	StdEnv/2020  gcc/9.3.0  cuda/11.0  openmpi/4.0.3  gromacs/2021.2	GCC & MKL
gromacs/2020.6 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2020.6	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2020.6	GCC, FlexiBLAS & FFTW
gromacs/2020.4 	                                                     	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2020.4	GCC, FlexiBLAS & FFTW
gromacs/2020.4 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2020.4	StdEnv/2020  gcc/9.3.0  cuda/11.0  openmpi/4.0.3  gromacs/2020.4	GCC & MKL

GROMACS version	modules for running on CPUs                          	modules for running on GPUs (CUDA)                                  	Notes
gromacs/2020.2 	StdEnv/2018.3  gcc/7.3.0 openmpi/3.1.2 gromacs/2020.2	StdEnv/2018.3  gcc/7.3.0 cuda/10.0.130 openmpi/3.1.2  gromacs/2020.2	GCC & MKL
gromacs/2019.6 	StdEnv/2018.3  gcc/7.3.0 openmpi/3.1.2 gromacs/2019.6	StdEnv/2018.3  gcc/7.3.0 cuda/10.0.130 openmpi/3.1.2  gromacs/2019.6	GCC & MKL
gromacs/2019.3 	StdEnv/2018.3  gcc/7.3.0 openmpi/3.1.2 gromacs/2019.3	StdEnv/2018.3  gcc/7.3.0 cuda/10.0.130 openmpi/3.1.2  gromacs/2019.3	GCC & MKL  ‡
gromacs/2018.7 	StdEnv/2018.3  gcc/7.3.0 openmpi/3.1.2 gromacs/2018.7	StdEnv/2018.3  gcc/7.3.0 cuda/10.0.130 openmpi/3.1.2  gromacs/2018.7	GCC & MKL

GROMACS version	modules for running on CPUs                           	modules for running on GPUs (CUDA)                                  	Notes
gromacs/2018.3 	StdEnv/2016.4  gcc/6.4.0 openmpi/2.1.1 gromacs/2018.3 	StdEnv/2016.4  gcc/6.4.0 cuda/9.0.176 openmpi/2.1.1  gromacs/2018.3 	GCC & FFTW
gromacs/2018.2 	StdEnv/2016.4  gcc/6.4.0 openmpi/2.1.1 gromacs/2018.2 	StdEnv/2016.4  gcc/6.4.0 cuda/9.0.176 openmpi/2.1.1  gromacs/2018.2 	GCC & FFTW
gromacs/2018.1 	StdEnv/2016.4  gcc/6.4.0 openmpi/2.1.1 gromacs/2018.1 	StdEnv/2016.4  gcc/6.4.0 cuda/9.0.176 openmpi/2.1.1  gromacs/2018.1 	GCC & FFTW
gromacs/2018   	StdEnv/2016.4  gromacs/2018                           	StdEnv/2016.4  cuda/9.0.176 gromacs/2018                            	Intel & MKL
gromacs/2016.5 	StdEnv/2016.4  gcc/6.4.0  openmpi/2.1.1 gromacs/2016.5	StdEnv/2016.4  gcc/6.4.0  cuda/9.0.176  openmpi/2.1.1 gromacs/2016.5	GCC & FFTW
gromacs/2016.3 	StdEnv/2016.4  gromacs/2016.3                         	StdEnv/2016.4  cuda/8.0.44 gromacs/2016.3                           	Intel & MKL
gromacs/5.1.5  	StdEnv/2016.4  gromacs/5.1.5                          	StdEnv/2016.4  cuda/8.0.44 gromacs/5.1.5                            	Intel & MKL
gromacs/5.1.4  	StdEnv/2016.4  gromacs/5.1.4                          	StdEnv/2016.4  cuda/8.0.44 gromacs/5.1.4                            	Intel & MKL
gromacs/5.0.7  	StdEnv/2016.4  gromacs/5.0.7                          	StdEnv/2016.4  cuda/8.0.44 gromacs/5.0.7                            	Intel & MKL
gromacs/4.6.7  	StdEnv/2016.4  gromacs/4.6.7                          	StdEnv/2016.4  cuda/8.0.44 gromacs/4.6.7                            	Intel & MKL
gromacs/4.6.7  	StdEnv/2016.4  gcc/5.4.0  openmpi/2.1.1 gromacs/4.6.7 	StdEnv/2016.4  gcc/5.4.0  cuda/8.0  openmpi/2.1.1  gromacs/4.6.7    	GCC & MKL & ThreadMPI

Notes:
*  GROMACS versions 2020.0 up to and including 2021.5 contain a bug when used on GPUs of Volta or newer generations (i.e. V100, T4, A100, and H100) with mdrun option -update gpu that could have perturbed the virial calculation and, in turn, led to incorrect pressure coupling. The GROMACS developers state in the 2021.6 Release Notes:"Fix missing synchronization in CUDA update kernels" in GROMACS 2021.6 Release Notes  The GPU update is not enabled by default, so the error can only appear in simulations where it [the -update gpu option] was manually selected, and even in this case the error might be rare since we have not observed it in practice in the testing we have performed. Further discussion of this bug can be found in the GitLab issue #4393 of the GROMACS project.Issue #4393 in GROMACS Project on GitLab.com
* Version 2020.4 and newer have been compiled for the new Standard software environment StdEnv/2020.
* Version 2018.7 and newer have been compiled with GCC compilers and the MKL-library, as they run a bit faster.
* Older versions have been compiled with either GCC compilers and FFTW or Intel compilers, using Intel MKL and Open MPI 2.1.1 libraries from the default environment as indicated in the table above.
* CPU (non-GPU) versions are available in both single- and double precision, with the exception of 2019.3 (‡), where double precision is not available for AVX512.

These modules can be loaded by using a module load command with the modules as stated in the second column in the above table.
For example:

 $ module load  StdEnv/2023  gcc/12.3   openmpi/4.1.5  gromacs/2025.4
 or
 $ module load  StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs/2023.2

These versions are also available with GPU support, albeit only with single precision. In order to load the GPU enabled version, the cuda module needs to be loaded first. The modules needed are listed in the third column of above table, e.g.:

 $ module load  StdEnv/2023  gcc/12.3  openmpi/4.1.5  cuda/12.6  gromacs/2025.4
 or
 $ module load  StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs/2023.2

For more information on environment modules, please refer to the Using modules page.

== Suffixes ==

=== GROMACS 5.x, 2016.x and newer ===
GROMACS 5 and newer releases consist of only four binaries that contain the full functionality.
All GROMACS tools from previous versions have been implemented as sub-commands of the gmx binaries.
Please refer to GROMACS 5.0 Tool Changes and the GROMACS documentation manuals for your version.

:* gmx       - mixed ("single") precision GROMACS with OpenMP (threading) but without MPI.
:* gmx_mpi   - mixed ("single") precision GROMACS with OpenMP and MPI.
:* gmx_d     - double precision GROMACS with OpenMP but without MPI.
:* gmx_mpi_d - double precision GROMACS with OpenMP and MPI.

=== GROMACS 4.6.7 ===
* The double precision binaries have the suffix _d.
* The parallel single and double precision mdrun binaries are:

:* mdrun_mpi
:* mdrun_mpi_d

== Submission scripts ==
Please refer to the page Running jobs for help on using the SLURM workload manager.

=== Serial jobs ===
Here's a simple job script for serial mdrun:

This will run the simulation of the molecular system in the file em.tpr.

=== Whole nodes ===
Commonly, the systems simulated with GROMACS are so large that you should use a number of whole nodes for the simulation.

Generally, the product of --ntasks-per-node and --cpus-per-task should match the number of CPU cores of the
cluster’s compute nodes. See section Performance and benchmarking below.

On clusters with a large number of CPU cores (e.g. 192) per compute node, domain decomposition can become a limiting factor when choosing --ntasks-per-node. The larger a system is, the more it can be divided into smaller regions, allowing larger --ntasks-per-node values. If GROMACS reports an error about domain decomposition being impossible given the system size and requested number of domains, halve --ntasks-per-node and double --cpus-per-task.

=== GPU job ===

Please read Using GPUs with Slurm for general information on using GPUs on our systems.

This is a job script for mdrun using 4 OpenMP threads and one GPU:

==== Notes on running GROMACS on GPUs ====

Note that using more than a single GPU usually leads to poor efficiency. Carefully test and compare multi-GPU and single-GPU performance before deciding to use more than one GPU for your simulations.

*  GROMACS versions 2020.0 up to and including 2021.5 contain a bug when used on GPUs of Volta or newer generations (i.e. V100, T4 and A100) with mdrun option -update gpu that could have perturbed the virial calculation and, in turn, led to incorrect pressure coupling. The GROMACS developers state in the 2021.6 Release Notes:"Fix missing synchronization in CUDA update kernels" in GROMACS 2021.6 Release Notes  The GPU update is not enabled by default, so the error can only appear in simulations where it was manually selected, and even in this case the error might be rare since we have not observed it in practice in the testing we have performed. Further discussion of this bug can be found in the GitLab issue #4393 of the GROMACS project.Issue #4393 in GROMACS Project on GitLab.com
* Our clusters have differently configured GPU nodes.On the page Using GPUs with Slurm#Available GPUs you can find more information about the different node configurations (GPU models and number of GPUs and CPUs per node).
* GROMACS imposes a number of constraints for choosing the number of GPUs, tasks (MPI ranks) and OpenMP threads.For GROMACS 2018.2 the constraints are:
::* The number of --tasks-per-node always needs to be the same as, or a multiple of the number of GPUs (--gpus-per-node).
::* GROMACS will not run GPU runs with only 1 OpenMP thread unless forced by setting the -ntomp option.According to GROMACS developers, the optimum number of --cpus-per-task is between 2 and 6.
* Avoid using a larger fraction of CPUs and memory than the fraction of GPUs you have requested in a node.

You can explore some benchmark results on our MDBench portal.

==== Running multiple simulations on a GPU ====

GROMACS and other MD simulation programs are unable to fully use recent GPU models such as the Nvidia A100 and H100 unless the molecular system is very large (millions of atoms). Running a typical simulation on such a GPU wastes a significant fraction of the allocated computational resources.

There are two recommended solutions to this problem. The first one is to run multiple simulations on a single GPU using mdrun -multidir as described below. This is the preferred solution if you run multiple similar simulations, for instance:

* Repeating the same simulation to acquire more conformational space sampling
* Simulating multiple protein variants, multiple small ligands in complex with the same protein, multiple temperatures or ionic concentrations, etc.
* Ensemble-based simulations such as replica exchange

Similar simulations are needed to ensure proper load balancing. If the simulations are dissimilar, some will progress faster and finish earlier than others, leading to idle resources.

The following job script runs three similar simulations in separate directories (sim1, sim2, sim3) using a single GPU. If you change the number of simulations, make sure to adjust --ntasks-per-node and --cpus-per-task: there should be one task per simulation, while the total number of CPU cores should remain constant.

The second solution is to use a  MIG instance (a fraction of a GPU) rather than a full GPU. This is the preferred solution if you have a single simulation or if your simulations are dissimilar, for instance:

* Systems with different sizes (more than a 10 % difference in the numbers of atoms)
* Systems with different shapes or compositions, such as a membrane-bound versus a soluble protein

 Note that Hyper-Q / MPS should never be used with GROMACS. The built-in -multidir option achieves the same functionality more efficiently.

= Usage =

More content for this section will be added at a later time.

== System preparation ==
In order to run a simulation, one needs to create a tpr file (portable binary run input file). This file contains the starting structure of the simulation, the molecular topology and all the simulation parameters.

Tpr  files are created with the gmx grompp command (or simply grompp for versions older than 5.0). Therefore one needs the following files:
* The coordinate file with the starting structure. GROMACS can read the starting structure from various file formats, such as .gro, .pdb or .cpt (checkpoint).
* The system topology (.top) file. It defines which force field is used and how the force field parameters are applied to the simulated system. Often the topologies for individual parts of the simulated system (e.g. molecules) are placed in separate .itp files and included in the .top file using a #include directive.
*  The run parameter (.mdp) file.  See the GROMACS user guide for a detailed description of the options.

Tpr files are portable, that is they can be grompp'ed on one machine, copied over to a different machine and used as an input file for mdrun.  One should always use the same version for both grompp and mdrun.  Although mdrun is able to use tpr files that have been created with an older version of grompp, this can lead to unexpected simulation results.

== Running simulations ==

MD Simulations often take much longer than the maximum walltime for a job
to complete and therefore need to be restarted.
To minimize the time a job needs to wait before it starts, you should maximize
the number of nodes you have access to
by choosing a shorter running time for your job.  Requesting a walltime of
24 hours or 72 hours (three days) is often a good trade-off between waiting time
and running time.

You should use the mdrun parameter -maxh to tell
the program the requested walltime so that it gracefully finishes the
current timestep when reaching 99% of this walltime.
This causes mdrun to create a new checkpoint file at this
final timestep and gives it the chance to properly close all output files
(trajectories, energy- and log-files, etc.).

For example use #SBATCH --time=24:00 along with gmx mdrun -maxh 24 ...
or  #SBATCH --time=3-00:00 along with gmx mdrun -maxh 72 ....

=== Restarting simulations ===

You can restart a simulation by using the same mdrun
command as the original simulation and adding the -cpi state.cpt
parameter where state.cpt is the filename of the most recent
checkpoint file.  Mdrun will by default (since version 4.5) try to append
to the existing files (trajectories, energy- and log-files, etc.).
GROMACS will check the consistency of the output files and - if needed -
discard timesteps that are newer than that of the checkpoint file.

Using the -maxh parameter ensures that the checkpoint and output
files are written in a consistent state when the simulation reaches the time
limit.

The GROMACS manual contains more detailed information
GROMACS User Guide: Managing long simulations.
GROMACS Manual page: gmx mdrun.

=== Checkpointing simulations ===

You can use GROMACS’ ability to restart a simulation to split a long simulation over multiple short jobs. Shorter jobs wait less in the queue. In particular, those that request 3 hours or less are eligible for backfill scheduling. (See our  job scheduling policies.) This is especially useful if your research group has only a default resource allocation (e.g. def-sponsor) on the cluster, but will benefit even those with competitive resource allocations (e.g. rrg-sponsor).

By using a  job array, you can automate checkpointing. With an array job script such as the following, a single sbatch call submits multiple short jobs, but only the first one is eligible to start. As soon as this first job has completed, the next one becomes eligible to start and resume your simulation. This process repeats until all jobs are complete or the simulation is finished, at which point any remaining pending jobs are automatically cancelled.

= Performance and benchmarking =

A team at ACENET has created a Molecular Dynamics Performance Guide for Alliance clusters.
It can help you determine optimal conditions for AMBER, GROMACS, NAMD, and OpenMM jobs. The present section focuses on GROMACS performance.

Getting the best mdrun performance with GROMACS is not a straightforward
task. The GROMACS developers are maintaining a long section in their user-guide
dedicated to mdrun-performanceGROMACS User-Guide: Getting good performance from mdrun
which explains all relevant options/parameters and strategies.

There is no "One size fits all", but the best parameters to choose highly
depend on the size of the system (number of particles as well as size and
shape of the simulation box) and the simulation parameters (cutoffs, use of
Particle-Mesh-Ewald GROMACS User-Guide:  Performance background information
(PME) method for long-range electrostatics).

GROMACS prints performance information and statistics at the end of the
md.log file, which is helpful in identifying bottlenecks.
This section often contains notes on how to further improve the performance.

The simulation performance is typically quantified by the number of
nanoseconds of MD-trajectory that can be simulated within a day (ns/day).

Parallel scaling is a measure of how effectively the compute resources
are used.  It is defined as:

: S = pN / ( N * p1 )

Where pN is the performance using N CPU cores.

Ideally, the performance increases linearly with the number of CPU cores
("linear scaling"; S = 1).

== MPI processes / Slurm tasks / Domain decomposition ==

To set the number of MPI processes (called MPI-ranks in the GROMACS
documentation), use one of the --ntasks or
--ntasks-per-node Slurm options in your job script.

GROMACS uses Domain Decomposition (DD)
to distribute the work of solving the non-bonded Particle-Particle (PP)
interactions across multiple CPU cores. This is done by effectively cutting
the simulation box along the X, Y and/or Z axes into domains and assigning
each domain to one MPI process.

This works well until the time needed for communication becomes large with
respect to the size (number of particles and volume)
of the domain. In that case the parallel scaling will drop significantly
below 1 and in extreme cases the performance drops when increasing the
number of domains.

GROMACS can use Dynamic Load Balancing to shift the boundaries between
domains to some extent, in order to avoid certain domains taking significantly
longer to solve than others.  The mdrun parameter
-dlb auto is the default.

Domains cannot be smaller in any direction than the longest cutoff radius.

=== Long-range interactions with PME ===

The Particle-Mesh-Ewald method (PME) is often used to calculate the long-range
non-bonded interactions (interactions beyond the cutoff radius).  As PME
requires global communication, the performance can degrade quickly when
many MPI processes are involved that are calculating both the short-range
(PP) as well as the long-range (PME) interactions.  This is avoided by having
dedicated MPI processes that only perform PME (PME-ranks).

GROMACS mdrun by default uses heuristics to dedicate a number of MPI
processes to PME when the total number of MPI processes is 12 or greater.
The mdrun parameter -npme can be used to select the number of
PME ranks manually.

In case there is a significant "Load Imbalance" between the PP and PME ranks
(e.g. the PP ranks have more work per timestep than the PME ranks), one can
shift work from the PP ranks to the PME ranks by increasing the cutoff radius.
This will not affect the result, as the sum of short-range + long-range forces
(or energies) will be the same for a given timestep.  Mdrun will attempt to
do that automatically since version 4.6 unless the mdrun parameter
-notunepme is used.

Since version 2018, PME can be offloaded to the GPU (see below)
however the implementation as of version 2018.1 still has several limitations
GROMACS User-Guide: GPU accelerated calculation of PME among them that only
a single GPU rank can be dedicated to PME.

== OpenMP threads / CPUs-per-task ==

Once Domain Decomposition with MPI processes reaches the scaling limit
(parallel scaling starts dropping), performance can be further improved by
using OpenMP threads to spread the work of an MPI process (rank) over more
than one CPU core.  To use OpenMP threads, use Slurm's --cpus-per-task
parameter in the job script (both for #SBATCH> and srun)
and either set the OMP_NUM_THREADS variable with:
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}" (recommended)
or the mdrun parameter -ntomp ${SLURM_CPUS_PER_TASK:-1}.

According to GROMACS developers, the optimum is usually between 2 and 6 OpenMP threads
per MPI process (cpus-per-task).  However for jobs running on a very large
number of nodes it might be worth trying an even larger number of cpus-per-task.

Especially for systems that don't use PME, we don't have to worry about a
"PP-PME Load Imbalance".  In those cases we can choose 2 or 4 ntasks-per-node
and set cpus-per-task to a value that ntasks-per-node * cpus-per-task
matches the number of CPU cores in a compute node.

== CPU architecture ==

GROMACS uses optimized kernel functions to compute the real-space portion of short-range, non-bonded interactions. Kernel functions are available for a variety of SIMD instruction sets, such as AVX, AVX2, and AVX512. Kernel functions are chosen when compiling GROMACS, and should match the capabilities of the CPUs that will be used to run the simulations. This is done for you by our team: when you load a GROMACS module into your environment, an appropriate AVX/AVX2/AVX512 version is chosen depending on the architecture of the cluster. GROMACS reports what SIMD instruction set it supports in its log file, and will warn you if the selected kernel function is suboptimal.

== GPUs ==

Tips on how to use GPUs efficiently will be added soon.

= Analyzing results =

== GROMACS tools ==

GROMACS contains a large number of tools that can be used for common tasks of post-processing and analysis.
The GROMACS manual contains a list of available commands organized by topic as well as organized by name that give a short description and link to the corresponding command reference.

These commands will typically read the trajectory (in the XTC, TNG or TRR format) as well as a coordinate file (GRO, PDB, TPR, etc.) and write plots in the XVG format which can be used for inputs for the plotting tool Grace (command xmgrace; Grace User Guide). As XVG files are simple text files, they can also be processed with scripts or imported into other spreadsheet programs.

== VMD ==
VMD is a molecular visualization program for displaying, animating, and analyzing large biomolecular systems using 3-D graphics and built-in scripting.  It can be used to visually inspect GROMACS trajectories and also offers a large number of built-in and external plugins for analysis.
It can also be used in command line mode.

== Using Python ==

MDAnalysis and MDTraj are two Python packages that we provide as precompiled Python wheels. They can read and write trajectory and coordinate files of GROMACS (TRR and XTC) and many other MD packages and also include a variety of commonly used analysis functions.  MDAnalysis can also read topology information from GROMACS TPR files, though often not those created by the latest versions of GROMACS.

Both packages feature a versatile atom-selection language and expose the coordinates of the trajectories, which makes it very easy to write custom analysis tools that can be tailored to a specific problem and integrate well with Python's data-science packages like NumPy, SciPy and Pandas, as well as plotting libraries like Matplotlib/Pyplot and Seaborn.

= Related modules =

== GROMACS-Plumed ==
PLUMEDPLUMED Home is an open source library for free energy calculations in molecular systems which works together with some of the most popular molecular dynamics engines.

The gromacs-plumed modules are versions of GROMACS that have been patched with PLUMED's modifications  so that they can run meta-dynamics simulations.

Also note that gromacs modules version 2025 and newer have native PLUMED support enabled, which can be used after loading any plumed module.

GROMACS	PLUMED	modules for running on CPUs                                	modules for running on GPUs (CUDA)                                    	Notes
v2023.5	v2.9.2	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs-plumed/2023.5	StdEnv/2023  gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs-plumed/2023.5	GCC, FlexiBLAS & FFTW
v2020.7	v2.8.5	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs-plumed/2020.7	StdEnv/2023  gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs-plumed/2020.7	GCC, FlexiBLAS & FFTW

GROMACS	PLUMED	modules for running on CPUs                                 	modules for running on GPUs (CUDA)                                     	Notes
v2022.6	v2.8.3	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-plumed/2022.6	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs-plumed/2022.6	GCC, FlexiBLAS & FFTW
v2022.3	v2.8.1	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-plumed/2022.3	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs-plumed/2022.3	GCC, FlexiBLAS & FFTW
v2021.6	v2.7.4	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-plumed/2021.6	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs-plumed/2021.6	GCC, FlexiBLAS & FFTW
v2021.4	v2.7.3	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-plumed/2021.4	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs-plumed/2021.4	GCC, FlexiBLAS & FFTW
v2021.2	v2.7.1	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-plumed/2021.2	StdEnv/2020  gcc/9.3.0  cuda/11.0  openmpi/4.0.3  gromacs-plumed/2021.2	GCC & MKL
v2019.6	v2.6.2	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-plumed/2019.6	StdEnv/2020  gcc/9.3.0  cuda/11.0  openmpi/4.0.3  gromacs-plumed/2019.6	GCC & MKL

GROMACS	PLUMED	modules for running on CPUs                                      	modules for running on GPUs (CUDA)                                            	Notes
v2019.6	v2.5.4	StdEnv/2018.3  gcc/7.3.0  openmpi/3.1.2  gromacs-plumed/2019.6   	StdEnv/2018.3  gcc/7.3.0  cuda/10.0.130  openmpi/3.1.2 gromacs-plumed/2019.6  	GCC & MKL
v2019.5	v2.5.3	StdEnv/2018.3  gcc/7.3.0  openmpi/3.1.2  gromacs-plumed/2019.5   	StdEnv/2018.3  gcc/7.3.0  cuda/10.0.130  openmpi/3.1.2 gromacs-plumed/2019.5  	GCC & MKL
v2018.1	v2.4.2	StdEnv/2016.4  gcc/6.4.0  openmpi/2.1.1  gromacs-plumed/2018.1   	StdEnv/2016.4  gcc/6.4.0  cuda/9.0.176  openmpi/2.1.1 gromacs-plumed/2018.1   	GCC & FFTW
v2016.3	v2.3.2	StdEnv/2016.4  intel/2016.4  openmpi/2.1.1  gromacs-plumed/2016.3	StdEnv/2016.4  intel/2016.4  cuda/8.0.44  openmpi/2.1.1  gromacs-plumed/2016.3	Intel & MKL

== GROMACS-Colvars ==
ColvarsColvars Home is a software module for molecular simulation programs, which
adds additional capabilities of collective variables to apply biasing potentials, calculate potentials-of-mean-force (PMFs)
along any set of variables, use enhanced sampling methods, such as Adaptive Biasing Force (ABF), metadynamics, steered MD and umbrella sampling.

As of GROMACS v2024GROMACS 2024 Major Release Highlights,
the Colvars library has been added to the official GROMACS releases and can be used without the need of a patched version.

Documentation on how to use Colvars with GROMACS:
* Collective Variable simulations with the Colvars moduleCollective Variable simulations with the Colvars module (GROMACS Reference manual) in the GROMACS Reference manual,
* Molecular dynamics parameters (.mdp options) for the Colvars moduleColvars .mdp Options (GROMACS User guide),
* the Colvars Reference manual for GROMACSColvars Reference manual for GROMACS,
* the publication: Fiorin et al. 2013, Using collective variables to drive molecular dynamics simulations.Fiorin et al. 2013, Using collective variables to drive molecular dynamics simulations.

GROMACS versions prior to v2024 required that they have been patched with Colvars modifications, so that
the collective variables can be used in simulations.
The gromacs-colvars/2020.6 module is such a modified version of GROMACS that includes Colvars 2021-12-20.

GROMACS	Colvars   	modules for running on CPUs                                  	modules for running on GPUs (CUDA)                                      	Notes
v2020.6	2021-12-20	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-colvars/2020.6	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs-colvars/2020.6	GCC, FlexiBLAS & FFTW

== GROMACS-CP2K ==
CP2KCP2K Home is a quantum chemistry and solid-state physics software package.
Since version 2022 GROMACS can be compiled with CP2K-supportBuilding GROMACS with CP2K  QM/MM support to enable Hybrid Quantum-Classical simulations (QM/MM)QM/MM with CP2K in the GROMACS Reference manual.

The gromacs-cp2k modules are versions of GROMACS that have been compiled with CP2K QM/MM support.

Different from other GROMACS modules, these modules are only available for CPU calculations and not for GPUs (CUDA).
Also the modules contain only MPI-enabled executables:

* gmx_mpi   - mixed precision GROMACS with OpenMP and MPI.
* gmx_mpi_d - double precision GROMACS with OpenMP and MPI.

GROMACS	CP2K	modules for running on CPUs                               	Notes
v2022.2	9.1 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-cp2k/2022.2	GCC, FlexiBLAS & FFTW

Here are links to various resources for running QM/MM simulations with this combination of GROMACS and CP2K:

* Hybrid Quantum-Classical simulations (QM/MM) with CP2K interface in the GROMACS manual.
* CP2K QM/MM Best Practices Guide by BioExcel.
* QM/MM with GROMACS + CP2K Workshop material from BioExcel.This contains tutorial material for setting up and running QM/MM simulations as well as links to YouTube videos with theory lectures.  This material was written to be used with HPC resources from the European Centre of Excellence for Computational Biomolecular Research (BioExcel), however only small adjustments are needed to use our HPC systems instead.Most notably, the command gmx_cp2k needs to be replaced with either gmx_mpi (mixed precision) or gmx_mpi_d (double precision). The job scripts, which also use Slurm, need to be adjusted as well.
:* GitHub Repository with example file for BioExcel Tutorial.
* GROMACS-CP2K integration on CP2K homepage.

== GROMACS-LS ==
GROMACS-LSGROMACS-LS and MDStress library and the MDStress library enable the calculation of local stress fields from molecular dynamics simulations.
The MDStress library is included in the GROMACS-LS module.

Please refer to the manual for GROMACS-LS at: Local_stress.pdf and the publications listed therein for information about the method and how to use it.

Invoking commands like gmx_LS mdrun -rerun or gmx_LS trjconv needs a .tpr file.
If you want to analyze a trajectory that has been simulated with a newer version of GROMACS (e.g. 2024), then an older version cannot read that .tpr file because new options are added to the format specification with every major release (2018, 2019 ... 2024).
But as the answer to Q14 in the Local_stress.pdf document suggests, you can use gmx_LS grompp or gmx grompp from the 2016.6 version (which is available as well) to create a new .tpr file using the same input files (*.mdp, topol.top, *.itp, *.gro, etc.) which were used to make the .tpr file for the simulation.
This new .tpr is then compatible with GROMACS-LS 2016.3.
In case the *.mdp files used any keywords or features that were not yet present in 2016 (e.g. pcouple = C-rescale), then you need to either change or remove it (e.g. change to pcouple = Berendsen).
In the case of pcouple, the result will not differ anyway, because the trajectory is processed as with the -rerun option and pressure coupling will not happen in that case.
The mentioning of cutoff-scheme = group in the answer to Q14 can be ignored, because GROMACS 2016 already supports "cutoff-scheme = Verlet" and the "group" scheme was removed for GROMACS 2020.
Therefore GROMACS-LS 2016.3 can be used to process simulations that used either cutoff scheme.

Notes:

* Because the manual was written for the older GROMACS-LS v4.5.5 while core GROMACS commands have changed in version 5, you need to use commands like gmx_LS mdrun and gmx_LS trjconv instead of mdrun_LS and trjconv_LS.
* GROMACS-LS must be compiled in double precision, and does not support MPI, SIMD hardware acceleration or GPUs and is therefore much slower than normal GROMACS. It can only use a single CPU core.
* Unlike other patched versions of GROMACS, the modules gromacs-ls/2016.3 and gromacs/2016.6 can be loaded at the same time.

module           	modules for running on CPUs                         	Notes
gromacs-ls/2016.3	StdEnv/2023  gcc/12.3  gromacs-ls/2016.3            	GROMACS-LS is a serial application and does not support MPI, OpenMP or GPUs/CUDA.
gromacs/2016.6   	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs/2016.6	This GROMACS module can be used to prepare TPR input files for GROMACS-LS.

== GROMACS-RAMD ==
GROMACS-RAMD is a fork of GROMACS that implements the Random Acceleration Molecular Dynamics (RAMD) method.Information on the RAMD method
This method can be used to identify ligand exit routes from the buried binding pockets of receptors and investigate the mechanism of ligand dissociation
by running molecular dynamics simulations with an additional randomly oriented force applied to a molecule in the system.

Information on RAMD-specific MDP optionsRAMD-specific MDP options
can be found on the GROMACS-RAMD GitHub page.

GROMACS	RAMD	modules for running on CPUs                                        	modules for running on GPUs (CUDA)                                            	Notes
v2024.1	2.1 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs-ramd/2024.1-RAMD-2.1 	StdEnv/2023  gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs-ramd/2024.1-RAMD-2.1 	GCC, FlexiBLAS & FFTW
v2020.5	2.0 	StdEnv/2020  gcc/9.3.0  openmpi/4.0.3  gromacs-ramd/2020.5-RAMD-2.0	StdEnv/2020  gcc/9.3.0  cuda/11.4  openmpi/4.0.3  gromacs-ramd/2020.5-RAMD-2.0	GCC, FlexiBLAS & FFTW

== GROMACS-SWAXS ==
GROMACS-SWAXSGROMACS-SWAXS Home
is a modified version of GROMACS for computing small- and wide-angle X-ray or neutron scattering curves (SAXS/SANS)
and for doing SAXS/SANS-driven molecular dynamics simulations.

Please refer to the GROMACS-SWAXS Documentation for
a description of the features (mdrun input and output options, mdp options, use of gmx genscatt
and gmx genenv commands) that have been added in addition to normal GROMACS features,
and for a number of tutorials.

GROMACS	SWAXS	modules for running on CPUs                                     	modules for running on GPUs (CUDA)                                         	Notes
v2021.7	0.5.1	StdEnv/2023  gcc/12.3  openmpi/4.1.5  gromacs-swaxs/2021.7-0.5.1	StdEnv/2023  gcc/12.3  openmpi/4.1.5  cuda/12.2  gromacs-swaxs/2021.7-0.5.1	GCC, FlexiBLAS & FFTW

== G_MMPBSA ==

G_MMPBSAG_MMPBSA Homepage is a tool that calculates components of binding energy using MM-PBSA method except the entropic term and energetic contribution of each residue to the binding using energy decomposition scheme.

Development of that tool seems to have stalled in April 2016 and no changes have been made since then.  Therefore it is only compatible with GROMACS 5.1.x.
For newer version of GROMACS consider using gmx_MMPBSA instead (see below).

The version installed can be loaded with module load  StdEnv/2016.4  gcc/5.4.0  g_mmpbsa/2016-04-19 which is the most up-to-date version and consists of version 1.6 plus the change to make it compatible with GROMACS 5.1.x.  The installed version has been compiled with gromacs/5.1.5 and apbs/1.3.

Please be aware that G_MMPBSA uses implicit solvents and there have been studiesComparison of Implicit and Explicit Solvent Models for the Calculation of Solvation Free Energy in Organic Solvents that conclude that there are issues with the accuracy of these methods for calculating binding free energies.

== gmx_MMPBSA ==

gmx_MMPBSAgmx_MMPBSA Homepage
is a tool based on AMBER's MMPBSA.py aiming to perform end-state free energy calculations with GROMACS files.

Other than the older G_MMPBSA, which is only compatible with older versions of GROMACS,
gmx_MMPBSA can be used with current versions of GROMACS and AmberTools.

Please be aware that gmx_MMPBSA uses implicit solvents and there have been studies that conclude that there are issues with the accuracy of these methods for calculating binding free energies.

=== Submission scripts ===
This submission script installs and executes gmx_MMPBSA in a temporary directory on the local disk of a compute node. All MPI tasks must be on one node. For multi-node submission install a virtual environment on a shared filesystem.

=== Installing gmx_MMPBSA into a virtualenv ===
gmx_MMPBSA needs to be installed in a permanent directory if you intend to use interactive visualization.

==== Installing for gromacs/2024 (StdEnv/2023) ====

1.6.3
}}

Testing.

==== Installing for gromacs/2021 (StdEnv/2020) ====

1. Load required modules and create the virtualenv
1.22.2 seaborn0.13.1 gmx_MMPBSA1.5.0.3 ParmEd3.4.4
}}

2. The Qt/PyQt module needs to be loaded after the virtualenv is ready:

3. Test if the main application works:

Fortunately, running the self-test is very quick, therefore it's permissible to run it on the login node.

Later when using gmx_MMPBSA in a job you need to load the modules and activate the virtualenv as follows:

= Links =
Biomolecular simulation

* Project resources
** Main Website: http://www.gromacs.org/
** Documentation & GROMACS Manuals: http://manual.gromacs.org/documentation/
** GROMACS Community Forums: https://gromacs.bioexcel.eu/ The forums are the successors to the GROMACS email lists.
* Tutorials
** Set of 7 very good Tutorials: http://www.mdtutorials.com/gmx/
** Link collection to more tutorials: http://www.gromacs.org/Documentation/Tutorials
* External resources
**Tool to generate small molecule topology files: http://www.ccpn.ac.uk/v2-software/software/ACPYPE-folder
** Database with Force Field topologies (CGenFF, GAFF and OPLS/AA) for small molecules: http://www.virtualchemistry.org/
** Web service to generate small molecule topologies for GROMOS force fields: https://atb.uq.edu.au/
** Discussion of best GPU configurations for running GROMACS: Best bang for your buck: GPU nodes for GROMACS biomolecular simulations

= References =