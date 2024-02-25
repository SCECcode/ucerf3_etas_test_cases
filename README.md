# ucerf3_etas_use_cases

# Description
This directory contains three use case examples for UCERF3-ETAS for Quakeworx.

# Test Case 1:
The first test case is an 10 day ETAS forecast using the Ridgecreset earthquake catalog leading up to the M7.1.
Select a reduced number of alternative catalogs to minimize the computational load.
Perform the same calculation but for 100000 catalogs on Cluster.

Running this ETAS simulation catalog N=10 on a laptop is a first order test case for etas.
To implement this test case, rather than install OpenSHA natively on a laptop, we'll put ETAS into a Docker container, then run the container on a laptop, allowing it full use of 8 cores and 16GB Ram.
thread and memory specifications are defined as defaults.
This contains a Dockerfile that will build an simple Example of the UCERF3-ETAS simulations.This configuration creates 10 catalogs. This example can be run on a laptop computer.
To run the test case, start the docker image. Go to ucerf3_etas_test_cases/test_case_1

These are the three commands that should work in the container:
However, on the second one is required because the required config.json file has been created and can be run directory.
Also, the benchmark measured on Expanse will not to the plotting because it depends on external system response (opensha - server).
````
$ u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir ucerf3_etas_test_cases/test_case_1 --random-seed 123456789
$ u3etas_launcher.sh ucerf3_etas_test_cases/test_case_1/config.json
$ u3etas_plot_generator.sh ucerf3_etas_test_cases/test_case_1/config.json
````
# Use Case 2:
This is a single node example of UCERF3-ETAS simulations. 
This contains a slurm script that is configured to run on a single node SDSC Expanse. This example produces 10000 catalogs and it will take several hours on a multiple cores of a single node on SDSC. 
It uses a single Expanse Node (w/ 128 cores and 256G Ram) and it uses Java threads and memory requirements (10GB per cpu). A threaded calculation, with too little RAM/thread (cpu) may start up, generate some catalogs, then exits on out of memory. On expanse this has happened when trying to run with less than 8GB/thread.

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
