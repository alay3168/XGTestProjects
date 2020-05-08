#!/bin/bash


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

yellow_echo "Start to build ${1}" 

cd /workspace/${1}
yarn config set registry https://registry.npm.taobao.org
yarn
Version=V2.3.0.$(date +%Y%m%d) npm run build
if [ $? -ne 0 ]; then
    red_echo "Build ${1} failed"
else
    green_echo "Build ${1} successfully"
fi