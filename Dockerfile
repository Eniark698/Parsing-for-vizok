# Use the latest version of Ubuntu
FROM ubuntu:latest

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update the repository and install necessary packages
RUN apt-get update && apt-get install -y \
#   ubuntu-desktop \
   lsb-release \ 
   firefox \
   wget \
   curl \
   git \
   vim \
   nano \
   sudo \
   net-tools \
   novnc \
   websockify \
   x11vnc \
   xvfb \
   lxde \
   build-essential \
   python3.11 \
   pip \
   dbus-x11 \
   gnome-session \
   gnome-terminal


RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
 msodbcsql18 \
 mssql-tools18 \
 unixodbc-dev


# Create a user
RUN useradd -m docker && \
    echo "docker:docker" | chpasswd && \
   adduser docker sudo && \
   echo 'docker ALL=NOPASSWD: ALL' >> /etc/sudoers


# Set the user for the subsequent RUN/CMD commands
USER docker

# Set the working directory
WORKDIR /home/docker

# Clone my repo into the home directory
RUN git clone https://github.com/Eniark698/Parsing-for-vizok.git

# Install python deps from requirements.txt
RUN python3.11 -m pip install -r ./Parsing-for-vizok/requirements-311.txt

# Install playwright again
RUN pip3 install playwright

# Install python deps from playwright
RUN python3 -m playwright install

COPY lightdm.conf /etc/lightdm/lightdm.conf

# Clone noVNC into the home directory
RUN git clone https://github.com/novnc/noVNC.git

# Set up VNC password
RUN mkdir -p ~/.vnc && x11vnc -storepasswd 8vacUxZziO ~/.vnc/passwd

# Set up the startup script
COPY start.sh .
RUN sudo chmod +x start.sh
RUN sudo mkdir -p /tmp/.X11-unix
RUN sudo chmod 1777 /tmp/.X11-unix
RUN sudo chown root /tmp/.X11-unix


# Expose the noVNC port
EXPOSE 6080


# Command to run the startup script
CMD ["./start.sh"]