#!/usr/bin/python
import os
import socket
import fcntl
import struct

# Variables to define different qualities of the stream

# Width of the video stream | default: 800
width = 800

# Height of the video stream | default: 400
height = 400

# Number of Frames per Second (20-30 should be fine) | default: 30
frames = 30

# Which port the stream will open on
# Recommend leaving this to it's default value | default: 8160
port = 8160

# DO NOT TOUCH
ip = "0.0.0.0"

# Run command to start the camera streaming, with the parameters defined above
def start_stream():
    # Get the IP of the RPi
    ip = get_ip_address(get_wlan_eth())
    print("Starting streaming service")
    print("Your stream will be available at %s:%s" %(ip, port))
    try:
        print("Great success")
        print("Your stream is now available at %s:%s" %(ip, port))
        #os.system("raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264")
        os.system("""raspivid -o - -t 0 -hf -w %s -h %s -fps %s
                |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:%s}' :demux=h264"""
                  %(width, height, frames, port))
    except:
        print("Well, damn...")
        # Exception: Either VLC is missing, or the camera failed to load
        print("An error has occured. You're either missing VLC, or your camera module is not properly installed/enabled")
        print("Attempting to install VLC")
        try:
            os.system("sudo apt-get install vlc")
        except:
            print("VLC appears to be installed. Try rebooting. If the error persists, check your camera module")

# Get the IP-address of the RPi
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Check if the RPi is on WiFi or Ethernet, and return whatever connection it is
def get_wlan_eth():
    if (get_ip_address("wlan0") != None):
        return "wlan0"
    else:
        return "eth0"

start_stream()
