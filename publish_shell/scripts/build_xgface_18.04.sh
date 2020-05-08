#!/bin/bash

source /etc/profile


function yellow_echo () 
{
        local what=$*
        echo -e "\e[1;33m-- ${what} \e[0m"
}

function green_echo () 
{
        local what=$*
        echo -e "\e[1;32m-- ${what} \e[0m"
}

function red_echo () 
{
        local what=$*
        echo -e "\e[1;31m-- ${what} \e[0m"
}

yellow_echo "Start to build xgface binary" 

#Build xgface_server
cd /workspace/xg_server/Solace
rm -rf build

cat CMakeLists.txt | grep gflags
if [ $? -ne 0 ]; then
    sed -i '/link_libraries(/a\    gflags' CMakeLists.txt 
fi

./codegen 
mkdir build
cd build && cmake .. && make -j
if [ $? -ne 0 ]; then
    red_echo "Build xgface_server failed"
else
    green_echo "Build xgface_server successfully"
fi

cd /workspace

yellow_echo "Finish building xgface binary" 
