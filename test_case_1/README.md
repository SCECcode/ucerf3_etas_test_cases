# Test Case 1
This is a ucerf3 etas test case for a laptop scale computer. This test case is run from a Docker image to simply distribution of opensha codes.

# Steps for running the tutorial UCERF3-ETAS simulation inside the Docker container

* u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir ../target/comcat-ridgecrest-m7.1-example --random-seed 123456789
* u3etas_launcher.sh ../target/comcat-ridgecrest-m7.1-example/config.json
* u3etas_plot_generator.sh target/comcat-ridgecrest-m7.1-example/config.json

# Examples

Once you have defined a JSON ETAS configuration file, you can use the scripts in the sbin directory. More detailed information on these scripts is available in the README. Commands shown below assume that you have added the sbin direcotory to your PATH.

To run a set of ETAS simulations on a single machine (but possibly with multiple threads), use the u3etas_launcher.sh command:
* u3etas_launcher.sh [--threads <num-threads>] </path/to/etas_configuration.json>
* For example, to run ETAS simulations for a JSON file in the current directory named "config.json" with 3 threads:
* u3etas_launcher.sh --threads 3 config.json

# Storage Requirements

* After creating configuration file: 1.2M
* After running simulation: 9.1M
* After generating all plots: 40M
