---
title: "Firedrake/en"
url: "https://docs.alliancecan.ca/wiki/Firedrake/en"
category: "General"
last_modified: "2026-08-24T16:29:19Z"
page_id: 34614
display_title: "Firedrake"
---

Firedrake is an automated system for the solution of partial differential equations using the finite element method (FEM).

Please note that every release of Firedrake requires a specific version of PETSc, several other modules and Python wheels.

= Installation =

Please note that all modules must be loaded before creating and/or activating the Python virtualenv.

3.11.0  pytools2026.1.1  immutabledict
|pip install --no-index  firedrake[check]2026.4.1
}}
The above has been tested with python/3.14, python/3.13, python/3.12 and python/3.11.

2025.2.2  immutabledict
|pip install --no-index  firedrake[check]2025.4.2
}}
The above has been tested with both python/3.13 as well as python/3.12.

= Running jobs =

The above has been tested with python/3.14, python/3.13, python/3.12 and python/3.11.

The above has been tested with both python/3.13 as well as python/3.12.

= Optional dependencies =
Firedrake has a number of optional dependencies that can be installed into the virtualenv:

* SLEPc and slepc4py are part of the petsc module and always available.
* netgen: We provide precompiled wheels for ngsPETSc and netgen_mesher.
* PyTorch: We provide precompiled wheels for torch.
* Jax: We provide precompiled wheels for jax.
* VTK: The module vtk/9.4.2 is compatible with python/3.14, python/3.13, python/3.12 and python/3.11.