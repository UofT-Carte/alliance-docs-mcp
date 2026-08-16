---
title: "Debugging and profiling/en"
url: "https://docs.alliancecan.ca/wiki/Debugging_and_profiling/en"
category: "General"
last_modified: "2026-08-05T18:48:01Z"
page_id: 11634
display_title: "Debugging and profiling"
---

An important step in the software development process, particularly for compiled languages like Fortran and C/C++, concerns the use of a program called a debugger to detect and identify the origin of runtime errors (e.g. memory leaks, floating point exceptions and so forth) so that they can be eliminated. Once the program's correctness is assured, a further step is profiling the software. This involves the use of another software tool, a profiler, determine what percentage of the total execution time each section of the source code is responsible for when run with a representative test case. A profiler can give information like how many times a particular function is called, which other functions are calling it and how many milli-seconds of time each invocation of this function costs on average.

= Debugging on a cluster =

Debugging sessions should be conducted using an interactive job and not run on a login node. You have multiple options:

* With the Slurm command salloc .... See Interactive jobs for all the details.
* With a JupyterLab session. See the JupyterLab page for the connection details and the prebuilt applications.
* With a remote desktop session for visual profiling tools. See this section of JupyterLab or one of the two Quickstart guides for Open OnDemand for the instructions.

= Debugging and profiling tools=

Our national clusters offer a variety of debugging and profiling tools, both command line and those with a graphical user interface, whose use requires an X11 connection.

== GNU debugger (gdb) ==

Please see the  GDB page.

== PGI debugger (pgdb) ==
Please see the Pgdbg page.

== ARM debugger (ddt) ==

Please see the  ARM software page.

==GNU profiler (gprof) ==

Please see the  Gprof  page.

== Scalasca profiler (scalasca, scorep, cube) ==

Scalasca is an open source, GUI-driven parallel profiling tool set. It is currently available for gcc 9.3.0 and OpenMPI 4.0.3, with AVX2 or AVX512 architecture. Its environment can be loaded with:

module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 scalasca

The current version is 2.5. More information can be found in the 2.x user guide, which contains workflow examples here.

== PGI profiler (pgprof) ==
Please see the  Pgprof page.

== Nvidia command-line profiler (nvprof) ==
Please see the  nvprof page.

==Valgrind==

Please see the  Valgrind page.

= External references =

* Introduction to (Parallel) Performance from SciNet
* Code profiling on Graham, video, 54 minutes.