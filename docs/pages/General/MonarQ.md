---
title: "MonarQ/en"
url: "https://docs.alliancecan.ca/wiki/MonarQ/en"
category: "General"
last_modified: "2026-09-18T12:42:43Z"
page_id: 26558
display_title: "MonarQ"
---

Login node: https://monarq.calculquebec.ca
''

Monarq is currently undergoing maintenance and should be operational in February 2026. In the meantime, Calcul Québec can offer access to a similar but smaller machine, with 6 qubits.

Its name is inspired by the monarch butterfly, a symbol of evolution and migration. The capital Q denotes the quantum nature of the computer and its origins in Quebec. Acquisition of MonarQ was made possible with the support of the Ministère de l'Économie, de l'Innovation et de l'Énergie du Québec (MEIE) and Canada Economic Development (CED).

== Getting access to MonarQ ==

# To begin the process of getting access to MonarQ, complete this form. It can only be completed by the principal investigator.
# You must have an account with the Alliance in order to get access to MonarQ.
# Meet with our team to discuss the specifics of your project.
# Receive access to the MonarQ dashboard and generate your access token.
# To get started using MonarQ, see  Getting started below.

Contact our quantum team at quantum@calculquebec.ca if you have any questions or if you want to have a more general discussion before requesting access to MonarQ.

== Technical specifications ==

Like quantum processors available today, MonarQ operates in an environment where noise remains a significant factor. Performance metrics, updated at each calibration, are accessible via the Thunderhead portal which you will be able to use after being approved for access to MonarQ.

Among the metrics are:
* 24-qubit quantum processor
* Single-qubit gate: 99.8% fidelity with gate duration of 15ns
* Two-qubit gate: 95.6% fidelity with gate duration of 35ns
* Coherence time: 4-10μs (depending on state)
* Maximum circuit depth: approximately 350 for single-qubit gates and 115 for two-qubit gates

== Quantum computing software ==

There are several specialized software libraries for quantum computing and the development of quantum algorithms. These libraries allow you to build circuits that are executed on simulators that mimic the performance and results obtained on a quantum computer such as MonarQ. They can be used on all Alliance clusters.

* PennyLane, for Python commands
* Snowflurry, for Julia commands
* Qiskit, for Python commands

The quantum logic gates of the MonarQ processor are called through a Snowflurry software library written in Julia. Although MonarQ is natively compatible with Snowflurry, there is a PennyLane-Snowflurry plugin developed by Calcul Québec that allows you to execute circuits on MonarQ while benefiting from the features and development environment offered by PennyLane.

== Getting started ==
Prerequisites: Make sure you have access to MonarQ and that you have your login credentials (username, API token). If you have any questions, write to quantique@calculquebec.ca.

* Step 1: Connect to Narval
** MonarQ is only accessible from Narval, a Calcul Québec cluster. Narval is accessed from the login node narval.alliancecan.ca.
** For help connecting to Narval, see SSH.

* Step 2: Create the environment
** Create a Python virtual environment (3.11 or later) to use PennyLane and the PennyLane-CalculQuébec plugin. These are already installed on Narval so that you will only have to import the software libraries you want.

* Step 3: Configure your identifiers on MonarQ and define MonarQ as your device
** Open a Python .py file and import the required dependencies (in the following example, PennyLane and MonarqClient).
** Create a client with your identifiers. Your token is available through the Thunderhead portal. The host is https://monarq.calculquebec.ca.
** Create a PennyLane device with your client. You can also enter the number of qubits (wires) and the number of shots.
** For more information, see pennylane_calculquebec.

* Step 4: Create your circuit
** In the same Python file, you can now code your quantum circuit.

* Step 5: Execute your circuit from the scheduler
** The sbatch command is used to submit a task.

$ sbatch simple_job.sh
Submitted batch job 123456

The Slurm script is similar to

* The result is written to a file with a name starting with slurm-, followed by the task ID and the .out suffix, for example slurm-123456.out.
* The file contains the result in dictionary  {'000': 496, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 504}.
* For more information on submitting tasks on Narval, see Running jobs.

== FAQ ==
* Foire aux questions (FAQ)

== Other tools ==
* Quantum transpilation

== Applications ==
MonarQ is suited for computations requiring small quantities of high-fidelity qubits, making it an ideal tool to develop and test quantum algorithms. Other possible applications include modelling small quantum systems; testing new methods and techniques for quantum programming and error correction; and more generally, fundamental research in quantum computing.

== Technical support ==
For questions about our quantum services, write to quantum@calculquebec.ca.
Sessions on quantum computing and programming with MonarQ are listed here.