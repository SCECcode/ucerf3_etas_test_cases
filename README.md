# ucerf3_etas_use_cases

# Description
This directory contains three use case examples for UCERF3-ETAS for Quakeworx.

# Test Case 1:
The first test case is an 10 year ETAS forecast using the Ridgecreset earthquake catalog leading up to the M7.1. The default benchmark is 10,000 catalogs, but that might take 8 hours or longer on a laptop.

# Test Case 2:
This is a single node example of UCERF3-ETAS simulations with 10,000 catalogs. The config.json configuration file is generated using the same input parameters as test case 1. However, this test case is configured to run on an Expanse compute node, and not on a laptop. The many cores (128) on an Expanse node should reduce the time required to generate the catalogs as compared to a laptop. 

## Outputs
When both the catalog generations and the plotting has run, the results are:
<pre>
(base) [ux454496@login02 ucerf3_etas_test_cases]$ du -sh test_2_ridgecrest_m71_results/
6.3G    test_2_ridgecrest_m71_results/
</pre>
        
# Test Case 3:
This is a multi-node example of UCERF3-ETAS. This contains a slurm script that is configured to run on multiple nodes on SDSC Expanse. This configuration requires installation of Java MPI library on the Expanse Java path. The default configuration generates 10000 catalogs and it will complete within 1 hour on 14 nodes on SDSC Expanse. It is multi-threaded and requires a Java-MPI libraries.

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
