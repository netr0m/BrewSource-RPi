=======
# [BrewSource | Backend] (http://brewsource.no) - :snake:Python3
Script to read temperature data from a DS18B20 sensor

BrewSource, a Raspberry Pi-powered monitor for your brewing :beers:. Written in :snake:Python and :sailboat:Sails.js

**Developed by:** Morten Amundsen.py, Svenn-Roger Sørensen.js

This repository is for our group project in the course IS-213, **_Open Source_**

- Developed in Python
- 1 Using a DS18B20 Waterproof Temperature Sensor to read temperatures

**The launcher.sh script is used to run the python script on reboot**

_In order to get this working, you'll need to do the following:_
```sh
sudo crontab -e
@reboot sh /home/pi/brewpi/launcher.sh >/home/pi/logs/cronlog 2>&1
```
