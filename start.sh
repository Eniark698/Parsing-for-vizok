#!/bin/bash

# Start Xvfb
Xvfb :0 -screen 0 1920x1080x24 &

# Wait for Xvfb to start
sleep 3

# Start the VNC server with the password file
x11vnc -xkb -noxrecord -noxfixes -noxdamage -display :0 -auth /var/run/lightdm/root/:0 -rfbauth /home/docker/.vnc/passwd -forever -bg

# Start the noVNC server
cd /home/docker/noVNC && ./utils/novnc_proxy  --vnc localhost:5900
#dbus-daemon --system

# Start the Ubuntu desktop environment
#/usr/sbin/lightdm &
DISPLAY=:0 startxlde &