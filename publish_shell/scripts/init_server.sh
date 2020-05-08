#!/bin/bash
function yellow_echo (){
        local what=$*
        echo -e "\e[1;33m-- Info: ${what} \e[0m"
}
function green_echo (){
        local what=$*
        echo -e "\e[1;32m-- Info: ${what} \e[0m"
}

function red_echo (){
        local what=$*
        echo -e "\e[1;31m-- Error: ${what} \e[0m"
}
# 修改源为阿里云源
mv /etc/apt/sources.list /etc/apt/sources.list.bak
cat >> /etc/apt/sources.list << EOF
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
EOF
green_echo "change sources to aliyun sources success!"
apt remove nano -y
# 安装阿里云监控插件
CMS_AGENT_ACCESSKEY=4Rnm4mmTSOo CMS_AGENT_SECRETKEY=r2AIcoFTyfpExi7WaOh9Ug VERSION=2.1.56 /bin/bash -c "$(curl -s http://cms-download.aliyun.com/cms-go-agent/cms_go_agent_install_necs-1.4.sh)"
# sudo免密
sed -i '/user/d' /etc/sudoers
sed -i '/%sudo/auser\    ALL=(ALL)\    NOPASSWD:\ ALL' /etc/sudoers
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
systemctl restart ssh
green_echo "sudo nopass success!"
# 固定默认启动内核
uuid=$(grep 'root=UUID=' /boot/grub/grub.cfg|head -1|awk {'print $3'}|awk -F= {'print $3'})
boot_uid="gnulinux-advanced-$uuid>gnulinux-$(uname -r)-advanced-$uuid"
sed -i "s/GRUB_DEFAULT=0/GRUB_DEFAULT=\"${boot_uid}\"/" /etc/default/grub
update-grub
green_echo "hold start-kernel success!"
# 固定主机名不随升级内核而改变
[ -e /etc/cloud/cloud.cfg ] && sed -i 's/preserve_hostname: false/preserve_hostname: true/' /etc/cloud/cloud.cfg
# 设置网卡等配置检查等待时间
sed -i '/TimeoutStartSec=2sec/d' /etc/systemd/system/network-online.target.wants/systemd-networkd-wait-online.service
sed -i '/RemainAfterExit=yes/a TimeoutStartSec=2sec' /etc/systemd/system/network-online.target.wants/systemd-networkd-wait-online.service
sed -i '/DefaultTimeoutStartSec=10s/d' /etc/systemd/system.conf
sed -i '/DefaultTimeoutStopSec=10s/d' /etc/systemd/system.conf
sed -i '$aDefaultTimeoutStartSec=10s' /etc/systemd/system.conf
sed -i '$aDefaultTimeoutStopSec=10s' /etc/systemd/system.conf
systemctl daemon-reload
# 修改用户密码
echo 'user:HAchi@3344' | chpasswd user
green_echo "修改user密码成功！"
# 修改root密码
echo 'root:1qaz3edc' | chpasswd root
green_echo "修改root密码成功！"
# 设置frpc
[ -e /etc/systemd/system/frpc.service ] && sed -i '1,$d' /etc/systemd/system/frpc.service
cat >> /etc/systemd/system/frpc.service << EOF
[Unit]
Description=Frp Client Daemon
After=syslog.target network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/data/frp_0.27.0_linux_amd64/frpc -c /data/frp_0.27.0_linux_amd64/frpc.ini
ExecStop=/usr/bin/killall frpc
#启动失败1分钟后再次启动
RestartSec=1min
KillMode=control-group
#重启控制：总是重启
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl enable frpc
green_echo "setup frpc success!"
# 启用rc.local
[ -e /etc/systemd/system/rc-local.service ] && rm -f /etc/systemd/system/rc-local.service
cat >> /etc/systemd/system/rc-local.service << EOF
[Unit]
Description=/etc/rc.local Compatibility
ConditionPathExists=/etc/rc.local
 
[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99
 
[Install]
WantedBy=multi-user.target
EOF
[ -e /etc/rc.local ] && rm -f /etc/rc.local
cat >> /etc/rc.local << EOF
#!/bin/bash
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

cd /data/homey2.2_190730/run_env && docker-compose up -d

exit 0
EOF
chmod +x /etc/rc.local && sudo systemctl enable rc-local
green_echo "enable rc.local success!"
# 设置时区
timedatectl set-local-rtc 1 --adjust-system-clock && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
green_echo "set timezone success!"
# 创建磁盘清理脚本
rm -f /data/disk_clean.sh
cat >> /data/disk_clean.sh << EOF
#!/bin/bash
imgs_dir=/data/homey2.2_190730/images_1/camera
avail_disk=\$(df -k | grep /data$ | awk '{print int(\$4)}')
if [ \${avail_disk} -le 102400000 ];then
    echo "\${avail_disk} less than 100G."
    for((k=2019;k<=2029;k++));
    do
        #echo "year \$k"
        for((v=1;v<=12;v++));
        do
        #echo "month \$v"
            for((e=1;e<=31;e++));
            do
            #echo "day \$e"
                rm -rf \${imgs_dir}/body/\${k}/\${v}/\${e} &> /dev/null
                rm -rf \${imgs_dir}/err/\${k}/\${v}/\${e} &> /dev/null
                rm -rf \${imgs_dir}/face/\${k}/\${v}/\${e} &> /dev/null
                avail_disk=\$(df -k | grep /data$ | awk '{print int(\$4)}')
                a=102400000
                for x in \${avail_disk}
                do
                #echo "disk free is \$x now"
                    if [ \$x -le \$a ];then
                        a=\$x
                    fi
                done
                echo "small disk free is \$a now"
                if [ \${a} -ge 102400000 ];then
                    exit 200
                fi
            done
        done
    done
fi
EOF
chmod +x /data/disk_clean.sh
green_echo "create disk clean script success!"
# 创建磁盘清理计划任务
[ -e /var/spool/cron/crontabs/root ] && sed -i '/disk_clean.sh$/d' /var/spool/cron/crontabs/root
touch /var/spool/cron/crontabs/root
echo '0 3 * * 6 sudo /data/disk_clean.sh' >> /var/spool/cron/crontabs/root
green_echo "create disk clean crontabs success!"
# 拉取必要软件包
cd /data
# [ ! -e NVIDIA-Linux-x86_64-430.26.run ] && wget http://10.58.122.61:8000/other/NVIDIA-Linux-x86_64-430.26.run && chmod +x NVIDIA-Linux-x86_64-430.26.run
[ ! -e frp_0.27.0_linux_amd64 ] && wget http://10.58.122.61:8000/other/frp_0.27.0_linux_amd64.tgz && tar xvf frp_0.27.0_linux_amd64.tgz
[ ! -e homey2.2_190730 ] && wget http://10.58.122.61:8000/rms/rms_local.tgz && tar xvf rms_local.tgz
rm -rf frp_0.27.0_linux_amd64.tgz rms_local.tgz
green_echo "get all needs apps success!"
#安装docker
yellow_echo "Start to install docker"
apt-get update
apt-get -y install apt-transport-https ca-certificates curl software-properties-common ntp ubuntu-drivers-common
timedatectl set-ntp no
systemctl enable ntp
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | \
  apt-key add -
add-apt-repository "deb [arch=amd64] \
  http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
apt-get -y update
apt-get -y install docker-ce
if [ $? -ne 0 ]; then
    red_echo "Failed to install docker"
    exit -1
else
    green_echo "Install docker successfully"
fi
#安装docker-compose
yellow_echo "Start to install docker-compose"
apt-get install wget && cd /usr/local/bin && rm -f docker-compose && wget http://10.58.122.61:8000/other/docker-compose && chmod +x ./docker-compose
if [ $? -ne 0 ]; then
    red_echo "Failed to install docker-compose"
    exit -1
else
    green_echo "Install docker-compose successfully"
fi
#安装nvidia-docker
yellow_echo "Start to install nvidia-docker"
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update && apt-get install -y nvidia-docker2
if [ $? -ne 0 ]; then
    red_echo "Failed to install nvidia-docker2"
    exit -1
else
    green_echo "Install nvidia-docker2 successfully"
fi
pkill -SIGHUP dockerd
#向docker daemon添加registry config
yellow_echo "Start to modify docker daemon.json"
sed -i "/\"runtimes\":/i\    \"insecure-registries\":[\"10.58.122.61:90\"],"  /etc/docker/daemon.json
if [ $? -ne 0 ]; then
    red_echo "Failed to modify docker daemon.json"
    exit -1
else
    green_echo "Modify docker daemon.json successfully"
fi
#docker命令免sudo,执行一下命令然后重新登录
gpasswd -a $(grep 1000 /etc/passwd | awk -F: '{print $1}') docker
service docker restart
if [ $? -ne 0 ]; then
    red_echo "Failed to restart docker"
    exit -1
else
    green_echo "Restart docker successfully"
fi
# 拉取镜像
cd /data/homey2.2_190730/run_env && docker-compose pull
# 安装显卡驱动
apt install nvidia-driver-440 -y
# autoremove
apt-get autoremove -y