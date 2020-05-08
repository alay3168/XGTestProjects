#!/bin/bash

source /etc/profile

go_dir=/workspace/go/src/github.com/Intelligentvision

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

yellow_echo "Start to build ${1} binary" 

cd ${go_dir}/${1}/HIK_SDK_RPC
if [ -e ${1} ]; then
    rm ${1}
    yellow_echo "Clean previous builded ${1}"
fi

chmod +x proto_gen.sh
./proto_gen.sh
if [ $? -ne 0 ]; then
    red_echo "Build ${1} run ./proto_env unsuccessfully"
else
    green_echo "Build ${1} run ./proto_env successfully"
fi

make -j
if [ $? -ne 0 ]; then
    red_echo "Build ${1} unsuccessfully"
else
    green_echo "Build ${1} successfully"
fi

cd /workspace
yellow_echo "Finish building ${1} binary" 
