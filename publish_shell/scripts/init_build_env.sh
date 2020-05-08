#!/bin/bash

. ./echo_color.sh
source local_env.conf

yellow_echo "Start to initialize build environment"

# Create source code directory
mkdir -p $src_dir
if [ $? -ne 0 ]; then
    red_echo "Make directory $src_dir unsuccessfully"
else
    green_echo "Make directory $src_dir successfully"
fi

# Copy build script to source code directory for docker build
cp build_*.sh $src_dir && chmod +x *.sh
if [ $? -ne 0 ]; then
    red_echo "Copy build_*.sh to $src_dir unsuccessfully"
else
    green_echo "Copy build_*.sh to $src_dir successfully"
fi

# Create tmp directory in source code directory
mkdir -p $src_dir/tmp
if [ $? -ne 0 ]; then
    red_echo "Make directory $src_dir/tmp unsuccessfully"
else
    green_echo "Make directory $src_dir/tmp successfully"
fi


# Create go source code directory
mkdir -p $go_dir
if [ $? -ne 0 ]; then
    red_echo "Make directory $go_dir unsuccessfully"
else
    green_echo "Make directory $go_dir successfully"
fi

# Create xgface and xgindex  source code directory
mkdir -p $xg_dir
if [ $? -ne 0 ]; then
    red_echo "Make directory $xg_dir unsuccessfully"
else
    green_echo "Make directory $xg_dir successfully"
fi

# Clone go source code directory
for api in AlarmSystem \
    DeviceManager \
    nvr \
    RtspClient \
    MapManager \
    StaffRepository \
    WebSystemImageService \
    grpc-getway \
    GrpcCommon \
    Watchmen \
    ImageStorage \
    ImageRetrieve \
    AliyunVOD \
    CaseField \
    LogSync \
    FeiDan \
    authentication
do 
    cd ${go_dir}
    if [ ! -d $api ]; then
        git clone git@47.111.178.139:Intelligentvision/${api}.git
        if [ $? -ne 0 ]; then
            red_echo "Clone $api source code unsuccessfully"
        else
            green_echo "Clone $api source code successfully"
        fi
    else
        green_echo "$api source code exists"
    fi
    cd - &>/dev/null
done

# Clone web source code directory
for i in AccessAuth CommunitySecurityWebSystem navigation FeiDan_Web
do 
    cd ${src_dir}
    if [ ! -d $i ]; then
        git clone git@47.111.178.139:Intelligentvision/${i}.git
        if [ $? -ne 0 ]; then
            red_echo "Clone $i source code unsuccessfully"
        else
            green_echo "Clone $i source code successfully"
        fi
    else
        green_echo "$i source code exists"
    fi
    cd - &>/dev/null
done

for i in Solace TheGood 
do 
    cd ${xg_dir}
    if [ ! -d $i ]; then
        git clone git@47.111.178.139:Intelligentvision/${i}.git
        if [ $? -ne 0 ]; then
            red_echo "Clone $i source code unsuccessfully"
        else
            green_echo "Clone $i source code successfully"
        fi
    else
        green_echo "$i source code exists"
    fi
    cd - &>/dev/null
done

yellow_echo "Finish initializing build environment"
