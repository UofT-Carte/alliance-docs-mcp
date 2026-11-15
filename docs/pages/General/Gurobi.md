---
title: "Gurobi/en"
url: "https://docs.alliancecan.ca/wiki/Gurobi/en"
category: "General"
last_modified: "2026-11-08T16:21:37Z"
page_id: 14002
display_title: "Gurobi"
---

Gurobi is a commercial software suite for solving complex optimization problems.  This wiki page describes the non-commercial use of Gurobi software on our clusters.

== License limitations ==

We support and provide a free license to use Gurobi on the Nibi, Narval, Fir, Rorqual and Trillium clusters.  The license provides a total number of 4096 simultaneous uses (tokens in use) and permits distributed optimization with up to 100 nodes.  A single user can run multiple simultaneous jobs.  In order to use Gurobi, you must agree to certain conditions. Please  contact support and include a copy of the following completed agreement.  You will then be added into our license file as a user within a few days.

===Academic usage agreement===

My Alliance username is "_______" and I am a member of the academic institution "_____________________."  This message confirms that I will only use the Gurobi license provided on Digital Research Alliance of Canada systems for the purpose of non-commercial research project(s) to be published in publicly available article(s).

===Configuring your account===
You do NOT need to create a ~/.licenses/gurobi.lic file.  The required settings to use our Gurobi license are configured by default when you load a Gurobi module on any cluster.

===Testing your license===
To verify your username has successfully been added to the Alliance Gurobi license, log into any cluster and run the following command:

 $ module load gurobi
 $ gurobi_cl 1> /dev/null && echo Success || echo Fail

If it returns "Success" you can begin using Gurobi immediately.  If the test returns "Fail" then check whether a file named ~/.license/gurobi exists.  If it does then remove it, reload the gurobi module and run the test again.  If it still returns "Fail" check whether there are any environment variables containing GUROBI being defined in either of our your ~/.bashrc or ~/.bash_profile files.  If you find any, comment or remove the lines then logout and login again, reload the Gurobi module and run the test again.  If you still get "Fail",  contact support for help.

===Minimizing license checkouts===

Note that all Gurobi license checkouts are handled by a single license server located in Ontario; it is therefore important to limit license checkout attempts as much as possible.  Rather than checking out a license for each invocation of Gurobi in a job---which may occur dozens or even hundreds of times---you should ensure that your program, whatever the language or computing environment used, only makes a single license checkout and reuses this license as required for the lifetime of the job.  This will improve your job's performance because contacting a remote license server is very costly in time; moreover, responsiveness of our license server for everyone using Gurobi will also improve.  Failure to use Gurobi carefully in this regard may ultimately result in random intermittent license checkout failures for all users.  If this happens, you will be contacted and asked to kill all your jobs until your program is fixed and tested to ensure the problem is resolved.   Some documentation on this subject for C++ programs may be found here, explaining how to create a single Gurobi environment which can then be used for all your models. Python users can consult this page, which discusses how to implement this same idea of using a single environment and thus a single license token with multiple models.   Other programs that call Gurobi, such as R, can also easily trigger the problem when run in parallel, especially when many simultaneous parallel jobs are submitted and/or run.

There are two other conditions that your jobs should satisfy to ensure the license server is not overloaded. The first is that all of your jobs running on all Alliance clusters are not consuming more than 1000 licenses since there are only 4096 license.  This maybe checked by logging into any cluster and issuing :
  module load gurobi
  gurobi_cl --tokens | grep $USER | wc -l  (should be < 1000)

The second condition is that each running gurobi job should be using just 1 license (less commonly 2). Assuming all of your Gurobi jobs are running on the cluster that you are logged into, the average license usage per jobs maybe checked by running:
  module load gurobi
  echo "$(gurobi_cl --tokens | grep $USER | wc -l) / $(squeue -h -r -u $USER -t running | wc -l)" | bc -l (should be <= 2)
If however you are running jobs on many clusters, then instead this modifed form of the previous command (which runs much slower) should be used :
  module load gurobi
  echo $(for n in $(gurobi_cl --tokens | grep $USER | awk "{print $1}"); do host $n; done | grep address | wc -l) / $(squeue -u $USER -h -t running -r | wc -l) | bc -l (should be <= 2)
Note that if you run either command on a cluster where there are no gurobi jobs running then a "Runtime error Divide by zero error" message will be output accordingly.

If you will be submitting many Gurobi jobs to the scheduler in a loop, the following sample script may be used to ensure the jobs start gradually instead of all at once.  Submitting jobs this way will in turn ensure licenses are checked out gradually rather than all at once and hence control the load imposed on our Gurobi license server.  The script uses the slurm dependency after option introduced in Advanced Job Submission.

 [l2(nibi):~] cat submit.sh
 i=1; jobid=$(sbatch --parsable --output=slurm-%j-$i.out script.sh)
 for i in {2..1000}; do
  jobid=$(sbatch --parsable --dependency=after:$jobid --output=slurm-%j-$i.out script.sh)
  [ "$?" -ne 0 ] && exit 1
 done

== Interactive allocations ==

===Gurobi command-line tools===

 [gra-login2:~] salloc --time=1:00:0 --cpus-per-task=8 --mem=1G --account=def-xyz
 [gra800:~] module load gurobi
 [gra800:~] gurobi_cl Record=1 Threads=8 Method=2 ResultFile=p0033.sol LogFile=p0033.log $GUROBI_HOME/examples/data/p0033.mps
 [gra800:~] gurobi_cl --help

===Gurobi interactive shell ===

 [gra-login2:~] salloc --time=1:00:0 --cpus-per-task=8 --mem=1G --account=def-xyz
 [gra800:~] module load gurobi
 [gra800:~] echo "Record 1" > gurobi.env    see *
 [gra800:~] gurobi.sh
 gurobi> m = read('/cvmfs/restricted.computecanada.ca/easybuild/software/2017/Core/gurobi/8.1.1/examples/data/glass4.mps')
 gurobi> m.Params.Threads = 8               see **
 gurobi> m.Params.Method = 2
 gurobi> m.Params.ResultFile = "glass4.sol"
 gurobi> m.Params.LogFile = "glass4.log"
 gurobi> m.optimize()
 gurobi> m.write('glass4.lp')
 gurobi> m.status                           see ***
 gurobi> m.runtime                          see ****
 gurobi> help()

where
    * https://www.gurobi.com/documentation/8.1/refman/recording_api_calls.html
   ** https://www.gurobi.com/documentation/8.1/refman/parameter_descriptions.html
  *** https://www.gurobi.com/documentation/8.1/refman/optimization_status_codes.html
 **** https://www.gurobi.com/documentation/8.1/refman/attributes.html

===Replaying API calls===
You can record API calls and repeat them with

 [gra800:~] gurobi_cl recording000.grbr

Reference: https://www.gurobi.com/documentation/8.1/refman/recording_api_calls.html

== Cluster batch job submission ==

Once a Slurm script has been prepared for a Gurobi problem, it can be submitted to the queue by running the sbatch script-name.sh command.  The jobs status in the queue can then be checked by running the sq command.  The following Slurm scripts demonstrate solving 2 problems provided in the  examples directory of each Gurobi module.

=== Data example ===

The following Slurm script utilizes the Gurobi command-line interface to solve a simple coin production model written in LP format.  The last line demonstrates how parameters can be passed directly to the Gurobi command-line tool "gurobi_cl" using simple command line arguments.  For help choosing values see the Performance and Parameters and Algorithms and Search sections found in the Gurobi Knowledge Base and the online Gurobi documentation.

=== Python example ===

This is an example Slurm script for solving a simple facility location model with Gurobi Python.  The example shows how to set the threads  parameter equal to the number of cores allocated to a job by dynamically generating a gurobi.env file into the working directory when using the Gurobi python interface.  This must be done for each submitted job, otherwise Gurobi will (by default) start as many execute threads as there are physical cores on the compute node, potentially slowing down the job and negatively impacting other user jobs running on the same node.

== Using Gurobi in Python virtual environments ==

Gurobi brings it's own version of Python which does not contain any 3rd-party Python packages except Gurobi.   In order to use Gurobi together with popular Python packages like NumPy, Matplotlib, Pandas and others, we need to create a virtual Python environment in which we can install both gurobipy and for example pandas.  Before we start, we need to decide which combination of versions for Gurobi and Python to use.  Following is a list of the Python versions supported by the major Gurobi versions installed in the previous through current standard environments (StdEnv):

 [name@server ~] module load StdEnv/2016; module load gurobi/8.1.1; cd $EBROOTGUROBI/lib; ls -d python*
 python2.7  python2.7_utf16  python2.7_utf32  python3.5_utf32  python3.6_utf32  python3.7_utf32

 [name@server ~] module load StdEnv/2020; module load gurobi/9.5.2; cd $EBROOTGUROBI/lib; ls -d python*
 python2.7_utf16  python2.7_utf32  python3.10_utf32  python3.7  python3.7_utf32  python3.8_utf32  python3.9_utf32

 [name@server ~] module load StdEnv/2023; module load gurobi/10.0.3; cd $EBROOTGUROBI/lib; ls -d python*
 python3.10_utf32  python3.11_utf32  python3.7  python3.7_utf32  python3.8_utf32  python3.9_utf32

 [name@server ~] module load StdEnv/2023; module load gurobi/11.0.1; cd $EBROOTGUROBI/lib; ls -d python*
 python3.11

=== Installing Gurobi for Python ===

As mentioned near the end of this official document How do I install Gurobi for Python?, the previously recommended method for installing Gurobi for Python with setup.py has been deprecated to only be usable with Gurobi 10 versions (and older).  Section Gurobi 11 versions (and newer) below shows how to simultaneously download a compatible binary wheel from pypi.org and convert it into a format usable with the newly recommended command to install Gurobi for Python.

=== Gurobi versions 10.0.3 (and older) ===

The following steps need to be done once per system and are usable with StdEnv/2023 and older.  First, load the modules to create the virtual environment and activate it:

Now install any Python packages you want to use, in this case pandas:

Next, install gurobipy in the environment.  Note that as of StdEnv/2023 the installation can no longer be done under $EBROOTGUROBI using the command python setup.py build --build-base /tmp/${USER} install since a fatal error (error: could not create 'gurobipy.egg-info': Read-only file system) will occur.  Instead, the required files need to be copied elsewhere (such as /tmp/$USER) and the installation made from there, for example:

=== Gurobi versions 11.0.0 (and newer) ===

Once again, the following steps need to be done once per system and are usable with StdEnv/2023 and older.  First load the modules to create the virtual environment and activate it.  Version 11.0.0 is skipped since it has been observed to seg fault in at least one example versus Version 11.0.1 which runs smoothly.

As before, install any needed Python packages.  Since the following matrix example requires numpy, we install the pandas package:

Next install gurobipy into the environment. As mentioned above and in [article] the use of setup.py to install Gurobi for python is deprecated starting with Gurobi 11.  Both pip and conda are given as alternatives; however, since conda should not be used on our systems, the pip approach will be demonstrated here. The installation of gurobipy is slightly complicated since our Linux systems are set up with gentoo prefix.  As a result neither A) the recommended command to download and install the gurobipy extension from the public PyPI server pip install gurobipy==11.0.1 mentioned in the article line or B) the offline command to install the wheel with python -m pip install --find-links  --no-index gurobipy, will work.  Instead, we have prepared a script to download and simultaneously convert the existing wheel into a usable format with a new name.  There is one caveat; for each new Gurobi version, you must go into https://pypi.org/project/gurobipy/11.0.1/#history and click on the desired version followed by the Download files button located in the menu on the left.  Finally, click to copy the https link for the wheel file (named gurobipy-11.0.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl in the case of Gurobi 11.0.1) and paste it as the --url argument as shown below :

=== Running Gurobi in the environment ===

Once created our Gurobi environment can be activated and used at any time.  To demonstrate this we also load gurobi (so $EBROOTGUROBI is defined) and scipy-stack (so scipy is available).  Both are required to run the matrix example (along with numpy that was already installed into our  environment with pip in a previous step above via pandas).

Python scripts, such as the examples provided with the gurobi module can now be run (within the virtual environment) using python :

Likewise custom python scripts such as the following can be run as jobs in the queue by writing slurm scripts that load your virtual environment.

Submit your script to the queue by running sbatch my_slurm_script.sh as per usual :

Further information regarding how to create and use python virtual environments within job scripts can be found  here.

== Using Gurobi with Java ==

To use Gurobi with Java, you will also need to load a Java module and add an option to your Java command in order to allow the Java virtual environment to find the Gurobi libraries. A sample job script is below:

== Using Gurobi with Jupyter notebooks ==

Various topics can be found by visiting Resources, then clicking Code and Modeling Examples and finally Optimization with Python – Jupyter Notebook Modeling Examples.  Alternatively visit support.gurobi.com and search on Jupyter Notebooks.

A demo case of using Gurobi with Jupyter notebooks on our systems can be found in this video recording, i.e. at time 38:28.

== Cite Gurobi ==

How do I cite Gurobi software for an academic publication?

== Getting Help ==

The Gurobi general Help Center is located here.
Gurobot a new Gurobi AI Agent is available here.
The official online Gurobi documentation is here.
For help using Gurobi on the Alliance  submit a ticket.