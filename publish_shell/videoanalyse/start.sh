#!/bin/bash
sudo docker rm -f videoanalyse &>/dev/null
sudo xhost +
sudo docker run -d --privileged --name videoanalyse -v /opt/videoanalyse/default.conf:/root/VideoAnalyse/default.conf -v /tmp/.X11-unix/:/tmp/.X11-unix -e DISPLAY=$DISPLAY --runtime=nvidia -e NVIDIA_DRIVER_CAPABILITIES=video,compute,utility -it 10.58.122.61:90/production/videoanalyse:0.14 /start.sh
