#!/bin/bash

# ======================================================================================
# This script is used for packing run env
# ======================================================================================

# Initialize run env directory
. ./echo_color.sh
run_dir=$(cd ../../run_env && pwd)
pjname=homey2.3
rm -rf ../run_env_package && mkdir -p ../run_env_package
package_dir=$(cd ../run_env_package/ && pwd)
gobin_dir=$(mkdir -p ${package_dir}"/${pjname}_$(date +%y%m%d)/"run_env/binary && cd ${package_dir}"/${pjname}_$(date +%y%m%d)/"run_env/binary && pwd)
pkg_run_dir=$(cd ${gobin_dir}/../ && pwd)

yellow_echo "Start to initialize package environment"
mkdir -p ${pkg_run_dir}/mysql/conf ${pkg_run_dir}/openresty
if [ $? -ne 0 ]; then
    red_echo "Make directory unsuccessfully"
    exit -1
else
    green_echo "Make directory successfully"
fi

# Copy run_env go binary to package directory
run=$(ls -F ${run_dir}/binary | grep /$)
for i in ${run}; do
    cp -arpv ${run_dir}/binary/${i} ${gobin_dir}
done
if [ $? -ne 0 ]; then
    red_echo "Copy run_env go binary to package directory unsuccessfully"
    exit -1
else
    green_echo "Copy run_env go binary to package directory successfully"
fi

# Copy common configure files to run env
cp ${run_dir}/*.sh ${pkg_run_dir}
if [ $? -ne 0 ]; then
    red_echo "Copy scripts unsuccessfully"
    exit -1
fi
[ -e ${run_dir}/commit.txt ] && cp ${run_dir}/commit.txt ${pkg_run_dir}
if [ $? -ne 0 ]; then
    red_echo "Copy commit.txt unsuccessfully"
    exit -1
fi
cp ${run_dir}/docker-compose.yml ${run_dir}/.env ${pkg_run_dir}
if [ $? -ne 0 ]; then
    red_echo "Copy docker-compose.yml modify_conf.sh .env unsuccessfully"
    exit -1
fi
cp ${run_dir}/mysql/conf/my.cnf ${pkg_run_dir}/mysql/conf
if [ $? -ne 0 ]; then
    red_echo "Copy my.cnf unsuccessfully"
    exit -1
fi
cp -arp ${run_dir}/openresty/nginx ${pkg_run_dir}/openresty
if [ $? -ne 0 ]; then
    red_echo "Copy nginx files unsuccessfully"
    exit -1
fi
[ -d ${run_dir}/apache-tomcat-9.0.7 ] && cp -arp ${run_dir}/apache-tomcat-9.0.7 ${pkg_run_dir}

# Delete some files
rm -rf ${gobin_dir}/index_server_*/*.log
rm -rf ${gobin_dir}/index_server_*/TheGood/service/indexDb
rm -rf ${gobin_dir}/xgface_server/*.log
rm -rf ${gobin_dir}/BodyDetect/*.log
rm -rf ${gobin_dir}/BodyDetect/build/BodyDetect_log*
rm -rf ${gobin_dir}/AlarmSystem/*.txt
rm -rf ${gobin_dir}/StaffRepository/log.txt*
rm -rf ${gobin_dir}/WebSystemImageService/*.log
rm -rf ${pkg_run_dir}/openresty/nginx/www/map
rm -rf ${pkg_run_dir}/openresty/nginx/logs
rm -rf ${pkg_run_dir}/openresty/nginx/www/rtsp

chown -R $(whoami). ${package_dir}

yellow_echo "Finish copying binary to run environments"
# --------------------------------------------------------------------------------------
# Pack run env to tar package
yellow_echo " Start to packing."
cd ${package_dir} && tar -zcf ${pjname}_$(date +%y%m%d).tgz ${pjname}_$(date +%y%m%d)
green_echo "Finish packing."
