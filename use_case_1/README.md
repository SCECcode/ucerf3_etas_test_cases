## Steps for running the tutorial UCERF3-ETAS simulation inside the Docker container

* u3etas_comcat_event_config_builder.sh --event-id ci38457511 --num-simulations 10 --days-before 7 --finite-surf-shakemap --finite-surf-shakemap-min-mag 5 --output-dir ucerf3-etas-simulations/comcat-ridgecrest-m7.1-example --random-seed 123456789

* u3etas_launcher.sh ucerf3-etas-simulations/comcat-ridgecrest-m7.1-example/config.json

* u3etas_plot_generator.sh ucerf3-etas-simulations/comcat-ridgecrest-m7.1-example/config.json

## Storage Requirements

* After creating configuration file: 1.2M
* After running simulation: 9.1M
* After generating all plots: 40M
