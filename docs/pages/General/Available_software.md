---
title: "Available software/en"
url: "https://docs.alliancecan.ca/wiki/Available_software/en"
category: "General"
last_modified: "2026-11-08T16:20:56Z"
page_id: 2490
display_title: "Available software"
---

__FORCETOC__

A current list of the software available on our national systems is below. This list changes frequently as new software is added. You can request the installation or updating of a particular program or library by contacting technical support. If you wish to use our software environment on your own system, please see Accessing CVMFS.

==Notes==
Except for basic system programs, you access most software by loading a module. See Using modules for more on how to use the Lmod module system. Note that some prerequisite modules are loaded by default.

Here are a few things to know about the available software:
* Most Python modules are not installed as (Lmod) modules. They are instead provided as binary wheels, stored on our systems under /cvmfs/soft.computecanada.ca/custom/python/wheelhouse/. One such package is TensorFlow. For instructions on how to install or list Python packages, see the Python page.
* Similarly, most R or Perl packages are not installed either. We recommend installing them in your personal or group file space. See the R and Perl pages for instructions on how to do so.
* A page discusses symbolic algebra software like Mathematica and Sage.
* Note that Docker is not available on our clusters but Apptainer is available by loading the module apptainer. Docker containers can be converted to Apptainer as discussed here.
* Some of the software packages listed below are not immediately usable because they require you to have a license. You may need to be granted access to them by us. Attempting to load the module for one of these will give you instructions on what to do to obtain access.
* While the vast majority of the software packages below are accessible on all our servers, a few are only available at one site or another due to licensing restrictions. See  Site-specific software below.
* The packages listed below are available in one or more standard software environments.  In rare circumstances it may be necessary to load a different standard environment (StdEnv) to access a particular version of a particular package.  For more on this please read Standard software environments.
* Many packages related to the operating system, such as Autotools, Make, Git, and others, are not installed as modules but are part of the default environment. These are not listed below.

==List of globally-installed modules==
The table below lists software for which an environment module has been installed on our systems. In simple cases, the module name listed in the Module column can be used with the module load command to configure your environment.  In more complicated cases, some prerequisite modules may also need to be loaded. Click on the corresponding [Expand] link in the Description column for a list of prerequisites and brief notes about the software.  If more extensive documentation about a package is available, there will be a link in the Documentation column.  Click the double arrows in the column heading to sort in ascending or descending order for a given column. In particular, sorting by software type might be of interest. The Type column shows the software tagged as: ai (artificial intelligence), bio (biology, bioinformatics), chem (chemistry), geo (earth sciences), io (input/output), math (mathematics), mpi (MPI), phys (physics and engineering), tools (languages and libraries), vis (visualization).

Software for legacy architectures can be found on their respective pages: AVX and SSE3.

== Site-specific software ==
Most application software is installed in CVMFS, a distributed file system which makes central management of the many packages easier.
Certain packages, however, are not installed in CVMFS but are installed only at some sites, or are installed separately at each site.
This is usually due to license restrictions on the package in question.
Such packages are listed in the following table.

List of software installed locally

Module          	Type	Documentation	Cluster	Description
adf/2016.106    	chem	ADF          	Nibi   	Amsterdam Density Functional Modeling Suite, computational chemistry software
adf/2017.207    	chem	ADF          	Nibi   	Amsterdam Density Functional Modeling Suite, computational chemistry software
adf/2018.104    	chem	ADF          	Nibi   	Amsterdam Density Functional Modeling Suite, computational chemistry software
adf/2019.305    	chem	ADF          	Nibi   	Amsterdam Density Functional Modeling Suite, computational chemistry software
ams/2020.102    	chem	AMS          	Nibi   	Amsterdam Modeling Suite products
amber/16        	chem	AMBER        	Nibi   	The Amber Molecular Dynamics Package
dirac/16.0      	phys	             	Fir    	The DIRAC program computes molecular properties using relativistic quantum chemical methods. Homepage: http://diracprogram.org
dirac/17.0      	phys	             	Fir    	The DIRAC program computes molecular properties using relativistic quantum chemical methods. Homepage: http://diracprogram.org
gaussian/g03.d01	chem	Gaussian     	Nibi   	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g09.e01	chem	Gaussian     	Nibi   	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g16.b01	chem	Gaussian     	Nibi   	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g16.c01	chem	Gaussian     	Nibi   	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g03.d01	chem	Gaussian     	Fir    	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g09.b01	chem	Gaussian     	Fir    	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g09.e01	chem	Gaussian     	Fir    	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g16.a03	chem	Gaussian     	Fir    	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g16.b01	chem	Gaussian     	Fir    	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/
gaussian/g16.c01	chem	Gaussian     	Fir    	Gaussian is a general-purpose computational chemistry software package. Homepage: http://gaussian.com/