# ucerf3_etas_use_cases

# Description
This directory contains three use case examples for UCERF3-ETAS for Quakeworx.

# Use Case 1:
Single core example of UCERF3-ETAS simulations. This contains a Dockerfile that will build an simple Example of the UCERF3-ETAS simulations.This configuration creates 10 catalogs. This example can be run on a laptop computer.

# Use Case 2:
This is a single node example of UCERF3-ETAS simulations. This contains a slurm script that is configured to run on a single node SDSC Expanse. This example produces 10000 catalogs and it will take several hours on a multiple cores of a single node on SDSC. It is multi-threaded and it uses a Java-MPI library.

# Use Case 3:
This is a multi-node example of UCERF3-ETAS. This contains a slurm script that is configured to run on multiple nodes on SDSC Expanse. This example produces 10000 catalogs and it will complete within 1 hour on 14 nodes on SDSC Expanse. It is multi-threaded and requires a Java-MPI libraries.

# Software Support:
Software support for UCERF3-ETAS  is provided by that Southern California Earthquake Center (SCEC) Research Computing Group.
1. [UCERF3-ETAS Issues](https://github.com/SCECcode/ucerf3_etas_use_cases/issues)
2. Email Contact: software [at] scec [dot] org

# Contributing:
We welcome contributions to the Quakeworx Toolkit. Please contact us at software [at] scec [dot] org

# Credits:
+ Kevin Milner
+ Fabio Silva
+ Philip Maechling

# License:
SCEC's UCERF-ETAS and Quakeworx software is distributed under the BSD 3-Clause open-source license. 
