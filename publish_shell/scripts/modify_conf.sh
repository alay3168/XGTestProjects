#!/bin/bash

local_ip=10.58.150.5
conf_ip=$(grep img_server binary/WebSystemImageService/config.yaml | awk -F'/' '{print $3}')

sed -i "s#${conf_ip}#${local_ip}#g" ./openresty/nginx/conf/nginx.conf &>/dev/null
sed -i "s#${conf_ip}#${local_ip}#g" ./binary/ImageRetrieve/config.yaml &>/dev/null
sed -i "s#${conf_ip}#${local_ip}#g" ./binary/RtspClient/Config.json &>/dev/null
sed -i "s#${conf_ip}#${local_ip}#g" ./binary/WebSystemImageService/config.yaml &>/dev/null
sed -i "s#${conf_ip}#${local_ip}#g" ./binary/LogSync/config.yaml &>/dev/null
sed -i "s#${conf_ip}#${local_ip}#g" ./binary/BodyDetect/build/config.json &>/dev/null
sed -i "s#${conf_ip}#${local_ip}#g" ./.env &>/dev/null