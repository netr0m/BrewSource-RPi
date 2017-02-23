#!/usr/bin/python
import os

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

# Run command to start the camera streaming, with the parameters defined above
def start_stream():
    try:
        os.system("""raspivid -o - -t 0 -hf -w %s -h %s -fps %s
        |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:%s}' :demux=h264"""
                  %(width, height, frames, port))
    except:
        # Exception: Either VLC is missing, or the camera failed to load
        os.system("sudo apt-get install vlc")
        print("An error has occured. You're either missing VLC, or your camera module is not properly installed/enabled")


start_stream()
