#!/bin/bash

source /etc/profile

go_dir=/workspace/go_service

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

cd ${go_dir}/${1}
if [ -e ${1} ]; then
    rm ${1}
    yellow_echo "Clean previous builded ${1}"
fi
CGO_ENABLED=0 GOOS=linux go build
if [ $? -ne 0 ]; then
    red_echo "Build ${1} unsuccessfully"
else
    green_echo "Build ${1} successfully"
fi
cd /workspace
