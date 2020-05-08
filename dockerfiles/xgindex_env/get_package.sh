#!/bin/bash

url=http://10.58.122.61:8000/software

# Get grpc
wget $url/grpc.tar.gz
tar -xzvf grpc.tar.gz
rm grpc.tar.gz

# Get protobuf
wget $url/protobuf-3.5.1.tar.gz
tar -xzvf protobuf-3.5.1.tar.gz
rm protobuf-3.5.1.tar.gz
