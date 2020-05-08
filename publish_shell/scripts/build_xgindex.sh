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

yellow_echo "Start to build xgindex binary" 

#Build index_server
#ln -s /usr/bin/g++-5 /usr/bin/g++ -f
#ln -s /usr/bin/gcc-5 /usr/bin/gcc -f
cd /workspace/xg_server/TheGood/service
make clean
#make -j
cd /workspace/xg_server/TheGood
rm -rf service/index_server
cp -av ./flann/lib/* /usr/lib/
make clean 
make -j
if [ $? -ne 0 ]; then
    red_echo "Build xgindex_server failed"
else
    green_echo "Build xgindex_server successfully"
fi

cd /workspace

yellow_echo "Finish building xgindex binary" 
