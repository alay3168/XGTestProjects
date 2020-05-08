#!/bin/bash
sudo docker rm -f faceshow &>/dev/null
sudo xhost +
sudo docker run -d --name faceshow --privileged -v /opt/faceshow/config.json:/workspace/faceshow/config.json -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -e NVIDIA_DRIVER_CAPABILITIES=video,compute,utility --runtime=nvidia 10.58.122.61:90/build/faceshow:v3 /start.sh