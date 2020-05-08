#!/bin/bash
# 执行方式：sudo chmod +x watchDogGeoServer.sh && nohup ./watchDogGeoServer.sh &  
# 该程序会常驻后台，15秒钟检测一次geoserver的状态，pending10秒则重启geoserver，谨慎使用。

uri=https://10.58.122.61:444
container_id=$(sudo docker ps -a | grep geoserver | grep -v grep | awk '{print $1}')
while true;
do
    status_code=$(echo `curl -o /dev/null -s -k -m 10 --connect-timeout 10 -w %{http_code} "${uri}/xgmap/wfs?outputFormat=application%2Fjson&request=GetFeature&service=wfs&srsname=EPSG:4326&typeNames=test:devices&version=1.1.0&_=1551781761602"`)
    #echo "$status_code"
    if [ $status_code -ne 200 ];
    then
      sudo docker stop "$i" && sudo docker rm "$i" && cd "$run_env" && \
      sudo docker-compose up -d && echo "$(date +%F' '%T) restart geoserver sucess!">>watchDogGeoserver.out
    fi
    sleep 15
done