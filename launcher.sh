#!/bin/sh
# launcher.sh
# navigate to home, then to this dir, then execute python script

cd /
cd home/pi/brewpi/temp
sudo python thermometer.py
cd /
