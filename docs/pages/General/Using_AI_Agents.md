---
title: "Using AI Agents"
url: "https://docs.alliancecan.ca/wiki/Using_AI_Agents"
category: "General"
last_modified: "2026-09-04T23:51:09Z"
page_id: 34829
display_title: "Using AI Agents"
---

Artificial intelligence (AI) agents can help read and explain code, modify files, run commands, prepare job submission scripts, analyze logs, and support debugging. On a shared computing infrastructure, however, their use requires a clear distinction between the agent process, the compute resources, and the model service being used.

This page presents general technical principles for using AI agents on Alliance clusters. It does not constitute institutional endorsement of any particular product or provider.

Important: To date, the Alliance has not issued a general recommendation for or against the use of AI agents on its clusters. The topic is still under review. Positions specific to a site or regional partner should be distinguished from Alliance-wide policies.

== Understanding where an AI agent runs ==

At least two components should be distinguished:

* the agent client, which runs in the environment where the agent is launched;
* the language model, which may be provided locally or through an external service, depending on the configuration.

An agent launched under a user's account generally operates with the permissions granted to that account. Depending on its authorization mode, it may therefore read files, run commands, or prepare context to be sent to the model.

If the agent is launched on a login node, its process runs on that node. If it is launched within an interactive SLURM allocation, its process runs on the allocated compute node. This distinction is important for following high-performance computing best practices.

== Where should an AI agent run? ==

Location                                     	Recommended use                                                                        	Notes
Local workstation or virtual machine         	Often the simplest option for hosting the agent.                                       	The agent runs outside the cluster, and the user then connects to Alliance resources using the authorized SSH, MFA, and SLURM mechanisms.
Login node                                   	Limit use to very lightweight operations.                                              	Prolonged use or computationally expensive agent activity is not appropriate on a login node.
Compute node within an interactive allocation	Suitable for development, small tests, validation, and interactive debugging.          	Use remains subject to local policies and the network connectivity available from compute nodes.
SLURM batch job                              	Standard method for reproducible, long-running, or computationally expensive workloads.	The agent may help prepare or analyze the job, but computation is managed by SLURM.
Automation node                              	Depends on the site.                                                                   	At Calcul Québec, these nodes are intended for deterministic platforms fully controlled by the user; an AI agent does not meet this definition.

== Using AI agents with SLURM ==

Compute-intensive workloads must run on compute nodes through the scheduler. See Running jobs and What is a scheduler?.

For interactive use, first request an allocation, for example:

salloc \
  --account= \
  --time=01:00:00 \
  --cpus-per-task=2 \
  --mem=4G

Then open a shell within the allocation:

srun --pty bash

Verify that the session is running inside an allocation:

hostname
echo "$SLURM_JOB_ID"
echo "$SLURM_CPUS_PER_TASK"

For long-running or reproducible experiments, prefer a batch job submitted with sbatch. An agent can help prepare the script, but every #SBATCH directive should be reviewed by the user before submission.

Ending the session: exit the agent and the interactive shell when they are no longer needed, then verify that no unnecessary allocation remains active:

squeue -u "$USER"

== Security, privacy, and data protection ==

=== Sensitive data ===

Alliance general-purpose computing resources are not appropriate for storing sensitive data. Before using an AI agent, consult Data protection, privacy, and confidentiality as well as the requirements of your institution and project.

Using an AI agent does not change the classification of the data or the obligations that apply to it.

=== Permissions between users ===

An agent launched by another user does not automatically bypass filesystem permissions. Standard Unix access controls continue to apply.

The situation is different when a user launches an agent under their own account: the agent may then access resources that the account itself can read or modify, to the extent allowed by the agent's authorization mode.

Important distinction: “another user cannot read my files” and “my own agent can access files that my account can read” are two different questions.

=== Data sent to an external service ===

If the model is provided through an external service, some context required for processing may leave the local infrastructure, depending on the tool configuration.

Before using an agent:

* do not provide secrets, passwords, private keys, tokens, or MFA codes in a prompt;
* restrict the agent to the project directory required for the task;
* avoid exposing unrelated files;
* review requested permissions and proposed commands;
* verify the policies of the provider, institution, and project;
* do not use the agent with data whose conditions for external processing are not clearly established.

== Permissions and human oversight ==

The user remains responsible for the commands, modifications, and computations they authorize.

A cautious configuration should follow principles such as:

# explain planned actions before executing them;
# do not run compute-intensive workloads on login nodes;
# use SLURM for computational workloads;
# request confirmation before modifying files;
# request confirmation before installing software;
# request confirmation before submitting or cancelling jobs;
# never delete data without explicit approval;
# do not browse directories unrelated to the project;
# never display or modify credentials or secrets;
# summarize the actions performed.

== SSH, public keys, and multifactor authentication ==

SSH keys and multifactor authentication may correspond to separate authentication steps. An accepted public key does not mean that the MFA step should be bypassed or disabled.

See SSH, SSH Keys, Multifactor authentication, and Automation in the context of multifactor authentication.

When an agent or application wraps an SSH connection, verify that the tool can handle an interactive session and the MFA challenge. If a standard SSH connection works but the application integration fails, the problem may be related to how the application handles SSH interaction or the terminal.

To diagnose the connection from the same environment as the agent:

ssh -v @.alliancecan.ca

Never attach a private key, password, MFA code, or API token to a support ticket.

== Automation nodes ==

Rules for automation nodes may vary by site.

At Calcul Québec, the communicated position is that these nodes must be used by deterministic platforms fully controlled by the user. An AI agent is not considered to meet this definition. A persistent deployment of an agent on this type of node is therefore not appropriate at Calcul Québec.

Preferred architectures are instead:

* a local workstation or VM hosting the agent, with connections to the cluster through supported mechanisms;
* an interactive SLURM allocation for interactive testing on a compute node, when policies and connectivity allow it;
* SLURM batch jobs for reproducible or computationally expensive workloads.

== Best practices ==

* Do not use login nodes for computation or intensive agent activity.
* Use SLURM for CPU or GPU workloads.
* Restrict the agent to the project directory needed for the task.
* Maintain human oversight of modifications, installations, deletions, and job submissions.
* Never provide secrets to the agent or in a support ticket.
* Verify the applicable data rules before using an external model or service.
* Independently validate code, scientific results, and SLURM resources suggested by the agent.
* Document tool, library, and environment versions to support reproducibility.
* Close interactive allocations when they are no longer needed.

== Information to include in a support ticket ==

When reporting an issue related to an AI agent, provide, where possible:

* the cluster name;
* where the agent is running: local workstation, VM, login node, or compute node;
* the operating system and tool version;
* the SSH connection method being used;
* whether a SLURM allocation is active;
* the exact error message, with secrets removed;
* relevant output from read-only diagnostics;
* the observed difference between a standard SSH connection and the connection initiated by the agent, if applicable.

== See also ==

* Running jobs
* Best practices for job submission
* Data protection, privacy, and confidentiality
* Multifactor authentication
* Automation in the context of multifactor authentication
* SSH
* Getting started with Claude on Alliance clusters