---
title: "Star-CCM+"
url: "https://docs.alliancecan.ca/wiki/Star-CCM%2B"
category: "General"
last_modified: "2026-06-29T17:45:20Z"
page_id: 4355
display_title: "Star-CCM+"
---

STAR-CCM+ is a multidisciplinary engineering simulation suite to model acoustics, fluid dynamics, heat transfer, rheology, multiphase flows, particle flows, solid mechanics, reacting flows, electrochemistry, and electromagnetics. It is developed by Siemens.

= License limitations =
The Alliance is authorized to host STAR-CCM+ binaries on its clusters. Researchers will need to purchase a license from Siemens in order to use the software. There are two options. Most research groups will purchase a Power-on-Demand (PoD) license which simply connects to a remotely hosted license server and requires only a license key to use. The second option is more complex and requires setting up and then managing a locally hosted institutional license server along with the purchase of a Simcenter STAR-CCM+ academic pack.  For this to work the local firewall of your STAR-CCM+ license server will need to be reconfigured.  You will need to ask the administrator of your license server at your institution to open its flex and static vendor ports so they are BOTH reachable from the Network Address Translation (NAT) nodes for each of the Alliance clusters that you will be using.  To get a list of NAT nodes for your administrator submit a ticket including 1) the names of ALL of the Alliance clusters you will be using 2) the hostname (FQDN) or public IP address of your STAR-CCM+ license server along with its flex and static vendor port numbers.

== Configuring your account ==
To configure your account to use a license server with the Star-CCM+ module, create a license file $HOME/.licenses/starccm.lic with the following layout:

where  and  should be changed to specify the hostname (or ip address) and the static vendor port of the license server respectively.  Note that manually setting CDLMD_LICENSE_FILE equal to @ in your slurm script is not required since this variable is automatically set whenever a starccm module is loaded.

=== PoD license file ===

To run jobs researchers with a Power-on-Demand (PoD) license must manually set the LM_PROJECT environment variable to your 22digit-PoD-License-Key as shown in the sample slurm scripts below.  The following ~/.licenses/starccm.lic file must also be configured on each cluster where jobs are to be run :

= Cluster batch job submission =

Before submitting jobs on a cluster, you must set up a ~/.licenses/starccm.lic file on each cluster where you will run jobs.  If you have a PoD license then the required firewall changes have already been done on all of the Alliance clusters.  If however you will be using a local institutional license server then you will need to submit a problem ticket to technical support to request the one time network firewall changes be made between the cluster(s) and your local license server.   If you have problems getting the licensing to work then try removing or renaming file ~/.flexlmrc since previous search paths and/or license server settings maybe stored in it.  Note that temporary output files from starccm jobs runs may accumulate in hidden directories named ~/.star-version_number consuming valuable quota space.  These can be removed by periodically running rm -ri ~/.starccm* and replying yes when prompted.

== Slurm scripts ==

 awk '{print $2}')
port=$(cat $CDLMD_LICENSE_FILE  grep -Eo '[0-9]+$')
nmap $server -Pn -p $port  grep -v '^$'; echo

CPU_VENDOR=$(lscpu  awk '/Vendor ID/{print $3}')
echo "CPU_VENDOR= $CPU_VENDOR"
if [ "$CPU_VENDOR" == GenuineIntel ]; then
  if [ "${EBVERSIONSTARCCM:0:2}" -lt 20 ]; then
    STAR_UCX="-xsystemucx"
    export FLEXIBLAS=StarMKL
  else
    STAR_FLEXIBLAS="-flexiblaslib MKL"
  fi
  STAR_MPI="-mpi intel"
  STAR_FABRIC="-fabric tcp"
elif [ "$CPU_VENDOR" == AuthenticAMD ]; then
  if [ "${EBVERSIONSTARCCM:0:2}" -lt 20 ]; then
    STAR_UCX="-xsystemucx"
    export FLEXIBLAS=StarAOCL
  else
    STAR_FLEXIBLAS="-flexiblaslib AOCL"
    STAR_PRELOAD="-ldpreload /usr/lib64/libdrm_amdgpu.so.1"
  fi
  STAR_MPI="-mpi openmpi40"
fi

if [ -n "$LM_PROJECT" ]; then
   echo "Siemens PoD license server ..."
   starccm+ -jvmargs "-Xmx4G -Djava.io.tmpdir=$SLURM_TMPDIR" -batch $BATCH_CMD -power -podkey $LM_PROJECT -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI $STAR_UCX $STAR_FABRIC $STAR_FLEXIBLAS $STAR_PRELOAD
else
   echo "Institutional license server ..."
   [ $(command -v lmutil) ] && lmutil lmstat -c ~/.licenses/starccm.lic -a  egrep "license1UPuse$USER"; echo
   starccm+ -jvmargs "-Xmx4G -Djava.io.tmpdir=$SLURM_TMPDIR" -batch $BATCH_CMD -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI $STAR_UCX $STAR_FABRIC $STAR_FLEXIBLAS $STAR_PRELOAD
fi
}}

 awk '{print $2}')
port=$(cat $CDLMD_LICENSE_FILE  grep -Eo '[0-9]+$')
nmap $server -Pn -p $port  grep -v '^$'; echo

export FLEXIBLAS=NETLIB
STAR_MPI="-mpi openmpi"
if [ "$RSNT_CPU_VENDOR_ID" == intel ]; then
  export FLEXIBLAS=StarMKL
  STAR_MPI="-mpi intel"
elif [ "$RSNT_CPU_VENDOR_ID" == amd ]; then
  export FLEXIBLAS=StarAOCL
fi
echo "FLEXIBLAS=$FLEXIBLAS"

if [ "${EBVERSIONSTARCCM:0:2}" -lt 20 ]; then
  STAR_UCX="-xsystemucx"
fi

if [ -n "$LM_PROJECT" ]; then
   echo "Siemens PoD license server ..."
   starccm+ -jvmargs "-Xmx4G -Djava.io.tmpdir=$SLURM_TMPDIR" -batch $BATCH_CMD -power -podkey $LM_PROJECT -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $SIM_FILE $STAR_MPI $STAR_UCX
else
   echo "Institutional license server ..."
   [ $(command -v lmutil) ] && lmutil lmstat -c ~/.licenses/starccm.lic -a  egrep "license1UPuse$USER"; echo
   starccm+ -jvmargs "-Xmx4G -Djava.io.tmpdir=$SLURM_TMPDIR" -batch $BATCH_CMD -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $SIM_FILE $STAR_MPI $STAR_UCX
fi
}}

= Graphical use =

To run starccm+ in graphical mode it is recommended to use an  OnDemand or JupyterLab system to start a remote desktop.  In addition to configuring ~/.licenses/starccm.lic, research groups with a POD license should also run export LM_PROJECT='22digit-PoD-License-Key' before starting starccm+ as shown below.  Additional command line options such as -power may also need to be appended depending on your license type.  Note that running module avail starccm will display all mixed and R8 versions that are available to load within the StdEnv/version you currently have loaded ie) 2020 or 2023.  Alternatively running module spider starccm will show all mixed and R8 module versions available to load within both StdEnv module versions that could be loaded ie) 2020 and 2023.

== OnDemand ==
1. To start an OnDemand desktop session click one of the following OnDemand links :
 NIBI: https://ondemand.sharcnet.ca
 TRILLIUM: https://ondemand.scinet.utoronto.ca
2. Open a new terminal window in your desktop and run one of:
: STAR-CCM+ 18.04.008 (or newer versions)
:: module load StdEnv/2023  (default)
:: module load starccm-mixed/21.02.008 **OR** starccm/21.02.008-R8
:: starccm+ -rr server   (Process Options="Serial")
:: starccm+ -rr server -np 2 -mpi openmpi40   (Process Options="Parallel on Local Host")
: STAR-CCM+ 15.04.010 → 17.06.008 (version range)
:: module load StdEnv/2020 (retired)
:: module load starccm-mixed/17.06.008 **OR** starccm/17.06.008-R8
:: starccm+    (Process Options="Serial")
:: starccm+ -np 2   (Process Options="Parallel on Local Host")
== JupyterLab ==
1. Start a JupyterHub desktop session by clicking one of the following JupyterHub links :
 FIR: https://jupyterhub.fir.alliancecan.ca
 NARVAL:  https://portail.narval.calculquebec.ca/
 RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
2. Click the hexagon shaped Software Modules gear icon located at the bottom of the left most vertical icon selector menu
3. Highlight a starccm module such as starccm-mixed/21.02.008/code> **OR** starccm/21.02.008-R8 and click Load
4. Click the rectangular StarCCM+ Mixed(VNC) **OR** StarCCM (VNC) icon that appears in desktop
5. To run StarCCM+ with multiple cores for compute purposes;
: Click File -> New and a Create a File configurator panel should appear
: Change the default Serial Process Option by instead ticking the Parallel on Local Host radio button
: Add -mpi openmpi40 to the end of the Command: string located at the bottom of the panel
: Finally click the OK button and the starccm+ gui should appear

== VncViewer ==
These instructions are retained for legacy purposes only :

1. Connect with a VncViewer client to a login or compute node by following TigerVNC
2. Open a new terminal window in your desktop and run one of:
: STAR-CCM+ 18.04.008 (or newer versions)
:: module load StdEnv/2023  (default)
:: module load starccm-mixed/21.02.008/code> **OR** starccm/21.02.008-R8
:: starccm+ -rr server ** OR ** starccm+ -rr server -np 2 -mpi openmpi40
: STAR-CCM+ 15.04.010 → 17.06.008 (version range)
:: module load StdEnv/2020 (retired)
:: module load starccm-mixed/17.06.008 **OR** starccm/17.06.008-R8
:: starccm+