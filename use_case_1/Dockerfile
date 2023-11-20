#
# Build an Ubuntu installation for UCERF3-ETAS-Launcher
#
from ubuntu:jammy
MAINTAINER Kevin Milner kmilner@usc.edu

# Define Build and runtime arguments
# These accept userid and groupid from the command line
#ARG APP_UNAME
#ARG APP_GRPNAME
#ARG APP_UID
#ARG APP_GID
#ARG BDATE

ENV APP_UNAME=scecuser \
APP_GRPNAME=scec \
APP_UID=1000 \
APP_GID=20 \
BDATE=20231117

# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
# and for building the model and adding the correct date into the label
RUN echo $APP_UNAME $APP_GRPNAME $APP_UID $APP_GID $BDATE

#
RUN apt-get -y update
RUN apt-get -y upgrade
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles

RUN apt-get install -y build-essential git vim nano emacs default-jdk

# Setup Owners
# Group add duplicates "staff" so just continue if it doesn't work
RUN groupadd -f --non-unique --gid $APP_GID $APP_GRPNAME
RUN useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME

#Define interactive user
USER $APP_UNAME

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
LABEL org.scec.responsible_person="Kevin Milner"
LABEL org.scec.primary_contact="kmilner@usc.edu"
LABEL version="$BDATE"

#
# Start Bash Terminal Window
WORKDIR /home/$APP_UNAME
ENTRYPOINT ["/bin/bash"]
