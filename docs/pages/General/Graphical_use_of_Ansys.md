---
title: "Graphical use of Ansys/en"
url: "https://docs.alliancecan.ca/wiki/Graphical_use_of_Ansys/en"
category: "General"
last_modified: "2026-08-17T13:58:41Z"
page_id: 34278
display_title: "Graphical use of Ansys"
---

To run Ansys programs in graphical mode using an OnDemand or JupyterHub desktop, click on one of the following links:

 Nibi: https://ondemand.sharcnet.ca
 Fir: https://jupyterhub.fir.alliancecan.ca
 Rorqual: https://jupyterhub.rorqual.alliancecan.ca
 Narval:  https://jupyterhub.narval.alliancecan.ca/
 Trillium: https://ondemand.scinet.utoronto.ca

A job submission web page should appear in your browser.  Configure the resources required for your interactive desktop session and click on Launch or Start.  If either accelerated graphics or computations will be conducted from within your desktop session, be sure to specify a GPU resource.  Load an Ansys module on the desktop.  If you started a JupyterLab-powered desktop, this can be done by clicking in the menu on the left; however, if you started an OnDemand desktop manually, type module load ansys/version on the command line.  To start one of the common Ansys programs such as Fluent, CFX, Workbench, and so forth, refer to the following sections which provide advice for setting environment variables and arguments required by VirtualGL or Mesa-based graphical environments, depending on whether a node with a GPU resource was specified or not.

=== Fluent ===

To start Ansys Fluent from the command line on an OnDemand desktop, open a terminal window and run

::: module load StdEnv/2023 ansys/2025R2.04
::: fluent

When the Fluent Launcher popup selector panel appears, click on the Environment tab and copy/paste the environment variable settings from one of the following two subsections, depending on whether you started your OnDemand session with a GPU for graphical acceleration. Do not include the text in parentheses as these are comments, and do not put export in front of any variable name. If the graphics console window becomes corrupted when starting the GUI, restart Fluent, setting HOOPS_PICTURE=null to disable the creation of the graphics panel.

Compute node (no GPU requested)

::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on Nibi w/ intelmpi)
::: HOOPS_PICTURE=opengl2-mesa    (version 2025R1 or newer)
::: HOOPS_PICTURE=x11/lin                (version 2024R2.04 or older)
::: Click on the Start button.

Compute node (with GPU requested)

To use hardware accelerated graphics with Fluent on Nibi, choose a t4 (15GB) from the GPU selector pulldown list for your OnDemand desktop session.  Doing this ensures that the environment variables used by VirtualGL to enable accelerated OpenGL graphics calls are automatically set up inside your desktop environment for the current session.  Once your desktop appears, open a terminal window and start Workbench as follows
::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on Nibi)
::: HOOPS_PICTURE=opengl2              (version 2025R1 or newer)
::: HOOPS_PICTURE=opengl                (version 2024R2.04 or older)
::: Click on the Start button.

NOTE: When running Fluent on Nibi, the environment variable I_MPI_HYDRA_BOOTSTRAP=ssh must be manually set; otherwise, Fluent will crash when started inside OOD Compute Desktop sessions when intelmpi is used.  Error output such as the following will be created.  Should this occur, completely exit Fluent, cleanly shut down Workbench and start over.
 [mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
 [mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
 [mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
 [mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
 [mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

=== CFX ===

When starting CFX from an OnDemand desktop, the following arguments may be specified on the terminal window command line.  Use ogl if you requested a GPU when the desktop was started and use mesa if you did not.

::: cfx5 -graphics mesa   (no GPU requested)
::: cfx5 -graphics ogl     (with GPU requested)

=== Mapdl ===

The following steps for starting the Mechanical APDL GUI from the command line of a terminal window should work regardless  of whether you have started your OnDemand desktop on a compute node with or without a GPU.

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

To start Fluent from within Workbench, click on Fluid Flow (Fluent) or Fluent with Fluent Meshing in the Analysis menu on the left, and click on Setup in the centre canvas Fluid Flow (Fluent) popup.  Once the Fluent Launcher selector panel popup appears, click on the Environment tab and copy/paste the following environment variable settings:
::: I_MPI_HYDRA_BOOTSTRAP=ssh      (required on the Nibi cluster only when using intelmpi)
::: HOOPS_PICTURE=opengl2-mesa    (optional for 2025R1 or newer)
::: Click on the Start button.

Compute node (with GPU requested)

If accelerated graphics are required on the Nibi cluster, choose t4 (15GB) from the GPU selector pulldown list for your OnDemand desktop session.  Doing this will ensure that the environment variables used by VirtualGL to enable accelerated OpenGL graphics calls are automatically set up inside your desktop environment for the current session.  Once your desktop appears, open a terminal window and start Workbench as follows
::: module load StdEnv/2023 ansys/2025R2.04
::: runwb2

To start Fluent from within Workbench, click on Fluid Flow (Fluent) or Fluent with Fluent Meshing in the left-hand Analysis menu, and click on Setup in the centre canvas Fluid Flow Fluent popup.  Once the Fluent Launcher selector panel popup appears, click on the Environment tab and copy/paste the following environment variable settings.
::: I_MPI_HYDRA_BOOTSTRAP=ssh     (required on the Nibi cluster only)
::: HOOPS_PICTURE=opengl2             (optional for 2025R1 or newer)
::: Click on the Start button.

==== JupyterHub desktop ====

Compute node (no GPU requested)

1. Click to load ansys/2025R1 (or newer version) in the desktop menu on the left.
2. Click on the Workbench (VNC) icon located in the JupyterLab desktop centre window.
: If the graphics of any application (such as Fluent) started within Workbench appear unusable because they seem corrupted, try carrying out the following steps.  They will create a custom runwb2 desktop icon so that Workbench can be started in Mesa mode.  If one of the applications you will be starting  in Workbench is Fluent, you may also try setting
::HOOPS_PICTURE=opengl2-mesa variable in the Fluent Launcher window when the Fluent launcher starts
::HOOPS_PICTURE=opengl2-mesa variable in the Fluent Launcher window.
3. To proceed, exit Workbench and open a terminal window.  Copy/paste cd ~/Desktop; cp -p $(realpath workbench.desktop) workbench-mesa.desktop into the Remote Clipboard located at the top right corner of your Jupyter desktop.
4. Open the newly created file in a text editor such as nano with
:nano ~/Desktop/workbench-mesa.desktop
5. Change all instances of runwb2 and exit the editor, saving the changes.
6. Now REFRESH the Jupyter desktop by pressing the key combination control-R.  The new icon should now appear in the desktop along with the original Workbench icon. Double-click on it to start Workbench. The new icon will persist for future sessions until manually deleted with
:rm -f ~/Desktop/workbench-mesa.desktop

Compute node (with GPU requested)

::: Click to load ansys/2025R1 (or newer version) in the desktop menu.
::: Click the Workbench (VNC) icon located in the JupyterLab desktop centre window.

=== Ensight ===
::: module load StdEnv/2023 ansys/2022R2; A=222; B=5.12.6
::: export LD_LIBRARY_PATH=$EBROOTANSYS/v$A/CEI/apex$A/machines/linux_2.6_64/qt-$B/lib
::: ensight -X

=== Rocky ===
Load the following modules
 module load StdEnv/2023 ansys/2025R2.04 (or 2025R1, 2025R1.02, 2025R2)
*The Rocky command starts Rocky in graphical mode.
* The RockySolver command runs the solver directly from the command line.
* The RockySchedular GUI starts a GUI to submit/run jobs on the current node.

== Electronics ==

See  our AnsysEDT wiki page.