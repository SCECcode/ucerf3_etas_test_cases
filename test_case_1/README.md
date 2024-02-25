# Test Case 1
This is a ucerf3 etas test case for a laptop scale computer. 
This will test basic ETAS simulation capabilities using opensha codes, and run the same simulations on different machines, configuration the same simulation but a different number of catalogs, on different system configurations from laptop to multi-node supercompter.

# Steps for running the tutorial UCERF3-ETAS simulation inside the Docker container
This initial test case is assume to run in a Docker subdirectory on a laptop. The subdirectory where this sceccode/ucerf3_jup image is started, should have a subdirectory called target. This subdirectory will be mounted in the container and will be the location for the results to be written, and then visible from both the container, and from the laptop after the container exists.
* u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir ../target/comcat-ridgecrest-m7.1-example --random-seed 123456789
* u3etas_launcher.sh ../target/comcat-ridgecrest-m7.1-example/config.json
* u3etas_plot_generator.sh ../target/comcat-ridgecrest-m7.1-example/config.json

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
  
