# Use case #3

This use case runs 10k simulations on several nodes (currently set to 14 nodes). It takes around 45 minutes to run on Expanse. After the simulations complete, the plotting script is invoked and all plots will be generated in a 'plots' folder.

# Generate the json.config file
From the directory about this, generate the config.json file and point to test_case_3 as output directory.
This typically has to be done on a compute node. On stampede3 the idev helps get a node quickly.
<pre>
u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10000 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir test_case_3 --random-seed 123456789


</pre>
# Storage Requirements

* Input file size: 81kb
* After simulation and plots: 4.3GB

# Additional details

The lines below should be added to .bashrc and set to point to the right locations:

```
module load cpu/0.15.4
module load openjdk/11.0.2

export ETAS_LAUNCHER=<PATH TO UCERF3-ETAS-LAUNCHER>
export PATH=$ETAS_LAUNCHER/sbin:$PATH
export ETAS_SIM_DIR=<PATH TO SIMULATION FOLDER in lustre file system>
export MPJ_HOME=<PATH TO MPJ EXPRESS>
export PATH=$ETAS_LAUNCHER/parallel/slurm_sbin:$MPJ_HOME/bin:$PATH
```

## Example slurm submit script
<pre>
  


login3.frontera(1200)$ more etas_sim_mpj.slurm
#!/bin/bash

#SBATCH -t 24:00:00
#SBATCH --nodes 14
#SBATCH --ntasks 14
#SBATCH --cpus-per-task=56
#SBATCH --partition normal
#SBATCH --mem 0
#SBATCH --job-name=u3etas
#SBATCH --output=%j_%x.out
#SBATCH --error=%j_%x.err
#SBATCH --mail-user=maechlin@usc.edu
#SBATCH --mail-type=ALL
#SBATCH --export=ALL
#SBATCH --account EAR20006

# Report on status

NP=${SLURM_NTASKS}
echo "Running on $NP processors: $NP"
echo "SLURM_NTASKS=$SLURM_NTASKS"
echo "NP=$NP"

echo "Job ID: $SLURM_JOB_ID"
echo "Job name: $SLURM_JOB_NAME"
echo "Node list: $SLURM_NODELIST"
echo "Number of tasks: $SLURM_NTASKS"
echo "Number of CPUs per task: $SLURM_CPUS_PER_TASK"

echo "SLURM_NTASKS=$SLURM_NTASKS"
echo "NP=$NP"


######################
## INPUT PARAMETERS ##
######################

# the above '#SBATCH' lines are requred, and are supposed to start with a '#'. They must be at the beginning of the file
# the '-t hh:mm:ss' argument is the wall clock time of the job
# the '-N 10' argument specifies the number of nodes required, in this case 10
# the '-n 560' argument specifies the number of cores, required by TACC. Set it to no more than 56*the number of nodes
# the 'p normal' argument specifies the queue, in this case we use the normal queue

## ETAS PARAMETERS ##

# path to the JSON configuration file
ETAS_CONF_JSON=$WORK/ucerf3/u3etas_sims/inputs/config.json

## JAVA/MPJ PARAMETERS ##

# maxmimum memory in gigabytes. should be close to, but not over, total memory available
MEM_GIGS=160

# number of etas threads. should be approximately MEM_GIGS/5, and no more than the total number of threads available
THREADS=20

# MPJ_HOME directory. Install from gz file
MPJ_HOME=$WORK/mpj-express

# path to the opensha-ucerf3 jar file
JAR_FILE=${ETAS_LAUNCHER}/opensha/opensha-all.jar

# simulations are sent out in batches to each compute node. these paramters control the size of those batches
# smaller max size will allow for better checking of progress with watch_logparse.sh, but more wasted time at the end of batches wai
ting on a single calculation to finish
MIN_DISPATCH=$THREADS
MAX_DISPATCH=500

# this allows for catalogs to be written locally on each compute node in a temporary directory, then only copied back onto shared st
orage after they complete. this reduces I/O load, but makes it harder to track progress of individual simulations. comment this out 
to disable this option
TEMP_OPTION="--temp-dir /tmp/etas-results-tmp"

# this allows for the results directory to be hosted on a different filesystem, in this case the $SCRATCH filesystem. this will prev
ent many files from being written to $WORK, as well as reducing I/O load
SCRATCH_OPTION="--scratch-dir $SCRATCH/etas-results-tmp"

# this automatically deletes subdirectories of the results directory once a catalog has been sucessfully written to the master binar
y file. comment out to disable
CLEAN_OPTION="--clean"

##########################
## END INPUT PARAMETERS ##
##   DO NOT EDIT BELOW  ##
##########################

NEW_JAR="`dirname ${ETAS_CONF_JSON}`/`basename $JAR_FILE`"
cp $JAR_FILE $NEW_JAR
if [[ -e $NEW_JAR ]];then
	JAR_FILE=$NEW_JAR
fi

PBS_NODEFILE="/tmp/${USER}-hostfile-${SLURM_JOBID}"
echo "creating PBS_NODEFILE: $PBS_NODEFILE"
scontrol show hostnames $SLURM_NODELIST > $PBS_NODEFILE

NEW_NODEFILE="/tmp/${USER}-hostfile-mpj-${SLURM_JOBID}"
echo "creating PBS_NODEFILE: $NEW_NODEFILE"
hname=$(hostname)
if [ "$hname" == "" ]
then
  echo "Error getting hostname. Exiting"
  exit 1
else
  cat $PBS_NODEFILE | sort | uniq | fgrep -v $hname > $NEW_NODEFILE
fi

export PBS_NODEFILE=$NEW_NODEFILE
export MPJ_HOME=$WORK/mpj-express
export PATH=$PATH:$MPJ_HOME/bin

if [[ $NP -le 0 ]]; then
  echo "invalid NP: $NP"
  exit 1
fi

JVM_MEM_MB=26624

date
echo "RUNNING MPJ"
t1=$(date +%s) # epoch start time in seconds

mpjrun_errdetect_wrapper.sh $PBS_NODEFILE -np $NP -dev niodev -Djava.library.path=$MPJ_HOME/lib -Xmx${MEM_GIGS}G -cp $JAR_FILE scrat
ch.UCERF3.erf.ETAS.launcher.MPJ_ETAS_Launcher --min-dispatch $MIN_DISPATCH --max-dispatch $MAX_DISPATCH --threads $THREADS $TEMP_OPT
ION $SCRATCH_OPTION $CLEAN_OPTION --end-time `scontrol show job $SLURM_JOB_ID | egrep --only-matching 'EndTime=[^ ]+' | cut -c 9-` $
ETAS_CONF_JSON
ret=$?
date

t2=$(date +%s) # epoch end time in seconds
numSec=$(echo $t2 - $t1 | bc -q ) # the number of seconds the process took.
runTime=$(date -ud @$numSec +%T) # Convert the seconds into Hours:Mins:Sec
echo "Time to Calculate Forecast: $runTime ($numSec seconds)"

exit $ret

</pre>
