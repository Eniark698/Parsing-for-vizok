#!/bin/bash

# Start the VNC server
x11vnc -xkb -noxrecord -noxfixes -noxdamage -display :0 -auth /var/run/lightdm/root/:0 -forever -bg

# Start the noVNC server
cd /home/docker/noVNC && ./utils/launch.sh --vnc localhost:5900

# Start the Ubuntu desktop environment
/usr/sbin/lightdm &