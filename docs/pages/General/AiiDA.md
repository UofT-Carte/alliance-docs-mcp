---
title: "AiiDA"
url: "https://docs.alliancecan.ca/wiki/AiiDA"
category: "General"
last_modified: "2026-08-14T15:39:55Z"
page_id: 25587
display_title: "AiiDA"
---

= General =

AiiDA is an open-source Python tool to help researchers with automating and reproducing the complex workflows associated with modern computational science.  Numerous plugins exist to integrate AiiDA with common computational packages, particularly in the field of computational chemistry (see list of available plugins ).

Typically AiiDA will run on user's personal computer, a lab workstation, or a virtual machine in the cloud.  From there the user can have AiiDA submit jobs to clusters.

To do this, AiiDA must be able to make many SSH connections to the clusters autonomously.  This becomes a problem on clusters which require interactive Multifactor authentication (MFA).  The implementation of MFA support in AiiDA is still under development.

= Automation in the context of multifactor authentication =

To allow AiiDA and other similar software to connect to Alliance clusters without MFA, you have two options:

# Use the ControlMaster mechanism of ssh. This only requires you log into an Alliance cluster on the command line using SSH just once, with MFA.  Subsequent SSH commands will then reuse the existing connection.  This works well from Linux and MacOS computers, and is supported starting from version 2.7.0 of AiiDA.   This is the recommended method, since it is both simpler and more secure than the next method.
# If you have to connect from a Microsoft Windows computer, or if your workflow is tied to an older version of AiiDA than version 2.7.0, we have set up so-called automation nodes on each cluster.  These allow SSH connections without MFA, subject to restrictions, as explained below.

= Instructions on using AiiDA with Alliance clusters through Control Master =
These instructions assume the reader is already familiar with how AiiDA works.

On Linux and MacOS, you need to setup ControlMaster for the Alliance cluster to which you want to connect. You also need to make sure to setup the "Computer" in AiiDA using the "core.ssh_async" transport option ("Computer" is AiiDA's way of referring to the cluster).

Once this is set up, you must first connect with SSH to the cluster on the command line in a terminal to setup the connection. You should keep that SSH session open to make sure the connection does not get broken.  You can then start AiiDA, which will reuse the SSH connection.

Important: the 2FA mechanism from the AiiDA documentation that uses short lived SSH keys, is not applicable on the Alliance clusters.

= Instructions on using AiiDA with Alliance clusters automation nodes =

These instructions assume the reader is already familiar with how AiiDA works. They should only be used if the Control Master mechanism above is not possible.

== Obtain access to automation nodes ==

Users need to submit a ticket requesting access to automation nodes, explaining why it is needed.

== Set up SSH key ==
The first step is to upload the public SSH key to enable access to Alliance clusters.  Generate this key on the machine which will be running AiiDA.

The uploaded key needs to specify the IP address that will be used to connect, as well as the working directory that AiiDA will be using (specified during AiiDA "computer setup" stage).  If the IP of the machine running AiiDA changes, the user will need to upload a key with updated IP address.

It also needs to specify the location of the aiida_commands.sh script that will be used to manage the connection (so change someusername to the actual username). The key given here is an example only, you should change it to the public key that you generated.

 restrict,from="206.158.1.23",command="/home/someusername/aiida_commands.sh /project/6000000/aiida_work_dir" ssh-ed25519 AAAAC3NzbC1lZKI1NTE5AABBIHyIW8dNHKpNae4jKjtIJW2LIagCPfHiT8yWSj/LXEvV

Make sure you have no extra unnecessary spaces in your uploaded ssh key.  The format must be exactly as given here, but you need to change /project/6000000/aiida_work_dir to the actual directory where you want to put your aiida files.

== Set up automation script ==

The above key will run every SSH command coming in with that key through the aiida_commands.sh script.  The user should download this script to the desired Alliance cluster, by running on that cluster:

 wget https://raw.githubusercontent.com/ComputeCanada/software-stack-custom/main/bin/computecanada/allowed_commands/aiida_commands.sh

The location should be the one specified in the SSH key.

The file should be given execute permission, and should be made non-writeable for added security.

 chmod u+x aiida_commands.sh
 chmod u-w aiida_commands.sh

This file should not be modified without consultation with Alliance staff.

== Set up computer and code to use in AiiDA ==

In AiiDA, set up a "computer" to use the desired cluster, using one of the  cluster automation nodes as hostname.  Specify the SSH key defined above as the one to be used.

== Setup on cluster ==

You may need to install the software you wish to run on the cluster.  Instructions will differ depending on which computational package you wish to use.  You may need to specify the location on the software when you create AiiDA "code".

Make sure the working directory specified when you created the "computer" in AiiDA to be used for connecting to the cluster exists.

Specify the default account for the jobs to run under, by adding to your .bashrc lines like (change someuser to the actual user name that matches the account you are running under)

 export SLURM_ACCOUNT=def-someuser
 export SBATCH_ACCOUNT=$SLURM_ACCOUNT

You may also need to add this line to your .bashrc in order to get the script working.

 source /etc/profile

== Debugging ==

The script has been tested for a basic AiiDA job, but it may run into trouble for more complicated workflows.  Please consult with Alliance staff if you run into any difficulties.