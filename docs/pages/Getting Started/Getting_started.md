---
title: "Getting started/en"
url: "https://docs.alliancecan.ca/wiki/Getting_started/en"
category: "Getting Started"
last_modified: "2026-06-11T14:48:01Z"
page_id: 635
display_title: "Getting started"
---

==What do you want to do?==
* If you don't already have an account, see
** Apply for a CCDB account
** Multifactor authentication
** Frequently Asked Questions about the CCDB
* If you are an experienced HPC user and are ready to log into a cluster, you probably want to know
**  what systems are available;
** what software is available;
** how environment modules work;
** how to submit jobs;
** how filesystems are organized.
* If you are new to HPC, you can
** read about how to connect to our HPC systems with SSH;
** read an introduction to Linux systems;
** read about how to transfer files  to and from our systems;
* If you want to know which software and hardware are available for a specific discipline, a series of discipline guides is in preparation. At this time, you can consult the guides on
** AI and Machine Learning
** Bioinformatics
** Biomolecular simulation
** Computational chemistry
** Computational fluid dynamics (CFD)
** Geographic information systems (GIS)
** Visualization
* If you have hundreds of gigabytes of data to move across the network, read about the Globus file transfer service.
* Python users can learn how to install modules in a virtual environment.
* R users can learn how to install packages.
* If you want to experiment with software that doesn’t run well on our HPC clusters, read about our cloud resources.

For any other questions, you might try the Search box in the upper right corner of this page, the main page for our technical documentation or contact us by email.

==Username and password==
Your password to log in to all new national systems is the same one you use to log into CCDB. Your username will be displayed at the top of the page once you've logged in.

==What systems are available?==

You must request access to one or more of our systems: Arbutus, Fir, Narval, Nibi, Rorqual, and Trillium.

* Arbutus is a cloud site, which allows users to launch and customize virtual machines. See Cloud for how to obtain access to Arbutus.

* Fir, Narval, Nibi, and Rorqual are general-purpose clusters (or supercomputers) composed of a variety of nodes including large memory nodes and nodes with accelerators such as GPUs.  You can log into any of these using SSH. A /home directory will be automatically created for you the first time you log in.

* Trillium is a homogeneous cluster (or supercomputer) designed for large parallel jobs (>1000 cores).

In this documentation, we generally use the term “cluster” instead of “supercomputer” since it better reflects the architecture of our systems: A large number of individual computers, or “nodes”, linked together as a unit, or “cluster”.

==What system should I use?==
This question is hard to answer because of the range of needs we serve and the wide variety of resources we have available. If the descriptions above are insufficient, contact our technical support.

In order to identify the best resource to use, we may ask specific questions, such as:
* What software do you want to use?
** Does the software require a commercial license?
** Can the software be used non-interactively? That is, can it be controlled from a file prepared prior to its execution rather than through a graphical interface?
** Can it run on the Linux operating system?
* How much memory, time, computing power, accelerators, storage, network bandwidth and so forth—are required by a typical job? Rough estimates are fine.
* How frequently will you need to run this type of job?

You may know the answer to these questions or not. If you do not, our technical support team is there to help you find the answers. They will then be able to direct you to the most appropriate resources for your needs.

==What training is available?==

Most workshops are organized by the Alliance's regional partners; both online and in-person training opportunities exist on a wide variety of subjects and at different levels of sophistication. We invite you to consult the following regional training calendars and websites for more information,
* WestDRI (Western Canada Research Computing covering both BC and the Prairies regions)
** Training Materials website: click on Upcoming sessions or browse the menu at the top for recorded webinars
** UAlberta ARC Bootcamp: videos of previous sessions available
* SHARCNET
** Training Events Calendar
** YouTube Channel
** Online Workshops
* SciNet
** SciNet Education Site
** SciNet YouTube Channel
* Calcul Québec
** Workshops
** Training information
* ACENET
** Training information
** ACENET YouTube Channel
See the complete and merged list of upcoming training events on Explora.