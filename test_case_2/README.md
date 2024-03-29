# Test case #2

This repo contains a slurm script that is configured to run on a single node SDSC Expanse. Tests completed in ~3.2 hours on a single node on SDSC Expanses (w/ 128 cores and 256G Ram) and it uses inputs 20 Java threads and memory requirements (10GB per cpu) at starttime. A threaded calculation, with too little RAM/thread (cpu) may start up, generate some catalogs, then exits on out of memory. On expanse this has happened when trying to run with less than 8GB/thread. 


This test case runs the same ETAS Simulation with 10000 catalogs on a single Expanse Node.
The scripts to generate the generate the configuration file, and run the launcher are similar to the test case 1 commands.
Define a path to the lustre file system.
SET .bashrc to define ENV
<pre>
    # User specific aliases and functions for bbp
#module load cpu/0.15.4
#module load gcc/9.2.0
# Common module loads
module load slurm
module load sdsc
export ETAS_MEM_GB=20
export ETAS_LAUNCHER=/expanse/lustre/projects/ddp408/ux454496/ucerf3_etas_test_cases/ucerf3-etas-launcher
export ETAS_THREADS=10
export ETAS_SIM_DIR=/expanse/lustre/projects/ddp408/ux454496/ucerf3_etas_test_cases
export PATH=$PATH:$ETAS_LAUNCHER/parallel/slurm_sbin:$ETAS_LAUNCHER/sbin/
</pre>
$ git clone htttps://github.com/sceccode/ucerf3_etas_test_cases.git
From there run the script to generate the test_case_2/config.json file.

````
$ u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10000 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir test_case_2 --random-seed 123456789

````
Then move into the test_case_2/ and submit the config to the batch system.
````
$ sbatch etas_sim_single_node.slurm
````

<pre>
Test Case 2 runs UCERF3-ETAS simulations generate 10 year earthquake catalogs based on the Ridgecrest M7.1 main shock. The test case runs on a single Expanse CPU node. It generates 10 year ETAS catalogs after the Ridgecrest M7.1. It uses a copy of the Comcat catalog, and forecasts annual earthquake forecasts for the next 10 years. The default test case generates 10000 alternative 10 year earthquake catalogs.

Test case 2.1 is defined to be the ucerf3 catalog creation processing stage. User-oriented etas products include the catalog generation, and plotting scripts to help summarize the results. The plotting scripts stage of the processing depend on the performance of external systems (non-ACCESS data servers) so plotting is excluded from this as a scaling performance test case.

As a N=10000 catalog run. It currently takes around 3 hours to run on one Expanse CPU nodes, using 20 Threads and 10Gb per thread RAM. 
A end-user test case which produced a proactical deliverable, will add the plotting stage. This requires the opensha.org server operating during the test. Ifthe plotting script is invoked and all plots will be generated in a 'plots' folder.

# installation
To build the opensha jar file, the Expanse head node does not allow enough memory to build this jar. To build it before running the simulations, you can request an interactive node and build it on the node before you run the simulations

<pre>
srun --partition=debug  --pty --account=ddp408 --nodes=1 --ntasks-per-node=4 \
    --mem=20G -t 00:30:00 --wait=0 --export=ALL /bin/bash

</pre>
Then, build with either the update or the test commands
<pre>
# Build UCERF3-ETAS
WORKDIR /home/$APP_UNAME
sbin/u3etas_opensha_update.sh -d
or
sbin/u3etas_env_test.sh
</pre>
# Storage Requirements

* Input file size: 81kb
* After simulation and plots: 4.3GB

# Additional details

The lines below should be added to .bashrc and set to point to the right locations:

<pre>
# Command module purge command
module purge
# Module load for ETAS
module load cpu/0.15.4
module load openjdk/11.0.2

# Common module loads
module load slurm
module load sdsc
export ETAS_MEM_GB=14
export ETAS_LAUNCHER=/expanse/lustre/projects/ddp408/ux454496/ucerf3_etas_use_cases/ucerf3-etas-launcher
export ETAS_THREADS=3
export ETAS_SIM_DIR=/expanse/lustre/projects/ddp408/ux454496/ucerf3_etas_use_cases
export PATH=$PATH:$ETAS_LAUNCHER/parallel/slurm_sbin:$ETAS_LAUNCHER/sbin/
</pre>


# Slurm Script
<pre>
#!/bin/bash
#SBATCH -t 04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --mem=200G
#SBATCH --partition=compute
#SBATCH --account=allocation_id
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user scecuser@usc.edu
#SBATCH --mail-type=ALL
#SBATCH --get-user-env
######################
## INPUT PARAMETERS ##
######################
## ETAS PARAMETERS ##
# path to the JSON configuration file
ETAS_CONF_JSON="${ETAS_SIM_DIR}/test_case_2/config.json"
## JAVA/MPJ PARAMETERS ##
# maxmimum memory in gigabytes. should be close to, but not over, total memory available
MEM_GIGS=200
# number of etas threads. should be approximately MEM_GIGS/5, and no more than the total number of threads available
THREADS=20
# path to the opensha-ucerf3 jar file
JAR_FILE=${ETAS_LAUNCHER}/opensha/opensha-all.jar

##########################
## END INPUT PARAMETERS ##
##   DO NOT EDIT BELOW  ##
##########################
NEW_JAR="`dirname ${ETAS_CONF_JSON}`/`basename $JAR_FILE`"
cp $JAR_FILE $NEW_JAR
if [[ -e $NEW_JAR ]];then
        JAR_FILE=$NEW_JAR
fi
date
java -Djava.awt.headless=true -Xmx${MEM_GIGS}G -cp $JAR_FILE scratch.UCERF3.erf.ETAS.launcher.ETAS_Launcher --threads $THREADS $ETAS_CONF_JSON
ret=$?
date
#java -Djava.awt.headless=true -Xmx${MEM_GIGS}G -cp $JAR_FILE scratch.UCERF3.erf.ETAS.analysis.SimulationMarkdownGenerator --threads $THREADS $ETAS_CONF_JSON
exit $ret
</pre>
