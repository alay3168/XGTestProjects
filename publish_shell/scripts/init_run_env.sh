#!/bin/bash

. ./echo_color.sh
source local_env.conf

yellow_echo "Start to initialize run environment"

# Create run environments directory
mkdir -p $run_dir
if [ $? -ne 0 ]; then
    red_echo "Make directory $run_dir unsuccessfully"
    exit -1
else
    green_echo "Make directory $run_dir successfully"
fi

# Create go binary directory
cd ${run_dir}
for api in AlarmSystem \
    StaffRepository \
    ImageStorage \
    WebSystemImageService \
    authentication \
    ImageRetrieve \
    RtspClient \
    Watchmen \
    grpc-getway \
    CommunityLog \
    CommunitySystemApi \
    AliyunVOD \
    CaseField \
    LogSync \
    FeiDan
do
    mkdir -p binary/${api}
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$api unsuccessfully"
    fi
done

for api in DeviceManager \
    MapManager
do
    mkdir -p binary/${api}
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$api unsuccessfully"
    fi

    mkdir -p binary/${api}/config
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$api/config unsuccessfully"
    fi
done

for api in nvr
do
    mkdir -p binary/${api}/HIK_SDK_RPC/
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$api/HIK_SDK_RPC unsuccessfully"
    fi

    mkdir -p binary/${api}/lib/
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$api/lib unsuccessfully"
    fi
done

# Greate xgface binary directory
for i in xgface_server
do
    mkdir -p binary/$i/Solace/build/bin
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$i/Solace/build/bin unsuccessfully"
    fi
done

# Greate xgindex binary directory
for i in index_server_1
do
    mkdir -p binary/$i/TheGood/service
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$i/TheGood/service unsuccessfully"
    fi
done

for i in index_server_2
do
    mkdir -p binary/$i/TheGood/service
    if [ $? -ne 0 ]; then
        red_echo "Make directory binary/$i/TheGood/service unsuccessfully"
    fi
done

# Create mysql directory
mkdir -p mysql/conf
if [ $? -ne 0 ]; then
    red_echo "Make directory mysql/config unsuccessfully"
fi

mkdir -p mysql/data
if [ $? -ne 0 ]; then
    red_echo "Make directory mysql/data unsuccessfully"
fi

# Create openresty directory
mkdir -p openresty/nginx/conf
if [ $? -ne 0 ]; then
    red_echo "Make directory openresty/nginx/conf unsuccessfully"
fi

mkdir -p openresty/nginx/logs
if [ $? -ne 0 ]; then
    red_echo "Make directory openresty/nginx/logs unsuccessfully"
fi

mkdir -p openresty/nginx/www
if [ $? -ne 0 ]; then
    red_echo "Make directory openresty/nginx/www unsuccessfully"
fi

mkdir -p openresty/nginx/www/community
if [ $? -ne 0 ]; then
    red_echo "Make directory openresty/nginx/www/community unsuccessfully"
fi
cd - &>/dev/null

# # Copy geoserver to run env
# cp -arp ../apache-tomcat-9.0.7 ${run_dir}
# if [ $? -ne 0 ]; then
#     red_echo "Copy apache-tomcat-9.0.7 unsuccessfully"
#     exit -1
# fi

cp up_bin_sigle.sh ${run_dir}
if [ $? -ne 0 ]; then
    red_echo "Copy up_bin_single.sh unsuccessfully"
fi

# cp config to run_env
./cp_config_run_env.sh

yellow_echo "Finish initializing run environment"
