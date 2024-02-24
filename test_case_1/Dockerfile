#
# Build an Ubuntu installation for UCERF3-ETAS-Launcher
#
from ubuntu:jammy
MAINTAINER Philip Maechling maechlin@usc.edu

# Define Build and runtime arguments
# These accept userid and groupid from the command line
#ARG APP_UNAME
#ARG APP_GRPNAME
#ARG APP_UID
#ARG APP_GID
#ARG BDATE

# The following ENV set the username for this testcase: scecuser
# Hardcode the user and userID here for testing
ENV APP_UNAME=scecuser \
APP_GRPNAME=scec \
APP_UID=1000 \
APP_GID=20 \
BDATE=20240222

# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
# and for building the model and adding the correct date into the label
RUN echo $APP_UNAME $APP_GRPNAME $APP_UID $APP_GID $BDATE

#
RUN apt-get -y update
RUN apt-get -y upgrade
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt-get install -y build-essential git vim nano emacs default-jdk jupyter

RUN apt-get update && apt-get -y upgrade \
  && apt-get install -y --no-install-recommends \
    git \
    wget \
    g++ \
    default-jdk \
    jupyter \
    libproj-dev proj-data proj-bin libgeos-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Setup Owners
# Group add duplicates "staff" so just continue if it doesn't work
RUN groupadd -f --non-unique --gid $APP_GID $APP_GRPNAME
RUN useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME

#Define interactive user
USER $APP_UNAME

# Move to the user directory where the gmsvtoolkit is installed and built

ENV PATH="/home/$APP_UNAME/miniconda3/bin:${PATH}"
ARG PATH="/home/$APP_UNAME/miniconda3/bin:${PATH}"

WORKDIR /home/$APP_UNAME

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /home/$APP_UNAME/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && echo "Running $(conda --version)" \
    && conda update conda \
    && conda create -n scec-dev \
    && conda init bash

RUN echo 'conda activate scec-dev' >> /home/$APP_UNAME/.bashrc \
    && bash /home/$APP_UNAME/.bashrc \
    && conda install python=3.10 pip numpy notebook

RUN conda install -c conda-forge jupyterlab jupyterhub

# Get a copy of the UCERF3-ETAS-LAUNCHER repo
WORKDIR /home/$APP_UNAME
RUN git clone https://github.com/opensha/ucerf3-etas-launcher.git

WORKDIR /home/$APP_UNAME
RUN mkdir -p ucerf3-etas-simulations

# Setup UCERF3-ETAS environment variables
ENV ETAS_LAUNCHER=/home/$APP_UNAME/ucerf3-etas-launcher
ENV ETAS_SIM_DIR=/home/$APP_UNAME/ucerf3-etas-simulations
ENV PATH="$PATH:$ETAS_LAUNCHER/sbin"

# Build UCERF3-ETAS
WORKDIR /home/$APP_UNAME
RUN u3etas_opensha_update.sh -d

# Define file input/output mounted disk
#
VOLUME /home/$APP_UNAME/target
WORKDIR /home/$APP_UNAME/target
#
# The .bashrc and .bash_profile will Define ENV variables
#
#
# Add metadata to dockerfile using labels
LABEL "org.scec.project"="UCERF3-ETAS"
LABEL org.scec.responsible_person="Phil Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="$BDATE"
#
# Start Bash Terminal Window
# For prototyping, this repeats the username for this testcase as: scecuser
# Consolidate these usages to 1 when possible.
WORKDIR /home/$APP_UNAME
#ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/usr/bin/jupyter","lab","--ip=0.0.0.0","--notebook-dir=/home/scecuser","--allow-root","--no-browser"]
