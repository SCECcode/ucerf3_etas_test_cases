# Test Case 1
This is a ucerf3 etas test case for a laptop scale computer using opensha code. OpenSha provides an ETAS simulation test case that generates ETAS catalogs for 10 years after the Ridgecrest M7.1 Main Shock. This can provide a performance test case for presumably speeding up as it runs on more cores. Current scale is 10,000 Catalog generation is the reference case. This calculation is expected to take 8 hour+ on a laptop. It can be computed in less time on multi-core and multi-node supercompters.

# Steps for running the tutorial UCERF3-ETAS simulation inside the Docker container
This initial test case is assume to run in a Docker subdirectory on a laptop. The subdirectory where this sceccode/ucerf3_jup image is started, should have a subdirectory called target. This subdirectory will be mounted in the container and will be the location for the results to be written, and then visible from both the container, and from the laptop after the container exists.

# Start as Juptyer lab
Run the Docker image and it will present a url on the screen. Post that url into a browser, and it presents the Jupyter Lab interface which includes a terminal window.

Open a terminal window in Jupyter lab.
<pre>
$ pwd
/home/scecuser
$ ls
miniconda3  target  ucerf3-etas-launcher  ucerf3_etas_test_cases
</pre>

From this home directory, run config builder, then run test_case_1 with the launcher. The outputs will be written to target/results.
````
* u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10000 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir target/comcat-ridgecrest-m7.1-example --random-seed 123456789
````
Then, from the same home directory:
````
* u3etas_launcher.sh target/comcat-ridgecrest-m7.1-example/config.json
````
Then plot the results as needed:
````
* u3etas_plot_generator.sh target/comcat-ridgecrest-m7.1-example/config.json
````

# Examples

Once you have defined a JSON ETAS configuration file, you can use the scripts in the sbin directory. More detailed information on these scripts is available in the README. Commands shown below assume that you have added the sbin direcotory to your PATH.

To run a set of ETAS simulations on a single machine (but possibly with multiple threads), use the u3etas_launcher.sh command:
* u3etas_launcher.sh [--threads <num-threads>] </path/to/etas_configuration.json>
* For example, to run ETAS simulations for a JSON file in the current directory named "config.json" with 3 threads:
* u3etas_launcher.sh --threads 3 config.json

# Storage Requirements

* After creating configuration file: 1.2M
* After running 10 simulation: 9.1M
* After generating all 10 plots: 40M

* After 1000 examples simulation: 922MB data storage
  
# Notes

Running this ETAS simulation catalog N=10 on a laptop is a first order test case for etas. Install OpenSHA into a Docker container, then run the container on a laptop, allowing it full use of 8 cores and 16GB Ram. This repo contains a Dockerfile that will build an simple Example of the UCERF3-ETAS simulations. This configuration creates 10 catalogs. This example can be run on a laptop computer. To run the test case, start the docker image. Go to ucerf3_etas_test_cases/test_case_1

These are the three commands that should work in the container:
````
$ u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir target/test_case_1 --random-seed 123456789
$ u3etas_launcher.sh target/test_case_1/config.json
$ u3etas_plot_generator.sh target/test_case_1/config.json
````
# Operating Notes
The second command is required. However the first command has been run and it has generated the the required config.json file. This ETAS Test Case will include to the plotting stages of the program, because the plotting scripts depend on external system response (opensha - server). For the Dockerized version of this test case, these configuration files assume that the docker contain will write files to a subdirectory called "./target". If you are starting a docker image from a directory, make sure there is a subdirectroy called target. That subdirectory will be mounted in the image, and it is the place where the outputs created by this program are saved on disk, even after the container that created them is gone.

## Generate Config File and Launch ETAS Catalog Generation
<pre>
$ u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir target/test_case_1 --random-seed 123456789

$ u3etas_launcher.sh target/test_case_1/config.json

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

## Run Plotting Stages retrieving Data from OpenSHA Server
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

