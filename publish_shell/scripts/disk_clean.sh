#!/bin/bash

imgs_dir=/opt/community_system_v0.2_exh/run_env/images_1/camera
avail_disk=$(df -k | grep /$ | awk '{print int($4)}')
if [ ${avail_disk} -le 102400000 ];then
    echo "${avail_disk} less than 100G."
    for((k=2019;k<=2029;k++));
    do
        #echo "year $k"
        for((v=1;v<=12;v++));
        do
        #echo "month $v"
            for((e=1;e<=31;e++));
            do
            #echo "day $e"
                rm -rf ${imgs_dir}/body/${k}/${v}/${e} &> /dev/null
                rm -rf ${imgs_dir}/err/${k}/${v}/${e} &> /dev/null
                rm -rf ${imgs_dir}/face/${k}/${v}/${e} &> /dev/null
                avail_disk=$(df -k /data | grep -v Filesystem | awk '{print int($4)}')
                a=102400000
                for x in ${avail_disk}
                do
                #echo "disk free is $x now"
                    if [ $x -le $a ];then
                        a=$x
                    fi
                done
                echo "small disk free is $a now"
                if [ ${a} -ge 102400000 ];then
                    exit 200
                fi
            done
        done
    done
fi