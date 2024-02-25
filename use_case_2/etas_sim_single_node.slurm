#!/bin/bash
#SBATCH -t 04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem=200G
#SBATCH --partition=compute
#SBATCH --account=ddp408
#SBATCH --output=R-%x.%j.out
#SBATCH --error=R-%x.%j.err
#SBATCH --mail-user maechlin@usc.edu
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
THREADS=10

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

java -Djava.awt.headless=true -Xmx${MEM_GIGS}G -cp $JAR_FILE scratch.UCERF3.erf.ETAS.analysis.SimulationMarkdownGenerator --threads $THREADS $ETAS_CONF_JSON

exit $ret
