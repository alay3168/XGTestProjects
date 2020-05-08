#!/bin/bash

url=http://10.58.122.61:8000/software

# Get cmake-3.13.1
wget $url/cmake-3.13.1.tar.gz
tar -xzvf cmake-3.13.1.tar.gz
rm cmake-3.13.1.tar.gz

# Get gcc-5.5.0
wget $url/gcc-5.5.0.tar.gz
tar -xzvf gcc-5.5.0.tar.gz
rm gcc-5.5.0.tar.gz

# Get opencv-4.0.0
wget $url/opencv-4.0.0.tar.gz
tar -xzvf opencv-4.0.0.tar.gz
rm opencv-4.0.0.tar.gz

# Get opencv_contrib-4.0.0
wget $url/opencv_contrib-4.0.0.tar.gz
tar -xzvf opencv_contrib-4.0.0.tar.gz
rm opencv_contrib-4.0.0.tar.gz

# Get go path
wget $url/go_path.tar.gz
tar -xzvf go_path.tar.gz
rm go_path.tar.gz

# Get go root
wget $url/go_root.tar.gz
tar -xzvf go_root.tar.gz
rm go_root.tar.gz
