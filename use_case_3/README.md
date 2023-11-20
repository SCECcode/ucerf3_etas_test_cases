# Use case #3

This use case runs 10k simulations on several nodes (currently set to 14 nodes). It takes around 45 minutes to run on Expanse. After the simulations complete, the plotting script is invoked and all plots will be generated in a 'plots' folder.

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