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

cd ${go_dir}/${1}
if [ -e ${1} ]; then
    rm -f ${1} 
    yellow_echo "Clean previous binary ${1} success!"
fi
if [[ ${1} == "DeviceManager" ]];then
    cp -arpv /workspace/go/src/github.com/Intelligentvision/DeviceManager/app/onvif/libcamctrl.so /usr/lib/libcamctrl.so
    GOOS=linux go build
    if [ $? -ne 0 ]; then
        red_echo "Build ${1} unsuccess!"
    else
        green_echo "Build ${1} success!"
    fi
elif [ ${1} == "RtspClient" -o ${1} == "AliyunVOD" ]; then
    cd ${go_dir}/${1}/server && rm -rf server && CGO_ENABLED=0 GOOS=linux go build
    if [ $? -ne 0 ]; then
        red_echo "Build ${1} unsuccess!"
    else
        green_echo "Build ${1} success!"
    fi
elif [[ ${1} == "Watchmen" ]]; then
    CGO_ENABLED=1 GOOS=linux go build -o ${1}
    if [ $? -ne 0 ]; then
        red_echo "Build ${1} unsuccess!"
    else
        green_echo "Build ${1} success!"
    fi
else
    CGO_ENABLED=0 GOOS=linux go build -o ${1}
    if [ $? -ne 0 ]; then
        red_echo "Build ${1} unsuccess!"
    else
        green_echo "Build ${1} success!"
    fi
fi
cd /workspace
