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
These configurations assume that their is a relative directory ./target
If you are starting a docker image from a directory, make sure there is a subdirectroy called target. That subdirectory will be mounted in the image, and it is the place where the outputs created by this program are saved on disk, even after the container that created them is gone.

````
$ u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir target/test_case_1 --random-seed 123456789
$ u3etas_launcher.sh target/test_case_1/config.json

<pre>
[19:09:12.971 (main)]: Simulation start time (epoch milliseconds): 1562383194040
[19:09:12.984 (main)]: Simulation start date: 2019/07/06 03:19:54 UTC
[19:09:13.013 (main)]: Setting maximum point source mag: 10.0
[19:09:13.877 (main)]: Simulation name: ComCat M7.1 (ci38457511), ShakeMap Surfaces
[19:09:13.991 (main)]: determining random seeds from input seed=123456789
[19:09:14.173 (main)]: max mem MB: 12288
[19:09:14.175 (main)]: max threads calculated from max mem & available procs: 2
[19:09:14.230 (main)]: starting 10 simulations with 2 threads
</pre>

<pre>
[19:14:12.850 (pool-1-thread-2)]: completed 8 (5447 ruptures)
Memory after loop:
        in use memory: 8,045,007
        free memory: 4,535,856
        allocated memory: 12,580,864
        max memory: 12,582,912
        total free memory: 4,537,904
Memory at end of simultation
        in use memory: 8,045,007
        free memory: 4,535,856
        allocated memory: 12,580,864
        max memory: 12,582,912
        total free memory: 4,537,904
[19:14:24.837 (pool-1-thread-1)]: completed 9 (4443 ruptures)
[19:14:24.888 (main)]: done with 10 simulations in 5.177117 minute
</pre>
Or another run
<pre>
[23:07:27.979 (pool-1-thread-2)]: completed 9 (4443 ruptures)
[23:07:28.148 (main)]: done with 10 simulations in 7.6860166 minutes
</pre>

$ u3etas_plot_generator.sh target/test_case_1/config.json
<pre>
(scec-dev) scecuser@d63902550175:~$ u3etas_plot_generator.sh target/test_case_1/config.json
ETAS_MEM_GB is not set, will automatically detect maximum memory as 80% of total system memory
     will use up to 12 GB of memory
Checking for updates to OpenSHA. You can disable these checks by setting the environmental variable ETAS_JAR_DISABLE_UPDATE=1
Checking for git updates in /home/scecuser/ucerf3-etas-launcher/opensha/git/opensha
        On branch: etas-launcher-stable
Fetching origin
Up-to-date
Path ('${ETAS_LAUNCHER}/inputs/cache_fm3p1_ba') contains environmental variable ('ETAS_LAUNCHER')
        replacing '${ETAS_LAUNCHER}' with '/home/scecuser/ucerf3-etas-launcher': /home/scecuser/ucerf3-etas-launcher/inputs/cache_fm3p1_ba
Catalogs file/dir not specififed, searching for catalogs...
Using results dir: /home/scecuser/target/test_case_1/results
[19:16:04.335 (main)]: Simulation start time (epoch milliseconds): 1562383194040
[19:16:04.353 (main)]: Simulation start date: 2019/07/06 03:19:54 UTC
[19:16:04.394 (main)]: Setting maximum point source mag: 10.0
[19:16:06.788 (main)]: Simulation name: ComCat M7.1 (ci38457511), ShakeMap Surfaces
[19:16:06.875 (main)]: determining random seeds from input seed=123456789
Has any triggers? true  Has non-hist triggers? true     Annualize MFD? false
ComCat map grid spacing: 0.02 for minSpan=1.1924393
Current duration from start time: 4.64065
Max comcat compare duration: 4.64065
https://earthquake.usgs.gov/fdsnws/event/1/query?endtime=2024-02-25T03:16:08.179Z&format=geojson&limit=20000&maxdepth=24.000&maxlatitude=36.33719&maxlongitude=-116.84279&mindepth=-10.000&minlatitude=35.14475&minlongitude=-118.26629&minmagnitude=2.500&orderby=time&starttime=2019-07-06T03:19:54.040Z
Count of events received = 2865
Count of events after filtering = 2835
Events filtered due to conversion = 0, location = 30, id = 0
Total number of events returned = 2835
Min ComCat mag: 2.5
[19:16:14.226 (main)]: Loading a new Fault System Solution from /home/scecuser/ucerf3-etas-launcher/inputs/2013_05_10-ucerf3p3-production-10runs_COMPOUND_SOL_FM3_1_SpatSeisU3_MEAN_BRANCH_AVG_SOL.zip
</pre>

````
# Use Case 2:
This is a single node example of UCERF3-ETAS simulations. 
This contains a slurm script that is configured to run on a single node SDSC Expanse. This example produces 10000 catalogs.
It took ~3.2 hours on a single node on SDSC Expanses (w/ 128 cores and 256G Ram) and it uses inputs a Java threads and memory requirements (10GB per cpu) at starttime. 
A threaded calculation, with too little RAM/thread (cpu) may start up, generate some catalogs, then exits on out of memory. On expanse this has happened when trying to run with less than 8GB/thread.
When both the catalog generations and the plotting has run, the results are:
<pre>
(base) [ux454496@login02 ucerf3_etas_test_cases]$ du -sh test_2_ridgecrest_m71_results/
6.3G    test_2_ridgecrest_m71_results/
</pre>
        
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
