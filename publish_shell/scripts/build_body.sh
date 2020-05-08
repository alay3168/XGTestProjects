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

yellow_echo "Start to build BodyDetect binary"

#Build BodyDetect
cd /workspace/BodyDetect
chmod +x ./codegen && ./codegen
rm -rf build
mkdir -p build && cd build && cmake .. && make -j
if [ $? -ne 0 ]; then
    red_echo "Build BodyDetect failed"
else
    green_echo "Build BodyDetect successfully"
fi

cd /workspace

yellow_echo "Finish building BodyDetect binary"