#!/bin/bash

docker-compose down && \
rm -rf faceimage nsq mysql/data redis ftp \
../ftp \
../images_1 \
openresty/nginx/www/map \
openresty/nginx/logs \
openresty/nginx/www/rtsp \
binary/ftp \
binary/*.log \
binary/AlarmSystem/alarm*.txt \
binary/StaffRepository/log.txt* \
binary/WebSystemImageService/*.log \
binary/BodyDetect/build/BodyDetect_log.* \
binary/index_server_*/*.log \
binary/index_server_*/TheGood/service/indexDb \
binary/xgface_server/Solace/build/bin/*.log && \
echo "flush data sucess!"