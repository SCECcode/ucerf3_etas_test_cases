# Test case #2
This test case runs the same ETAS Simulation with 10000 catalogs on a single Expanse Node.
The scripts to generate the generate the configuration file, and run the launcher are similar to the test case 1 commands.
````
$ u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir target/test_case_2 --random-seed 123456789
$ u3etas_launcher.sh target/test_case_1/config.json
````


<pre>
This Test Case runs 10k simulations on a single node. 
This test case generates ETAS catalogs after the Ridgecrest M7.1.
It uses a copy of the Comcat catalog, and forecasts annual earthquake forecasts for the next 10 years.
This m
This test case 2.1 is defined to be the ucerf3 catalog creation, but not the plotting, because the plotting stages depend on the performance of external systems, specifically a data server at USC.
As a N=10000 catalog run. It currently takes around 3 hours to run on one Expanse CPU nodes, using 20 Threads and 10Gb per thread RAM. 
A end-user test case which produced a proactical deliverable, will add the plotting stage. This requires the opensha.org server operating during the test. Ifthe plotting script is invoked and all plots will be generated in a 'plots' folder.

# installation
To build the opensha jar file, the Expanse head node does not allow enough memory to build this jar. To build it before running the simulations, you can request an interactive node and build it on the node before you run the simulations

<pre>
srun --partition=debug  --pty --account=ddp409 --nodes=1 --ntasks-per-node=4 \
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
