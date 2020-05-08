#!/bin/bash

. ./echo_color.sh
source local_env.conf

declare -A repo_pid
declare -A repo_result
declare -A repo_dir

all_pid=""
logs_dir=`mkdir -p ../logs && cd ../logs && pwd`

repo_pid=(
["AlarmSystem"]=""
["DeviceManager"]=""
["MapManager"]=""
["nvr"]=""
["RtspClient"]=""
["StaffRepository"]=""
["ImageStorage"]=""
["WebSystemImageService"]=""
["authentication"]=""
["ImageRetrieve"]=""
["grpc-getway"]=""
["GrpcCommon"]=""
["AccessAuth"]=""
["CommunitySecurityWebSystem"]=""
["navigation"]=""
["Watchmen"]=""
["Solace"]=""
["TheGood"]=""
["AliyunVOD"]=""
["LogSync"]=""
["CaseField"]=""
["FeiDan"]=""
["FeiDan_Web"]=""
)

repo_result=(
["AlarmSystem"]=""
["DeviceManager"]=""
["MapManager"]=""
["nvr"]=""
["RtspClient"]=""
["StaffRepository"]=""
["ImageStorage"]=""
["WebSystemImageService"]=""
["authentication"]=""
["ImageRetrieve"]=""
["grpc-getway"]=""
["GrpcCommon"]=""
["AccessAuth"]=""
["CommunitySecurityWebSystem"]=""
["navigation"]=""
["Watchmen"]=""
["Solace"]=""
["TheGood"]=""
["AliyunVOD"]=""
["LogSync"]=""
["CaseField"]=""
["FeiDan"]=""
["FeiDan_Web"]=""
)

repo_dir=(
["AlarmSystem"]="${go_dir}"
["DeviceManager"]="${go_dir}"
["MapManager"]="${go_dir}"
["nvr"]="${go_dir}"
["RtspClient"]="${go_dir}"
["StaffRepository"]="${go_dir}"
["ImageStorage"]="${go_dir}"
["WebSystemImageService"]="${go_dir}"
["authentication"]="${go_dir}"
["ImageRetrieve"]="${go_dir}"
["grpc-getway"]="${go_dir}"
["GrpcCommon"]="${go_dir}"
["AccessAuth"]="${src_dir}"
["CommunitySecurityWebSystem"]="${src_dir}"
["navigation"]="${src_dir}"
["Watchmen"]="${go_dir}"
["Solace"]="${xg_dir}"
["TheGood"]="${xg_dir}"
["AliyunVOD"]="${go_dir}"
["LogSync"]="${go_dir}"
["CaseField"]="${go_dir}"
["FeiDan"]="${go_dir}"
["FeiDan_Web"]="${src_dir}"
)

yellow_echo "Start to pull source code"

# use background subshell to pull code to save time
for api in $(echo ${!repo_result[*]})
do
    # {
    # set -e
    yellow_echo "Start to pull $api code"

    cd ${repo_dir[$api]}/${api} > /dev/null
    log=${logs_dir}/${api}.log
    echo "" > $log 2>&1

    git clean -f >> $log 2>&1
    git checkout -- . >> $log 2>&1
    git fetch >> $log 2>&1

    if [ $api == "grpc-getway" ] ; then
        git checkout ${getway_branch} > $log 2>&1
    else
        git checkout `eval echo '$'"${api}_branch"` >> $log 2>&1
    fi

    git pull --rebase >> $log 2>&1
    cd - &>/dev/null
    # } &
    pid=$!
    all_pid=$all_pid" $pid"
    repo_pid[$api]=$pid
done

for api in $(echo ${!repo_pid[*]})
do
    wait ${repo_pid[$api]}
    repo_result[$api]=$?
done

fail_count=0

for api in $(echo ${!repo_result[*]})
do
   {
   ret=${repo_result[$api]}
   if [ $ret -eq 1 ]; then
       red_echo ""
       red_echo "============= Pull $api unsuccessfully"
       red_echo "$api subshell exit code: $ret"
       red_echo `cat ${logs_dir}/${api}.log`
       red_echo "=============================================================="
       ((fail_count++))
   else
       green_echo ""
       green_echo "============= Pull $api successfully"
       green_echo "$api subshell exit code: $ret"
       green_echo `cat ${logs_dir}/${api}.log`
       green_echo "=============================================================="
   fi
   }
done


if [ $fail_count -ne 0 ];then
    red_echo "Pulled some source code unsuccessfully"
fi

# Old version xgface xgindex
#scp -r user@10.58.122.61:/home1/publish_env/xg_server  ../src/xg_server/
#if [ $? -ne 0 ]; then
#    red_echo "Scp xgserver code unsuccessfully"
#    exit -1
#else
#    green_echo "Scp xgserver code successfully"
#fi

# Get xgface data
apt install sshpass -y
[ -e ../src/xg_server/ ] || sshpass -p 1qaz2wsx scp -r user@10.58.122.61:/home1/publish_env/xgface_data  ../src/xg_server/
if [ $? -ne 0 ]; then
    red_echo "Scp xgface data unsuccessfully"
else
    green_echo "Scp xgface data successfully"
fi

yellow_echo "Finish pulling source code"
