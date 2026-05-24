---
title: "COMSOL/en"
url: "https://docs.alliancecan.ca/wiki/COMSOL/en"
category: "General"
last_modified: "2026-05-15T15:27:26Z"
page_id: 6233
display_title: "COMSOL"
---

= Introduction =
COMSOL is a general-purpose software for modelling engineering applications. We would like to thank COMSOL, Inc. for allowing its software to be hosted on our clusters via a special agreement.

We recommend that you consult the documentation included with the software under File > Help > Documentation prior to attempting to use COMSOL on one of our clusters.  Links to the COMSOL blog, Knowledge Base, Support Centre and Documentation can be found at the bottom of the COMSOL home page.  Searchable online COMSOL documentation is also available  here.

= Licensing =
We are a hosting provider for COMSOL. This means that we have COMSOL software installed on our clusters, but we do not provide a generic license accessible to everyone. Many institutions, faculties, and departments already have licenses that can be used on our clusters.  Alternatively, you can purchase a license from CMC for use anywhere in Canada. Once the legal aspects are worked out for licensing, there will be remaining technical aspects. The license server on your end will need to be reachable by our compute nodes. This will require our technical team to get in touch with the technical people managing your license software. If you have purchased a CMC license and will be connecting to the CMC license server, this has already been done. Once the license server work is done and your ~/.licenses/comsol.lic has been created, you can load any COMSOL module and begin using the software.  If this is not the case, please contact our technical support.

== Configuring your own license file ==
Our COMSOL module is designed to look for license information in a few places, one of which is your ~/.licenses directory. If you have your own license server then specify it by creating a text file $HOME/.licenses/comsol.lic with the following information:

Where  is your license server hostname and  is the flex port number of the license server.

=== Local license setup ===

For researchers wanting to use a new local institutional license server, firewall changes will need to be done to the network on both the Alliance (system/cluster) side and the institutional (server) side. To arrange this, send an email to technical support containing 1) the COMSOL lmgrd TCP flex port number (typically 1718 default) and 2) the static LMCOMSOL TCP vendor port number (typically 1719 default) and finally 3) the fully qualified hostname of your COMSOL license server.  Once this is complete, create a corresponding comsol.lic text file as shown above.

=== CMC license setup ===

Researchers who own a COMSOL license subscription from CMC should use the following preconfigured public IP settings in their comsol.lic file:

* Fir: SERVER 172.26.0.101 ANY 6601
* Nibi: SERVER 10.25.1.56 ANY 6601
* Narval/Rorqual: SERVER 10.100.64.10 ANY 6601
* Trillium: SERVER scinet-cmc ANY 6601

For example, a license file created on Nibi cluster would look as follows:
 [l2 (login node):~] cat ~/.licenses/comsol.lic
 SERVER 10.25.1.56 ANY 6601
 USE_SERVER

If initial license checkout attempts fail, create a support case with CMC

== Checking license use ==

To determine the number of licenses checked out by your running comsol jobs it is necessary to query the licence server.  As described here this maybe done using the lmutil command.  However as this particular command is not installed with the COMSOL by default the following one-liner command maybe used instead.  To use it, simply copy/paste the following one-liner into your terminal window on a cluster login node and hit enter.  It will then read your ~/.licenses/comsol.lic to determine which COMSOL server you are using and may take ~30sec to return.  While it should work when run on any login node of Nibi, Narval, Rorqual or Trillium clusters for CMC license holders, it may or may not work with other institutional servers depending on how they are configured.

   touch ~/.licenses/ansys.lic; module load ansys; $EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil lmstat -c ~/.licenses/comsol.lic -a | sed '/^$/d' | egrep 'License|UP|$USER|Total of'  | grep -v 'Total of 0'; module unload ansys

== Installed products ==

To check which modules and products are available for use, start COMSOL in graphical mode and then click Options -> Licensed and Used Products on the upper pull-down menu.  For a more detailed explanation, click  here.  If a module/product is missing or reports being unlicensed, contact technical support as a reinstall of the CVMFS module you are using may be required.

== Installed versions ==
To check the full version number either start comsol in gui mode and inspect the lower right corner messages window OR more simply login to a cluster and run comsol in batch mode as follows:
 [login-node:~] salloc --time=0:01:00 --nodes=1 --cores=1 --mem=1G --account=def-someuser
 [login-node:~] module load comsol/6.2
 [login-node:~] comsol batch -version
 COMSOL Multiphysics 6.2.0.290
which corresponds to COMSOL 6.2 Update 1.  In other words, when a new COMSOL release is installed, it will use the abbreviated 6.X version format but for convenience will contain the latest available update at the time of installation.  As additional product updates are released they will instead utilize the full 6.X.Y.Z version format.   For example, Update 3 can be loaded on a cluster with the module load comsol/6.2.0.415 OR module load comsol commands.  We recommend using the moat recent update to take advantage of all the latest improvements. That said, if you want to continue using any module version (6.X or 6.X.Y.Z). you can be assured by definition that the software contained in these modules will remain exactly the same.

To check which versions are available in the standard environment you have loaded ( typically StdEnv/2023 ) run the module avail comsol command.  Lastly, to check which versions are available in ALL available standard environments, use the module spider comsol command.

A module comsol/6.3 corresponding to version 6.3.0.290 is now available on all clusters.

= Submit jobs =

== Single compute node ==

Sample submission script to run a COMSOL job with eight cores on a single compute node:

Depending on the complexity of the simulation, COMSOL may not be able to efficiently use very many cores.  Therefore, it is advisable to test the scaling of your simulation by gradually increasing the number of cores. If near-linear speedup is obtained using all cores on a compute node, consider running the job over multiple full nodes using the next Slurm script.

== Multiple compute nodes ==

Sample submission script to run a COMSOL job with eight cores distributed evenly over two compute nodes.  Ideal for very large simulations (that exceed the capabilities of a single compute node), this script supports restarting interrupted jobs, allocating large temporary files to /scratch and utilizing the default comsolbatch.ini file settings.  There is also an option to modify the Java heap memory described below the script.

Note 1: If your multiple node job crashes on startup with a java segmentation fault, try increasing the java heap by adding the following two sed lines after the two cp -f lines.  If it does not help, try further changing both 4g values to 8g. For further information see Out of Memory.
 sed -i 's/-Xmx2g/-Xmx4g/g' comsolbatch.ini
 sed -i 's/-Xmx768m/-Xmx4g/g' java.opts

Note: If a job runs slow or hangs during startup when submitted to a single node with the above script-smp.sh script, try using the above multiple node script-dis.sh script instead with #SBATCH --nodes=1 and then please open a ticket to report the problem including the job number and cluster name.

= Graphical use =

To run comsol in graphical mode open a remote desktop on an OnDemand or JupyterLab system by clicking one of the following links.  Note that the old approach of using a TigerVNC client/server pair should still work but is no longer recommended or supported.  For either approach  ~/.licenses/comsol.lic must first be configured.  Note that running command module avail comsol will display which comsol versions are available within the StdEnv version that you currently have loaded ie) StdEnv/2023 .  If you find the upper menu items are greyed out and not clickable after starting COMSOL in GUI mode then your ~/.comsol maybe corrupted so try deleting it.

== OnDemand ==
1. Start an OnDemand desktop session by clicking one of the following OnDemand links
 NIBI: https://ondemand.sharcnet.ca
 TRILLIUM: https://ondemand.scinet.utoronto.ca
2. Open a new terminal window in your desktop and run one of:
: COMSOL 6.2 (or newer versions)
:: module load StdEnv/2023  (default)
:: module load comsol/6.4
:: comsol
: COMSOL 6.1 (or older versions)
:: module load StdEnv/2020  (default)
:: module load comsol/6.1
:: comsol

== JupyterLab ==
1. Start a JupyterHub desktop session by clicking one of the following JupyterHub links
 FIR: https://jupyterhub.fir.alliancecan.ca
 NARVAL:  https://portail.narval.calculquebec.ca/
 RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
2. Highlight a comsol module such as comsol/6.4 in the left hand side Available Module section
3. Click Load for the highlighted module and a Comsol (VNC) Icon will appear in desktop
4. Click the Icon and comsol should automatically be started in a remote Juypter desktop

=Parameter sweeps=

==Batch sweep==

When working interactively in the COMSOL GUI, parametric problems may be solved using the Batch Sweep approach.  Multiple parameter sweeps maybe carried out as shown in this video.  Speedup due to Task Parallism may also be realized.

==Cluster sweep==

To run a parameter sweep on a cluster, a job must be submitted to the scheduler from the command line using sbatch slurmscript.  For a discussion regarding additional required arguments, see a and b for details. Support for submitting parametric simulations to the cluster queue from the graphical interface using a Cluster Sweep node is not available at this time.