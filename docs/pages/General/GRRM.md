---
title: "GRRM/en"
url: "https://docs.alliancecan.ca/wiki/GRRM/en"
category: "General"
last_modified: "2026-10-23T15:00:36Z"
page_id: 34997
display_title: "GRRM"
---

Global Reaction Route Mapping (GRRM) is commercial software for the analysis of chemical reaction pathways.
The program is capable of exhaustively exploring the potential energy surface of a collection of atoms, automatically finding molecular geometries of reactants, transition states and products.
GRRM23 works in conjunction with quantum chemistry software such as Gaussian 16 and ORCA.

== License ==
To obtain a license and pricing, submit a request at HPC SYSTEMS Inc. or contact Kenshiro Kimura.

GRRM23 uses a floating license approach for validating users; it requires setting up a license server.
For this, HPC SYSTEMS Inc. allows users to connect to license servers at their company site in Japan at no additional cost.
Alternatively, a license server can be set up at your university in Canada.
For more about either license server option contact technical support at HPC SYSTEMS Inc.

== Installation ==
After buying a license, users will receive a link and instructions to download a compressed tar.bz2 file. Download the file and follow the instructions below.

In your home directory, create a directory for the installation and another one for the executables:

mkdir GRRM23_Installation
mkdir GRRM23_RUN

Move the compressed GRRM23 file to $HOME/GRRM23_Installation and extract it there:

cd GRRM23_Installation
tar xjf GRRM23.tar.bz2

Verify that this has created an installation script (install.sh).
Then from $HOME/GRRM23_Installation, execute the script as follows:

./install.sh /home/user/GRRM23_RUN

The installation will prompt you to the following screen:

Installation configuration:
GRRMroot = /home/user/GRRM23_RUN
Intel MPI installation prefix = /home/user/GRRM23_RUN/mpi-rt
Are you sure to start installation? [Y/n]

Type “Y” and press “Enter” to proceed with the installation. Once the
installation is finished, a “GRRM INSTALLATION DONE” message should appear:

Installing Intel MPI ... done successfully.
Installing GRRM binary ...done successfully.
Installing STLib ...done successfully.

GRRM INSTALLATION DONE.
IMPORTANT[1]: Before using GRRM, please insert lines below to your shell (/bin/bash) configuration file.
IMPORTANT[2]: Please consult your system administrator about the STLM server IP address and port number.

source /home/user/GRRM23_RUN/mpi-rt/mpi/2021.6.0/env/vars.sh
export PATH="/home/user/GRRM23_RUN:${PATH}"
export LD_LIBRARY_PATH="/home/user/GRRM23_RUN:${LD_LIBRARY_PATH}"
export GRRMroot="/home/user/GRRM23_RUN"
export subgrr="GRRM23.out"
export subgau=""
export subchk=""
export subuchk=""
export submol=""
export subsiesta=""
export submpi="mpirun"
export I_MPI_FABRICS="shm:tcp"
export I_MPI_FALLBACK=0
export I_MPI_HYDRA_BOOTSTRAP="ssh"
export STLM_SERVER_ADDRESS="XXX.XXX.XXX.XXX"
export STLM_SERVER_PORT=XXXXX

Copy the last lines (from source to the last export line) into your .bashrc in your home directory. Since G16 is not loaded on the Alliance's login nodes, you need to manually add g16, formchk and unfchk into the corresponding lines below (subgau, subchk and subunchk, respectively). For validating your license, replace the XXX values in STLM_SERVER_ADDRESS and STLM_SERVER_PORT with the information provided by HPC SYSTEMS Inc. for your license (HPC SYSTEMS Inc. will send users this information via email):

source /home/user/GRRM23_RUN/mpi-rt/mpi/2021.6.0/env/vars.sh
export PATH="/home/user/GRRM23_RUN:${PATH}"
export LD_LIBRARY_PATH="/home/user/GRRM23_RUN:${LD_LIBRARY_PATH}"
export GRRMroot="/home/user/GRRM23_RUN"
export subgrr="GRRM23.out"
export subgau="g16"
export subchk="formchk"
export subuchk="unfchk"
export submol=""
export subsiesta=""
export submpi="mpirun"
export I_MPI_FABRICS="shm:tcp"
export I_MPI_FALLBACK=0
export I_MPI_HYDRA_BOOTSTRAP="ssh"
export STLM_SERVER_ADDRESS="XXX.XXX.XXX.XXX"
export STLM_SERVER_PORT=XXXXX

Log out and log in again, or source your .bashrc file:

source ~/.bashrc

Then type GRRM23p on the terminal. If the installation was successful, the following text should appear:

USAGE: GRRMp [input file name] (-p[Nproc]) (-h[Hour]) (-w/xxx/xxx)
(-f[machine_file]) (-c[Ncore])

Gaussian (G16) is already installed on Fir and Nibi.
Compute nodes on both systems have access to the Internet for the purpose of contacting a license server.

== Usage ==
For input examples, please refer to the GRRM23 user’s manual.
In most cases GRRM23 requires only one input file (Job.com) containing the Cartesian coordinates of a molecule and methodology options.
In some other cases, GRRM23 requires the output of a previous GRRM23 job.

=== Sample Slurm script for a single node ===
For a single node (--nodes=1) and 12 cores (--ntasks-per-node=12), running from your /scratch directory:

#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem-per-cpu=4000M

module load gaussian/g16.c01
export GAUSS_SCRDIR=/home/user/scratch/

GRRM23p Job -p1 -s80000

* -p1: number of parallel processes.
* -s80000: signals when (in seconds) to create a checkpoint file so that an interrupted job can be restarted properly.  Notice that 80000 second is about 22 hours.  This time should be less than the --time you request from Slurm.

Multiple nodes not supported:
Due to the Gaussian licenses at Fir and Nibi, GRRM23 can be used with Gaussian only on a single node.

=== Example using ORCA ===

#!/bin/bash
#SBATCH --time=18:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=4000M

module load StdEnv/2023  gcc/12.3  openmpi/4.1.5
module load orca/6.0.0

GRRM23p glucose -p1 -h15

== External resources ==
GRRM manuals: https://afir.sci.hokudai.ac.jp/manual/

== Acknowledgements ==
The original draft of this page was contributed by Eduardo Romero Montalvo.