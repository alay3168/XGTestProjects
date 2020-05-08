#!/bin/bash
# 自动接收key不输入yes
sed -i 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/' /etc/ssh/ssh_config
# 配置git登录
bash -c "echo 'http://qujin:Qujin0417@git.vision.puppyrobot.com'>~/.git-credentials && git config --global credential.helper store"
# 拉取publish_shell
if [ ! -d ../publish_shell ];then
    cd ../ && git clone http://qujin@git.vision.puppyrobot.com/Intelligentvision/publish_shell.git && cd - &> /dev/null
else
    cd ../publish_shell && git remote set-url origin http://git.vision.puppyrobot.com/Intelligentvision/publish_shell.git && \
    git fetch && git reset --hard origin/master && cd - &> /dev/null
fi
run_dir=$(pwd)
[ ! -d ../src ] && mkdir -p ../src
src_dir=`cd ../src && pwd`
scripts_dir=`cd ../publish_shell/scripts && pwd`
logs_dir=${src_dir}/logs
go_dir=${src_dir}/go_service
xg_dir=${src_dir}/xg_server
run_name=$(grep COMPOSE_NAME .env | awk -F '=' '{print $2}')
mkdir -p ${go_dir} ${xg_dir} ${logs_dir}
chmod +x ${scripts_dir}/*.sh

# Configure for code repo branch
ZhanHui_Server_branch=master
ZhanHui_Web_branch=master
Watchmen_branch=exh/master
GrpcCommon_branch=exh/master

# 设置程序源码目录
declare -A repo_dir
repo_dir=(
["ZhanHui_Server"]="${go_dir}"
["ZhanHui_Web"]="${src_dir}"
["GrpcCommon"]="${go_dir}"
["Watchmen"]="${go_dir}"
)

# 定义所有ZhanHui_Server程序
all_proj="OperationManage AliyunVOD GrpcCommon authentication FtpImage grpc-getway AlarmSystem StaffRepository DeviceManager MapManager WebSystemImageService ImageRetrieve nvr RtspClient BodyDetect CommunitySecurityWebSystem navigation Solace TheGood"
all_bin_proj="AlarmSystem authentication BodyDetect DeviceManager FtpImage grpc-getway ImageRetrieve MapManager nvr RtspClient Solace StaffRepository TheGood WebSystemImageService Watchmen"

# 登录阿里云docker
[ -e /root/.docker/config.json ] && grep -q "registry.cn-beijing.aliyuncs.com" /root/.docker/config.json
if [ $? -ne 0 ]
then
    docker login --username=智能视觉事业部 --password=1QAZ3edc registry.cn-beijing.aliyuncs.com &>/dev/null
fi
[ ! -e /root/.docker/config.json ] && docker login --username=智能视觉事业部 --password=1QAZ3edc registry.cn-beijing.aliyuncs.com &>/dev/null

nc -nz -w 1 10.58.122.61 90
if [ $? -eq 0 ];then
    BUILD_GO_ENV="10.58.122.61:90/build/build_go:latest"
    BUILD_GO_VENDOR_ENV="10.58.122.61:90/build/build_go_vendor:latest"
    BUILD_NVR_ENV="10.58.122.61:90/build/build_nvr:latest"
    BUILD_XGINDEX_ENV="10.58.122.61:90/build/build_xgindex:latest"
    BUILD_XGFACE_ENV="10.58.122.61:90/build/build_bodydetect:v4"
    BUILD_WEB_ENV="10.58.122.61:90/build/build_web:yarn"
    BUILD_WATCHMEN_ENV="10.58.122.61:90/build/build_watchmen:latest"
    BUILD_BODY_ENV="10.58.122.61:90/build/build_bodydetect:v4"
else
    BUILD_GO_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_go:latest"
    BUILD_GO_VENDOR_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_go_vendor:latest"
    BUILD_NVR_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_nvr:latest"
    BUILD_XGINDEX_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_xgindex:latest"
    BUILD_XGFACE_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_bodydetect:v4"
    BUILD_WEB_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_web:yarn"
    BUILD_WATCHMEN_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_watchmen:latest"
    BUILD_BODY_ENV="registry.cn-beijing.aliyuncs.com/puppy-build/build_bodydetect:v4"
fi
DOCKER_GO_NAME="build_go_"`date '+%Y%m%d-%H%M%S'`
DOCKER_GO_VENDOR_NAME="build_go_vendor"`date '+%Y%m%d-%H%M%S'`
DOCKER_NVR_NAME="build_nvr_"`date '+%Y%m%d-%H%M%S'`
DOCKER_XGINDEX_NAME="build_xgindex_"`date '+%Y%m%d-%H%M%S'`
DOCKER_XGFACE_NAME="build_xgface_"`date '+%Y%m%d-%H%M%S'`
DOCKER_WEB_NAME="build_web_"`date '+%Y%m%d-%H%M%S'`
DOCKER_WATCHMEN_NAME="build_watchmen_"`date '+%Y%m%d-%H%M%S'`
DOCKER_BODY_NAME="build_body_"`date '+%Y%m%d-%H%M%S'`

function yellow_echo () {
    local what=$*
    echo -e "\e[1;33m-- Info: ${what} \e[0m"
}
function green_echo () {
    local what=$*
    echo -e "\e[1;32m-- Info: ${what} \e[0m"
}
function red_echo () {
    local what=$*
    echo -e "\e[1;31m-- Error: ${what} \e[0m"
}

function pull_and_clean_build(){
    log=${logs_dir}/${1}.log
    echo '' > ${log}
    if [ ! -e ${repo_dir[$1]}/${1} ];then
        cd ${repo_dir[$1]} && git clone http://qujin@git.vision.puppyrobot.com/Intelligentvision/${1}.git
        cd ${repo_dir[$1]}/${1} 
        git checkout `eval echo '$'"${1}_branch"` &>> ${log}
    else
        cd ${repo_dir[$1]}/${1}
        git clean -f | tee -a ${log}
        git checkout -- . | tee -a ${log}
        yellow_echo "Start to pull ${1} code"
        git fetch --all | tee -a ${log}
        git reset --hard `eval echo '$'"${1}_branch"`
        git checkout `eval echo '$'"${1}_branch"` &>> ${log}
        git pull --rebase | tee -a ${log}
    fi
    green_echo "Pull ${1} code success!"
    cd - &> /dev/null
}

function build_go_common() {
    # build
    cp -v ${scripts_dir}/build_go_common.sh ${src_dir}
    yellow_echo "Start to build ${1} code."
    if [ ${1} == "Watchmen" ];then
        docker pull $BUILD_WATCHMEN_ENV
        docker run -v ${go_dir}/ZhanHui_Server:/workspace/go/src/github.com/Intelligentvision/ \
        -v ${src_dir}/ZhanHui_Server/mod:/workspace/go/pkg/mod \
        -v ${src_dir}/build_go_common.sh:/workspace/build_go_common.sh \
        --name $DOCKER_WATCHMEN_NAME -i $BUILD_WATCHMEN_ENV /bin/bash -c "/workspace/build_go_common.sh ${1}"
        docker rm $DOCKER_WATCHMEN_NAME &> /dev/null && green_echo "rm build container $DOCKER_WATCHMEN_NAME Success!"
    else
        docker pull $BUILD_GO_ENV
        if [ ${1} == "AliyunVOD" -o ${1} == "RtspClient" ];then
            bashStr="/workspace/build_go_common.sh"
        else
            bashStr="GO111MODULE=on GOPROXY=https://goproxy.cn,direct /workspace/build_go_common.sh"
        fi
        docker run -v ${go_dir}/ZhanHui_Server:/workspace/go/src/github.com/Intelligentvision/ \
        -v ${src_dir}/ZhanHui_Server/mod:/workspace/go/pkg/mod \
        -v ${xg_dir}:/workspace/xg_server \
        -v ${src_dir}/build_go_common.sh:/workspace/build_go_common.sh \
        --name $DOCKER_GO_NAME -i $BUILD_GO_ENV /bin/bash -c "${bashStr} ${1}"
        docker rm $DOCKER_GO_NAME &> /dev/null && green_echo "rm build container $DOCKER_GO_NAME Success!"
    fi
    # stop service
    cd ${run_dir} && sudo docker stop ${run_name}_${1} &> /dev/null
    if [ $? -ne 0 ]; then
        red_echo "Stop ${1} container unsuccessfully"
    else
        green_echo "Stop ${1} container successfully"
    fi
    # cp bin to run_env
    if [ ${1} == "AliyunVOD" -o ${1} == "RtspClient" ];then
        cp -v ${go_dir}/ZhanHui_Server/${1}/server/server ${run_dir}/binary/${1} && green_echo "Copy ${1} binary to run_env Success!"
    elif [ ${1} == "authentication" ]; then
        cp -v ${go_dir}/ZhanHui_Server/${1}/${1} ${run_dir}/binary/${1} && green_echo "Copy ${1} binary to run_env Success!"
        cp -arp ${go_dir}/ZhanHui_Server/${1}/public ${run_dir}/binary/${1} 
        cp -v ${go_dir}/ZhanHui_Server/${1}/restful_model.conf ${run_dir}/binary/${1}
        cp -v ${go_dir}/ZhanHui_Server/${1}/restful_policy.csv ${run_dir}/binary/${1}
    elif [ ${1} == "DeviceManager" ]; then
        cp -v ${go_dir}/ZhanHui_Server/${1}/app/onvif/libcamctrl.so ${run_dir}/binary/${1} && green_echo "Copy ${1} libcamctrl.so to run_env Success!"
        cp -v ${go_dir}/ZhanHui_Server/${1}/${1} ${run_dir}/binary/${1} && green_echo "Copy ${1} binary to run_env Success!"
    else
        cp -v ${go_dir}/ZhanHui_Server/${1}/${1} ${run_dir}/binary/${1} && green_echo "Copy ${1} binary to run_env Success!"
    fi
    # start service
    cd ${run_dir} && sudo docker-compose up -d
    if [ $? -ne 0 ]; then
        red_echo "Start ${1} container unsuccessfully"
    else
        green_echo "Start ${1} container successfully"
    fi 
}

function build_go_new() {
    # build
    cp -v ${scripts_dir}/build_go_new.sh ${src_dir}
    docker pull $BUILD_GO_VENDOR_ENV
    yellow_echo "Start to build ${1} code"
    docker run -v ${go_dir}:/workspace/go_service \
    -v ${src_dir}/mod:/workspace/go/pkg/mod \
    -v ${xg_dir}:/workspace/xg_server \
    -v /tmp/pkg:/root/go/pkg \
    -v ${src_dir}/build_go_new.sh:/workspace/build_go_new.sh \
    --name $DOCKER_GO_VENDOR_NAME -i $BUILD_GO_VENDOR_ENV /bin/bash -c "GO111MODULE=on GOPROXY=https://goproxy.cn,direct /workspace/build_go_new.sh ${1}"
    docker rm $DOCKER_GO_VENDOR_NAME &> /dev/null && green_echo "rm build container $DOCKER_GO_VENDOR_NAME Success!"
    # stop service
    cd ${run_dir} && sudo docker stop ${run_name}_${1} &> /dev/null
    if [ $? -ne 0 ]; then
        red_echo "Stop ${1} container unsuccessfully"
    else
        green_echo "Stop ${1} container successfully"
    fi
    # cp bin to run_env
    if [ ${1} == "authentication" ]; then
        cp ${go_dir}/${1}/${1} ${run_dir}/binary/${1} && green_echo "Copy ${1} binary to run_env success."
        cp -arp ${go_dir}/${1}/pubulic ${run_dir}/binary/${1}
        cp ${go_dir}/${1}/restful* ${run_dir}/binary/${1}
    else
        cp ${go_dir}/${1}/${1} ${run_dir}/binary/${1}/ && green_echo "Copy ${1} binary to run_env success."
    fi
    # start service
    cd ${run_dir} && sudo docker-compose up -d
    if [ $? -ne 0 ]; then
        red_echo "Start ${1} container unsuccessfully"
    else
        green_echo "Start ${1} container successfully"
    fi 
}

function build_nvr() {
    # build
    cp -v ${scripts_dir}/build_nvr.sh ${src_dir}
    docker pull $BUILD_NVR_ENV
    yellow_echo "Start to build ${1} code"
    docker run -v ${go_dir}:/workspace/go/src/github.com/Intelligentvision/ \
    -v ${src_dir}/mod:/workspace/go/pkg/mod \
    -v ${src_dir}/build_${1}.sh:/workspace/build_${1}.sh \
    --name $DOCKER_NVR_NAME -i $BUILD_NVR_ENV /bin/bash -c "/workspace/build_${1}.sh ${1}"
    docker rm $DOCKER_NVR_NAME &> /dev/null && green_echo "rm build container $DOCKER_NVR_NAME Success!" 
    # stop service
    cd ${run_dir} && sudo docker stop ${run_name}_${1} &> /dev/null
    if [ $? -ne 0 ]; then
        red_echo "Stop ${1} container unsuccessfully"
    else
        green_echo "Stop ${1} container successfully"
    fi
    # cp bin to run_env
    cp -v ${go_dir}/${1}/HIK_SDK_RPC/server ${run_dir}/binary/${1}/HIK_SDK_RPC/
    if [ $? -ne 0 ]; then
        red_echo "Copy ${1} server unsuccessfully"
    else
        green_echo "Copy ${1} server successfully"
    fi
    cp -arv ${go_dir}/${1}/lib/. ${run_dir}/binary/${1}/lib/
    if [ $? -ne 0 ]; then
        red_echo "Copy ${1} lib unsuccessfully"
    else
        green_echo "Copy ${1} lib successfully"
    fi
    # start service
    cd ${run_dir} && docker-compose up -d
    if [ $? -ne 0 ]; then
        red_echo "Start ${1} container unsuccessfully"
    else
        green_echo "Start ${1} container successfully"
    fi 
}

function build_web_common() {
    # build web
    cp -v ${scripts_dir}/build_web_common.sh ${src_dir}
    docker pull $BUILD_WEB_ENV
    docker run -v ${src_dir}:/workspace \
    --name $DOCKER_WEB_NAME -i $BUILD_WEB_ENV /bin/bash -c "/workspace/build_web_common.sh ${1}"
    docker rm $DOCKER_WEB_NAME &> /dev/null && green_echo "rm build container $DOCKER_WEB_NAME Success!"
    # cp bin to run_env
    [ -e ${run_dir}/openresty/nginx/www/static/config.js ] && cp -v ${run_dir}/openresty/nginx/www/static/config.js ${run_dir}/openresty/nginx/config.js.bak
    if [ ${1} == "CommunitySecurityWebSystem" ]; then
        rm -rf ${run_dir}/openresty/nginx/www/community && mv ${src_dir}/${1}/dist/ ${run_dir}/openresty/nginx/www/community && green_echo "Copy ${1} to run_env Success!"
    elif [ ${1} == "FeiDan_Web" ]; then
        [ -e ${run_dir}/openresty/nginx/www/feidan/config.js ] && cp ${run_dir}/openresty/nginx/www/feidan/config.js ${run_dir}/openresty/nginx/www/config.js.bak
        rm -rf ${run_dir}/openresty/nginx/www/feidan && mv ${src_dir}/${1}/dist ${run_dir}/openresty/nginx/www/feidan && green_echo "Copy ${1} to run_env Success!"
        [ -e ${run_dir}/openresty/nginx/www/config.js.bak ] && mv ${run_dir}/openresty/nginx/www/config.js.bak ${run_dir}/openresty/nginx/www/feidan/config.js
    else
        rm -rf ${run_dir}/openresty/nginx/www/static && mkdir -p ${run_dir}/openresty/nginx/www
        cp -arv ${src_dir}/${1}/dist/. ${run_dir}/openresty/nginx/www && green_echo "Copy ${1} to run_env Success!"
    fi
    [ -e ${run_dir}/openresty/nginx/config.js.bak ] && mv ${run_dir}/openresty/nginx/config.js.bak ${run_dir}/openresty/nginx/www/static/config.js
}

function get_commit_info() {
    log=`cd $run_dir && pwd`
    log=$log/commit.txt
    function get_commit() {
        repo_branch=`git branch | grep "\*" |  awk -F' ' '{print $NF}'`
        commit_all=`git log -1`
        commit_id=`git log -1 | grep "commit" | awk -F' ' '{print $NF}'`
        commit_Author=`git log -1 | grep "Author:" | awk -F': ' '{print $NF}'`
        commit_Date=`git log -1 | grep "Date:" | awk -F':   ' '{print $NF}'`
        commit_msg=`git log -1 | grep -v 'commit\|Author\|Date\|^$' | sed 's/^[ \t]*//g'`

        echo "" >> $log
        echo "=================================================================== " >> $log
        echo "repo name:     | ${1}" >> $log
        echo "------------------------------------------------------------------- " >> $log
        echo "repo branch:   | $repo_branch" >> $log
        echo "------------------------------------------------------------------- " >> $log
        echo "commit id:     | $commit_id" >> $log
        echo "------------------------------------------------------------------- " >> $log
        echo "commit author: | $commit_Author" >> $log
        echo "------------------------------------------------------------------- " >> $log
        echo "commit date:   | $commit_Date" >> $log
        echo "------------------------------------------------------------------- " >> $log
        echo "commit msg:    | $commit_msg" >> $log
        echo "=================================================================== " >> $log
        echo "" >> $log
    }
    echo '' > $log
    for api in $(echo ${!repo_dir[*]})
    do
        if [ -d ${go_dir}/${api} ];then
            cd ${go_dir}/${api}
            get_commit ${api}
            cd - &> /dev/null
        elif [ -d ${src_dir}/${api} ];then
            cd ${src_dir}/${api}
            get_commit ${api}
            cd - &> /dev/null
        elif [ -d ${xg_dir}/${api} ];then
            cd ${xg_dir}/${api}
            get_commit ${api}
            cd - &> /dev/null
        fi
    done
    if [ ! ${1} == "All_Homey" ];then
        grep -B 2 -A 12 ${1} ${run_dir}/commit.txt
    fi
}
echo -e '\n------------------------------\nZhanHui_Server\nZhanHui_Web\nAlarmSystem\nauthentication\nBodyDetect\nDeviceManager\nFtpImage\nGrpcCommon\ngrpc-getway\nImageRetrieve\nMapManager\nnvr\nRtspClient\nSolace\nStaffRepository\nTheGood\nWebSystemImageService\nWatchmen\n------------------------------\n'
read -p "请输入要更新的程序名(例如:ZhanHui_Server,ZhanHui_Web,以空格隔开):" projs

for i in ${projs};do
case ${i} in
  ZhanHui_Server)
    # 复制编译脚本
    cp -v ${scripts_dir}/build_*.sh ${src_dir} && green_echo "Copy scripts success!"
    # 拉取代码
    yellow_echo "Start to pull code"
    log=${logs_dir}/${i}.log
    echo '' > ${log}
    cd ${repo_dir[$i]}
    if [ ! -d ${i} ];then
        git clone http://qujin@git.vision.puppyrobot.com/Intelligentvision/${i}.git
        cd ${repo_dir[$i]}/${i} > /dev/null
        git checkout `eval echo '$'"${i}_branch"` | tee -a ${log}
    else
        cd ${repo_dir[$i]}/${i} > /dev/null
        git clean -f | tee -a ${log}
        git checkout -- . | tee -a ${log}
        git fetch --all | tee -a ${log}
        git reset --hard `eval echo '$'"${i}_branch"` | tee -a ${log}
        git checkout `eval echo '$'"${i}_branch"` | tee -a ${log}
        git pull --rebase | tee -a ${log}
    fi
    green_echo "Pull ${i} code success!"
    # 开始编译
    yellow_echo "Start to build code！"
    for k in ${all_bin_proj}; do
        if [ ${k} == "Solace" ]; then
            docker pull $BUILD_XGFACE_ENV
            docker run -v ${go_dir}/ZhanHui_Server:/workspace/xg_server \
            -v ${src_dir}/mod:/workspace/go/pkg/mod \
            -v ${src_dir}/build_xgface_18.04.sh:/workspace/build_xgface_18.04.sh \
            --runtime=nvidia \
            --name $DOCKER_XGFACE_NAME -i $BUILD_XGFACE_ENV /bin/bash -c "/workspace/build_xgface_18.04.sh"
            docker rm $DOCKER_XGFACE_NAME
        elif [ ${k} == "TheGood" ]; then
            docker pull $BUILD_XGINDEX_ENV
            docker run -v ${go_dir}/ZhanHui_Server:/workspace/xg_server \
            -v ${src_dir}/mod:/workspace/go/pkg/mod \
            -v ${src_dir}/build_xgindex.sh:/workspace/build_xgindex.sh \
            --name $DOCKER_XGINDEX_NAME -i $BUILD_XGINDEX_ENV /bin/bash -c "/workspace/build_xgindex.sh"
            docker rm $DOCKER_XGINDEX_NAME
        elif [ ${k} == "nvr" ]; then
            docker pull $BUILD_NVR_ENV
            docker run -v ${go_dir}/ZhanHui_Server:/workspace/go/src/github.com/Intelligentvision/ \
            -v ${src_dir}/mod:/workspace/go/pkg/mod \
            -v ${src_dir}/build_nvr.sh:/workspace/build_nvr.sh \
            --name $DOCKER_NVR_NAME -i $BUILD_NVR_ENV /bin/bash -c "/workspace/build_nvr.sh ${k}"
            docker rm $DOCKER_NVR_NAME
        elif [ ${k} == "BodyDetect" ]; then
            docker pull $BUILD_BODY_ENV
            docker run -v ${go_dir}/ZhanHui_Server/BodyDetect:/workspace/BodyDetect \
            -v ${src_dir}/mod:/workspace/go/pkg/mod \
            -v ${src_dir}/build_body.sh:/workspace/build_body.sh \
            --runtime=nvidia \
            --name $DOCKER_BODY_NAME -i $BUILD_BODY_ENV /bin/bash -c "/workspace/build_body.sh"
            docker rm $DOCKER_BODY_NAME
        else
            docker pull $BUILD_GO_ENV
            docker run -v ${go_dir}/ZhanHui_Server:/workspace/go/src/github.com/Intelligentvision/ \
            -v ${src_dir}/mod:/workspace/go/pkg/mod \
            -v ${src_dir}/build_go_common.sh:/workspace/build_go_common.sh \
            --name $DOCKER_GO_NAME -i $BUILD_GO_ENV /bin/bash -c "GO111MODULE=on GOPROXY=https://goproxy.cn,direct /workspace/build_go_common.sh ${k}"
            docker rm $DOCKER_GO_NAME
        fi
    done
    #记录commit信息
    get_commit_info ${i}
    # 停服
    cd ${run_dir} && docker-compose stop
    # 拷贝程序到对应路径
    for k in ${all_bin_proj};
    do
        if [ ${k} == "RtspClient" ];then
            cp -v ${go_dir}/ZhanHui_Server/${k}/server/server ${run_dir}/binary/${k} && green_echo "Copy ${k} binary to run_env Success!"
        elif [ ${k} == "nvr" ]; then
            cp -v ${go_dir}/ZhanHui_Server/${k}/HIK_SDK_RPC/server ${run_dir}/binary/${k}/HIK_SDK_RPC/ && green_echo "Copy ${k} binary to run_env Success!"
        elif [ ${k} == "Solace" ]; then
            cp -v ${go_dir}/ZhanHui_Server/Solace/build/xgface_server ${run_dir}/binary/xgface_server/Solace/build/bin && green_echo "Copy ${k} binary to run_env Success!"
        elif [ ${k} == "BodyDetect" ]; then
            cp -v ${go_dir}/ZhanHui_Server/BodyDetect/build/BodyDetect ${run_dir}/binary/${k}/build/ && green_echo "Copy ${k} binary to run_env Success!"
        elif [ ${k} == "TheGood" ]; then
            echo ${run_dir}/binary/index_server_{1..2}/TheGood/service/ | xargs -n 1 cp -v ${go_dir}/ZhanHui_Server/TheGood/service/index_server && green_echo "Copy ${k} binary to run_env Success!"
            echo ${run_dir}/binary/index_server_{1..2}/TheGood/ | xargs -n 1 cp -v ${go_dir}/ZhanHui_Server/TheGood/libxgindex.so && green_echo "Copy libxgindex.so to run_env Success!"
        elif [ ${k} == "authentication" ]; then
            cp -v ${go_dir}/ZhanHui_Server/${k}/${k} ${run_dir}/binary/${k} && green_echo "Copy ${k} binary to run_env Success!"
            cp -arp ${go_dir}/ZhanHui_Server/${k}/public ${run_dir}/binary/${k} 
            cp -v ${go_dir}/ZhanHui_Server/${k}/restful_model.conf ${run_dir}/binary/${k}
            cp -v ${go_dir}/ZhanHui_Server/${k}/restful_policy.csv ${run_dir}/binary/${k}
        elif [ ${k} == "DeviceManager" ]; then
            cp -v ${go_dir}/ZhanHui_Server/${k}/app/onvif/libcamctrl.so ${run_dir}/binary/${k} && green_echo "Copy ${k} libcamctrl.so to run_env Success!"
            cp -v ${go_dir}/ZhanHui_Server/${k}/${k} ${run_dir}/binary/${k} && green_echo "Copy ${k} binary to run_env Success!"
        else
            cp -v ${go_dir}/ZhanHui_Server/${k}/${k} ${run_dir}/binary/${k} && green_echo "Copy ${k} binary to run_env Success!"
        fi
    done
    # 启动服务
    cd ${run_dir} && docker-compose up -d
    # 查看commit信息
    cat ${run_dir}/commit.txt
  ;;
  OperationManage)
    pull_and_clean_build ${i}
    build_go_common ${i}
    get_commit_info ${i}
  ;;
  AliyunVOD)
    pull_and_clean_build ${i}
    build_go_common ${i}
    get_commit_info ${i}
  ;;
  authentication)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  FtpImage)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  LogSync)
    pull_and_clean_build ${i}
    build_go_common ${i}
    get_commit_info ${i}
  ;;
  CaseField)
    pull_and_clean_build ${i}
    build_go_common ${i}
    get_commit_info ${i}
  ;;
  FeiDan)
    pull_and_clean_build ${i}
    build_go_new ${i}
    get_commit_info ${i}
  ;;
  AlarmSystem)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  DeviceManager)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  MapManager)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  nvr)
    pull_and_clean_build ZhanHui_Server
    build_nvr ${i}
    get_commit_info ZhanHui_Server
  ;;
  RtspClient)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  StaffRepository)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  ImageStorage)
    pull_and_clean_build ${i}
    build_go_common ${i}
    get_commit_info ${i}
  ;;
  WebSystemImageService)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  ImageRetrieve)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  grpc-getway)
    pull_and_clean_build ZhanHui_Server
    build_go_common ${i}
    get_commit_info ZhanHui_Server
  ;;
  GrpcCommon)
    pull_and_clean_build ${i}
    get_commit_info ${i}
  ;;
  CommunitySecurityWebSystem)
    pull_and_clean_build ${i}
    build_web_common ${i}
    get_commit_info ${i}
  ;;
  navigation)
    pull_and_clean_build ${i}
    build_web_common ${i}
    get_commit_info ${i}
  ;;
  ZhanHui_Web)
    pull_and_clean_build ${i}
    build_web_common ${i}
    get_commit_info ${i}
  ;;
  FeiDan_Web)
    pull_and_clean_build ${i}
    build_web_common ${i}
    get_commit_info ${i}
  ;;
  Watchmen)
    pull_and_clean_build ${i}
    build_go_common ${i}
    get_commit_info ${i}
  ;;
  AccessAuth)
    pull_and_clean_build ${i}
    #cp AccessAuth code to openresty/nginx
    find ${src_dir}/AccessAuth  -name ".git"| xargs rm -Rf
    cp -rv ${src_dir}/AccessAuth ${run_dir}/openresty/nginx/conf
    if [ $? -ne 0 ]; then
        red_echo "Copy AccessAuth unsuccessfully"
    else
        green_echo "Copy AccessAuth successfully"
    fi
    # update commit.txt
    get_commit_info ${i}
  ;;
  Solace)
    # pull code and clean old build
    pull_and_clean_build ZhanHui_Server
    # build
    cp -v ${scripts_dir}/build_xgface_18.04.sh ${src_dir}
    docker pull $BUILD_XGFACE_ENV
    docker run -v ${go_dir}/ZhanHui_Server:/workspace/xg_server \
    -v ${src_dir}/mod:/workspace/go/pkg/mod \
    -v ${src_dir}/build_xgface_18.04.sh:/workspace/build_xgface_18.04.sh \
    --runtime=nvidia \
    --name $DOCKER_XGFACE_NAME -i $BUILD_XGFACE_ENV /bin/bash -c "/workspace/build_xgface_18.04.sh"
    docker rm $DOCKER_XGFACE_NAME
    # stop service
    cd ${run_dir} && docker stop ${run_name}_xgface &> /dev/null
    # cp bin to run_env
    cp -v ${go_dir}/ZhanHui_Server/Solace/build/xgface_server ${run_dir}/binary/xgface_server/Solace/build/bin && green_echo "Copy xgface_server successfully" || red_echo "Copy xgface_server unsuccessfully"
    [ ! -d ${run_dir}/binary/xgface_server/Solace/data ] && cp -rv ${go_dir}/ZhanHui_Server/xgface_data/data ${run_dir}/binary/xgface_server/Solace/ && green_echo "Copy xgface_data successfully"
    # start service
    cd ${run_dir} && docker-compose up -d
    # update commit.txt
    get_commit_info ZhanHui_Server
  ;;
  TheGood)
    # pull code and clean old build
    pull_and_clean_build ZhanHui_Server
    # build
    cp -v ${scripts_dir}/build_xgindex.sh ${src_dir}
    docker pull $BUILD_XGINDEX_ENV
    docker run -v ${go_dir}/ZhanHui_Server:/workspace/xg_server \
    -v ${src_dir}/mod:/workspace/go/pkg/mod \
    -v ${src_dir}/build_xgindex.sh:/workspace/build_xgindex.sh \
    --name $DOCKER_XGINDEX_NAME -i $BUILD_XGINDEX_ENV /bin/bash -c "/workspace/build_xgindex.sh"
    docker rm $DOCKER_XGINDEX_NAME
    # stop service
    cd ${run_dir} && docker stop ${run_name}_xgindex_{1..2}
    # cp bin to run_env
    echo ${run_dir}/binary/index_server_{1..2}/TheGood/service/ | xargs -n 1 cp -v ${go_dir}/ZhanHui_Server/TheGood/service/index_server && green_echo "Copy index_server successfully" || red_echo "Copy index_server unsuccessfully"
    echo ${run_dir}/binary/index_server_{1..2}/TheGood/ | xargs -n 1 cp -v ${go_dir}/ZhanHui_Server/TheGood/libxgindex.so && green_echo "Copy libxgindex.so successfully" || red_echo "Copy libxgindex.so unsuccessfully"
    # start service
    cd ${run_dir} && docker-compose up -d
    # update commit.txt
    get_commit_info ZhanHui_Server
  ;;
  BodyDetect)
    # pull code and clean old build
    pull_and_clean_build ZhanHui_Server
    # build
    cp -v ${scripts_dir}/build_body.sh ${src_dir}
    docker pull $BUILD_BODY_ENV
    docker run -v ${go_dir}/ZhanHui_Server/BodyDetect:/workspace/BodyDetect \
    -v ${src_dir}/mod:/workspace/go/pkg/mod \
    -v ${src_dir}/build_body.sh:/workspace/build_body.sh \
    --runtime=nvidia \
    --name $DOCKER_BODY_NAME -i $BUILD_BODY_ENV /bin/bash -c "/workspace/build_body.sh"
    docker rm $DOCKER_BODY_NAME
    # stop service
    cd ${run_dir} && docker stop ${run_name}_${i}
    # copy binary to run_env
    cp -v ${go_dir}/ZhanHui_Server/BodyDetect/build/BodyDetect ${run_dir}/binary/BodyDetect/build
    # start service
    cd ${run_dir} && docker-compose up -d
    # update commit.txt
    get_commit_info ZhanHui_Server       
  ;;
  *)
    echo "输入有误！"
  ;;
esac
done