---
title: "Cloud/en"
url: "https://docs.alliancecan.ca/wiki/Cloud/en"
category: "General"
last_modified: "2026-10-08T17:51:01Z"
page_id: 538
display_title: "Cloud"
---

We offer Infrastructure as a Service that supports virtualization.

A user of the cloud will typically create or spin up one or more virtual machines (VMs or instances). He or she then logs into the VM with administrative privileges, installs any desired software, and runs the software applications needed. These applications could be as diverse as a CPU-intensive analysis of particle physics data, or a web service directed towards scholars of literature and the humanities. The advantage is that the user has complete control over the collection of installed software (the software stack). The disadvantage is that the user must have some degree of experience in installing software and otherwise managing a computer.

Virtual machines can be easily replicated. One can take a snapshot of a VM which can then be started again elsewhere. This makes it easy to replicate or scale up a service, and to recover from (for example) a power interruption.

If you can fit your work easily into the HPC batch submission workflow and environment (see What is a scheduler?) it is preferable to work outside the cloud, as there are more resources available for HPC and software is already configured and installed for many common needs. There are also tools like Apptainer to run custom software stacks inside containers within our HPC clusters.
If your need isn't served by Apptainer or HPC batch, then the cloud is your solution.

==Getting a cloud project==
* Review and understand the important role you are about to take on to safeguard your research and the shared cloud infrastructure.
* If you do not have an account with us, create one with these instructions.
* A project is an allocation of resources for creating VMs within a cloud.
* If you are a primary investigator (PI) with an active cloud resource allocation (see RAC) you should already have a project. See the sections below on using the cloud to get started. If not or if you are not sure please contact technical support.
* Otherwise go to the Alliance cloud project and RAS request form to
** request access to an existing project (see the section below for information you will need to supply)
** and if you are a PI you may also
*** request a new project with our Rapid Access Service (RAS),
*** or request an increase in quota of an existing project.

* Requests are typically processed within two business days.

===Preparing your request===
* When requesting access to an existing project, you will need to know the project name and which cloud it is on. See the section on projects for guidance on how to find the project name and the section about cloud systems for a list of our clouds. Requests for access must be confirmed by the PI owning the project.
* When requesting either a new project or an increase in quota for an existing project some justification, in the form of a few sentences, is required:
**why you need cloud resources,
**why an HPC cluster is not suitable,
**your plans for efficient usage of your resources,
**your plans for maintenance and security (refer to this page).
*A PI may own up to 3 projects, but the sum of all project quotas must be within the RAS allocation limits. A PI may have both compute and persistent cloud RAS allocations.

==Creating a virtual machine on the cloud infrastructure==
* The cloud quick start guide describes how to manually create your first VM.
* Review the glossary to learn definitions of common topics.
* Consider storage options best suited to your use case.
* See the troubleshooting guide for steps to deal with common issues in cloud computing.

==User responsibilities==
For each cloud project, you are responsible for
* Creating and managing your virtual machines
*Securing and patching software on your VM
*Defining security groups to allow access to your network
*Creating user accounts
*Following best practices
*Considering security issues
*Backing up your VMs

==Advanced topics==
More experienced users can
*Automatically create VMs,
*Describe your VM infrastructure as code using Terraform.
==Use cases==
More detailed instructions are available for some of the common cloud use cases, including
*Configure a data or web server
*Using vGPUs (standard shared GPU allocation) in the cloud
*Using PCI-e passthrough GPUs in the cloud
*Setting up GUI Desktop on a VM
*Using IPv6 in Arbutus cloud

==Cloud systems==
Your project will be on one of the following clouds:
* Béluga cloud
* Arbutus
* Legacy Arbutus
* Nibi cloud
* Cedar cloud
The details of the underlying hardware and OpenStack versions are described on the cloud resources page. The System status wiki page contains information about the current cloud status and future planned maintenance and upgrade activities.

==Support==
For questions about our cloud service, contact technical support.