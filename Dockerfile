# Use the latest version of Ubuntu
FROM ubuntu:latest

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update the repository and install necessary packages
RUN apt-get update && apt-get install -y \
   ubuntu-desktop \
   firefox \
   wget \
   curl \
   git \
   vim \
   sudo \
   net-tools \
   novnc \
   websockify \
   x11vnc \
   xvfb \
   build-essential \
   python3.11 \
   pip



RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \ msodbcsql18 \ mssql-tools18 \ unixodbc-dev

# Create a user
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

# Set the user for the subsequent RUN/CMD commands
USER docker

# Set the working directory
WORKDIR /home/docker

# Clone my repo into the home directory
RUN git clone https://github.com/Eniark698/Parsing-for-vizok.git

# Install python deps from requirements.txt
RUN python3.11 -m pip install -r ./Parsing-for-vizok/requirements-311.txt

# Install python deps from playwrigt
RUN python3.11 -m playwright install

# Clone noVNC into the home directory
RUN git clone https://github.com/novnc/noVNC.git

# Set up VNC password
RUN mkdir -p ~/.vnc && x11vnc -storepasswd 8vacUxZziO ~/.vnc/passwd

# Changing user to root to change permission
USER root

# Set up the startup script
COPY start.sh .
RUN chmod +x start.sh

#Switching back to docker user
USER docker


# Expose the noVNC port
EXPOSE 6080

# Command to run the startup script
CMD ["./start.sh"]