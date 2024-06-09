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
