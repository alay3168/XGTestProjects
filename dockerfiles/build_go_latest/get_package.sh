#!/bin/bash

url=http://10.58.122.61:8000/software

# Get go path
wget $url/go_path.tar.gz
tar -xzvf go_path.tar.gz
rm go_path.tar.gz

# Get go root
wget $url/go_root.tar.gz
tar -xzvf go_root.tar.gz
rm go_root.tar.gz
