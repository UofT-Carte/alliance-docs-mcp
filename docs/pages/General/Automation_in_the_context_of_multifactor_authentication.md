---
title: "Automation in the context of multifactor authentication/en"
url: "https://docs.alliancecan.ca/wiki/Automation_in_the_context_of_multifactor_authentication/en"
category: "General"
last_modified: "2026-05-13T14:51:30Z"
page_id: 24806
display_title: "Automation in the context of multifactor authentication"
---

An automated workflow which involves some outside machine connecting to a cluster without human intervention cannot make use of a second authentication factor. In order to execute such a workflow now that MFA is a requirement, you must request access to an automation node. An automation node does not require the use of a second factor, but is much more limited than a regular login node in terms of the type of authentication it accepts and the types of actions that it can be used to perform.

= Increased security measures =
== Available only by request ==
If you need to make use of an automated workflow for your research, contact our technical support and request access to an automation node. When contacting us, please explain in detail the type of automation you intend to use. Tell us what commands will be executed and what tools or libraries you will be using to manage the automation.

== Available only through constrained SSH keys ==
The only accepted means of authentication for the automation nodes is through SSH keys uploaded to the CCDB. SSH keys written in your .ssh/authorized_keys file are not accepted. Please follow the rule of 'one SSH key per use.' Do not reuse the key for interactive login. Instead, generate a new SSH key specifically for your automation workflow. In addition, the SSH keys must obey the following constraints.

=== restrict ===
This constraint disables port forwarding, agent forwarding, and X11 forwarding. It also disables the pseudo teletype (PTY), blocking most interactive workloads. This is required because these automation nodes are not intended to be used to start long-running or interactive processes. Regular login nodes must be used instead.

=== from="pattern-list" ===
This constraint specifies that the key can only be used from IP addresses that match the patterns. This is to ensure that this key is not used from computers other than the ones intended. The pattern list must include only IP addresses that fully specify at least the network class, the network, and the subnet, which are the first three elements of an IP address, for example, x.y.*.* would not be accepted, but x.y.z.* would be accepted. Also, the IP address must be a public IP address; thus anything like 10.0.0.0 – 10.255.255.255, 172.16.0.0 – 172.31.255.255 and 192.168.0.0 – 192.168.255.255 is incorrect. You can use a site like What Is My IP Address? or the shell command curl ifconfig.me to learn your public IP address.

=== command="COMMAND" ===
This constraint forces the command COMMAND to be executed when the connection is established. This is so that you may restrict which commands can be used with this key.

Any path in the COMMAND may be absolute (that is from /) or relative to the home directory.

== Convenience wrapper scripts to use for command= ==
command constraints can specify any command, but they are most useful when using a wrapper script which will accept or reject commands based on which command is being called. You can write your own script, but for convenience, we provide a number of such scripts which allow common actions. These scripts are defined in this git repository.

* /cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/transfer_commands.sh allows only file transfers, such as scp, sftp or rsync.
* /cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/archiving_commands.sh allows commands to archive files, such as gzip, tar or dar.
* /cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/file_commands.sh allows commands to manipulate files, such as mv, cp or rm.
* /cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/git_commands.sh allows the git command.
* /cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/slurm_commands.sh allows some Slurm commands, such as squeue, sbatch.
* /cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/allowed_commands.sh allows all of the above.

== Examples of accepted SSH keys ==
Accepted SSH keys must include all 3 of the above constraints to be accepted. Here are examples of SSH keys that would be accepted:
For example, the following key would be accepted, and could only be used for transferring files (through scp, sftp or rsync for example):

restrict,from="216.18.209.*",command="/cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/transfer_commands.sh" ssh-ed25519 AAAAC3NzaC1lZDI1NTE6AACAIExK9iTTDGsyqKKzduA46DvIJ9oFKZ/WN5memqG9Invw

while this one would only allow Slurm commands (squeue, scancel, sbatch, scontrol, sq):

restrict,from="216.18.209.*",command="/cvmfs/soft.computecanada.ca/custom/bin/computecanada/allowed_commands/slurm_commands.sh" ssh-ed25519 AAAAC3NzaC1lZDI1NTE6AACAIExK9iTTDGsyqKKzduA46DvIJ9oFKZ/WN5memqG9Invw

= Automation nodes for each cluster =
Here is the hostname of the node to be used for unattended connections on each cluster:
* Fir: robot.fir.alliancecan.ca
* Narval: robot.narval.alliancecan.ca
* Nibi: robot.nibi.alliancecan.ca
* Rorqual: robot.rorqual.alliancecan.ca
* tamIA: robot.tamia.ecpia.ca
* Trillium: robot2.scinet.utoronto.ca

= Using the right key =
If you have multiple keys on your computer, you need to be careful to use the correct key. This is typically done by passing parameters to the command you are using. Below are a few examples.

With ssh or scp:

With rsync:

It's often much more convenient to put these parameters into your ~/.ssh/config file, so they get picked up by any ssh client invocation.  For instance:
 host robot
  hostname robot.cluster.alliancecan.ca
  user myrobot
  identityfile ~/.ssh/my-robot-key
  identitiesonly yes
  requesttty no

this means that the following kinds of commands will do what you want:

= IPv4 vs IPv6 issue =

When connecting to a automation node the SSH client on your computer may choose to use the IPv6 addressing over the older IPv4.
This seems to be more probable in a Windows environment.
If this is the case you have to make sure that the IP address mask you put in the restrict,from= field of the key
matches the type your computer will be using when connecting to the node.

You can check your addresses using this web site: https://test-ipv6.com/ .

* An IPv4 address could look like 199.241.166.5.
* An IPv6 address could look like 2620:123:7002:4::5.

The possible problem is that if you put the IPv4 address mask, 199.241.166.* into the CCDB SSH key, and
your SSH client will be connecting to the automation node using IPv6 address, the source address will not match the mask in the key
and the key will not be accepted by the automation node.

=== How to identify the problem ===

If you are having difficulties to make the SSH connection to an automation node work,
try this test command:
 ssh -i ~/.ssh/automation_key -vvv username@robot.rorqual.alliancecan.ca "ls -l"

This tries to connect to the automation node at Rorqual and execute the ls -l command
using the ~/.ssh/automation_key SSH key.
Then it prints the list of files in your home directory on Rorqual to screen.

This command will produce a lot of debug output due to the -vvv option ("Very Very Verbose").
Look for the Connecting to... message there.
If it says something like this:
 debug1: Connecting to robot.rorqual.alliancecan.ca [199.241.166.5] port 22.

it means that IPv4 is being used.
If the message is similar to
 debug1: Connecting to robot.rorqual.alliancecan.ca [2620:123:7002:4::5] port 22.

then IPv6 is being used to make the connection.

=== Possible solutions ===

* You can make the SSH client to explicitly use either IPv4 or IPv6 using the -4 and -6 options, respectively, to match the format you used for the key in CCDB.

* You can try using an IP address instead of the name to point to the automation node. Using Rorqual example, try using the
: ssh -i ~/.ssh/automation_key -vvv username@132.219.138.79 "ls -l"
: instead, to force SSH to use the IPv4 addresses.

* You can try to disable the IPv6 addressing for your computer, to make sure that only IPv4 is used.
: Currently, there should not be any negative impact on your computer. However, Microsoft does not recommend this, and this should be your last resort method, if nothing else works.
: How to disable IPv6 will depend on your operating system.

= Automation using Python and Paramiko =

If you are using the Paramiko Python module to automate your workflow, this is how you can make it work with the automation nodes:

# ====================================================================================================
#! /usr/bin/env python3
# ====================================================================================================
import os
import paramiko
# ====================================================================================================

key = paramiko.Ed25519Key.from_private_key_file("/home/username/.ssh/cc_allowed")

user = "username"
host = "robot.rorqual.alliancecan.ca"

ssh = paramiko.SSHClient()

# If the host is not known, it is OK.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=host, username=user, pkey=key)

cmd = "ls -l"
stdin, stdout, stderr = ssh.exec_command(cmd)

print("".join(stdout.readlines()))

ssh.close()
# ====================================================================================================

This code connects to the automation node on Rorqual using an key specified in CCDB and
executes the ls -l command to get the list of files.
Then prints the list to the screen.

Note that it is important to install Paramiko with the
 $ pip install paramiko[all]

command. This will make sure that the support for the Ed25519 key type will also be installed.