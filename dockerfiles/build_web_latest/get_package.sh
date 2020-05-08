#!/bin/bash

url=http://10.58.122.61:8000/software

# Get nodejs
wget $url/node-v8.12.0.tar.gz
tar -xzvf node-v8.12.0.tar.gz
rm node-v8.12.0.tar.gz
