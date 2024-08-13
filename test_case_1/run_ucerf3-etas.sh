# -rm removes container on exit
# -it indicates inteactive + --tty so that users are at an interactive tty command line when the container starts

mkdir -p target
docker run -i -t sceccode/ucerf3_jup
