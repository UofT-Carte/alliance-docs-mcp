---
title: "JupyterNotebook/en"
url: "https://docs.alliancecan.ca/wiki/JupyterNotebook/en"
category: "General"
last_modified: "2026-10-23T15:00:01Z"
page_id: 4559
display_title: "JupyterNotebook"
---

==Introduction==

"Project Jupyter is a non-profit, open-source project, born out of the IPython Project in 2014 as it evolved to support interactive data science and scientific computing across all programming languages."http://jupyter.org/about.html

"The Jupyter Notebook is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text."http://www.jupyter.org/

You can run Jupyter Notebook on a compute node or on a login node (not recommended). Note that login nodes impose various user- and process-based limits, so applications running there may be killed if they consume too much CPU time or memory. To use a compute node you will have to submit a job requesting the number of CPUs (and optionally GPUs), the amount of memory, and the run time. Here, we give instructions to submit a Jupyter Notebook job.

Other information:
* Since Jupyter Notebook is the older Jupyter interface, please consider installing JupyterLab instead.
* If you are instead looking for a preconfigured Jupyter environment, please see the Jupyter page.

== Installing Jupyter Notebook ==

These instructions install Jupyter Notebook with the pip command in a  Python virtual environment in your home directory. The following instructions are for Python 3.7, but you can also install the application for a different version by loading a different Python module.

Load the Python module.

Create a new Python virtual environment.

Activate your newly created Python virtual environment.

Install Jupyter Notebook in your new virtual environment.

In the virtual environment, create a wrapper script that launches Jupyter Notebook.
$SLURM_TMPDIR/jupyter\njupyter notebook --ip $(hostname -f) --no-browser' > $VIRTUAL_ENV/bin/notebook.sh
}}
Finally, make the script executable.

== Installing extensions ==

Extensions allow you to add functionalities and modify the application’s user interface.

=== Jupyter Lmod ===

Jupyter Lmod is an extension that allows you to interact with environment modules before launching kernels. The extension uses the Lmod's Python interface to accomplish module-related tasks like loading, unloading, saving a collection, etc.

=== Proxy web services ===

nbserverproxy enables users to reach arbitrary web services running within their spawned Jupyter server. This is useful to access web services that are listening only on a port of the localhost like TensorBoard.

==== Example ====

In Jupyter, a user starts a web service via 'Terminal' in the New dropdown list:

8008
}}

The service is proxied off of /proxy/ at https://address.of.notebook.server/user/theuser/proxy/8008.

=== RStudio Launcher ===

Jupyter Notebook can start an RStudio session that uses Jupyter Notebook's token authentication system. RStudio Launcher adds an RStudio Session option to the Jupyter Notebook New dropdown list.

Note: the installation procedure below only works with the StdEnv/2016.4 and StdEnv/2018.3 software environments.

== Activating the environment ==

Once you have installed Jupyter Notebook, you need only reload the Python module associated with your environment when you log into the cluster.

Then, activate the virtual environment in which you have installed Jupyter Notebook.

=== RStudio Server (optional) ===

To use  RStudio Launcher, load the RStudio Server module.

== Starting Jupyter Notebook ==

To start the application, submit an interactive job. Adjust the parameters based on your needs. See Running jobs for more information.

1:0:0 --ntasks1 --cpus-per-task2 --mem-per-cpu1024M --accountdef-yourpi srun $VIRTUAL_ENV/bin/notebook.sh
|result=
salloc: Granted job allocation 1422754
salloc: Waiting for resource configuration
salloc: Nodes cdr544 are ready for job
[I 14:07:08.661 NotebookApp] Serving notebooks from local directory: /home/fafor10
[I 14:07:08.662 NotebookApp] 0 active kernels
[I 14:07:08.662 NotebookApp] The Jupyter Notebook is running at:
[I 14:07:08.663 NotebookApp] http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e32af8d20efa72e72476eb72ca
[I 14:07:08.663 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 14:07:08.669 NotebookApp]

Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e3}}

== Connecting to Jupyter Notebook ==

To access Jupyter Notebook running on a compute node from your web browser, you will need to create an SSH tunnel between the cluster and your computer since the compute nodes are not directly accessible from the Internet.

=== From Linux or MacOS X ===

On a Linux or MacOS X system, we recommend using the sshuttle Python package.

On your computer, open a new terminal window and run the following sshuttle command to create the tunnel.

In the preceding command substitute  by your username; and substitute  by the cluster you connected to launch your Jupyter Notebook.

Then, copy and paste the provided URL into your browser. In the above example, this would be

 http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e3

=== From Windows ===

An SSH tunnel can be created from Windows using  MobaXTerm as follows.  This will also work from any Unix system (MacOS, Linux, etc).

Open a new Terminal tab in MobaXTerm (Session 1) and connect to a cluster. Then follow the instructions in section  Starting Jupyter Notebook. At this point, you should have on your screen an URL with the following form.

http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e3
       └────────────────┬───────────────────┘        └──────────┬───────────┘
                  hostname:port                               token

Open a second Terminal tab in MobaXTerm (Session 2). In the following command, substitute  by its corresponding value from the URL you obtained in Session 1 (refer to the previous figure); substitute  by your username; and substitute  by the cluster you connected to in Session 1. Run the command.

 Open your browser and go to

 http://localhost:8888/?token=

Replace  with its value from Session 1.

== Shutting down Jupyter Notebook ==

You can shut down the Jupyter Notebook server before the walltime limit by pressing Ctrl-C twice in the terminal that launched the interactive job.

If you used MobaXterm to create a tunnel, press Ctrl-D in Session 2 to shut down the tunnel.

== Adding kernels ==

It is possible to add kernels for other programming languages or Python versions different than the one running the Jupyter Notebook. Refer to Making kernels for Jupyter to learn more.

The installation of a new kernel is done in two steps.
#Installation of the packages that will allow the language interpreter to communicate with Jupyter Notebook.
#Creation of a file that will indicate to Jupyter Notebook how to initiate a communication channel with the language interpreter. This file is called a kernel spec file.

Each kernel spec file has to be created in its own subfolder inside a folder in your home directory with the following path  ~/.local/share/jupyter/kernels. Jupyter Notebook does not create this folder, so the first step in all cases is to create it. You can use the following command.

In the following sections, we provide a few examples of the kernel installation procedure.

=== Julia ===

Load the Julia module.
Activate the Jupyter Notebook virtual environment.
Install IJulia.  julia}}

For more information, see the IJulia documentation.

=== Python ===

Load the Python module.
Create a new Python virtual environment.
Activate your newly created Python virtual environment.
Install the ipykernel library.
Generate the kernel spec file.  Substitute  by a name that will uniquely identify your kernel.
Deactivate the virtual environment.

For more information, see the ipykernel documentation.

=== R ===

Load the R module.
Activate the Jupyter Notebook virtual environment.
Install the R kernel dependencies. 'http://cran.us.r-project.org')"}}
Install the R kernel.
Install the R kernel spec file.

For more information, see the IRKernel documentation.

== References ==