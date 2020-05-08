#!/bin/bash
function yellow_echo ()
{
        local what=$*
        echo -e "\e[1;33m-- Info: ${what} \e[0m"
}

function green_echo ()
{
        local what=$*
        echo -e "\e[1;32m-- Info: ${what} \e[0m"
}

function red_echo ()
{
        local what=$*
        echo -e "\e[1;31m-- Error: ${what} \e[0m"
}
sudo df | grep -q /opt
if [ $? -ne 0 ];then
    parted -s /dev/sda mklabel gpt
    blockdev --rereadpt /dev/sda
    parted -s /dev/sda mkpart primary 1 1000G
    echo y | mkfs.ext4 /dev/sda1
    sed -i '#/dev/sda1#d' /etc/fstab
    echo '/dev/sda1	/opt	ext4	defaults	0	0' >> /etc/fstab
    mount -a && rm -rf /opt/lost+found
fi
# 关闭自动更细软件
sed -i '1,$d' /etc/apt/apt.conf.d/10periodic
cat >> /etc/apt/apt.conf.d/10periodic << EOF
APT::Periodic::Update-Package-Lists "0"; //显示更新包列表 0表示停用设置
APT::Periodic::Download-Upgradeable-Packages "0"; //下载更新包 0表示停用设置
APT::Periodic::AutocleanInterval "0"; // 7日自动删除
APT::Periodic::Unattended-Upgrade "0"; //启用自动更新 0表示停用自动更新
EOF
# 修改源为阿里云源
rm -f /etc/apt/sources.list
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
# 修改启动关闭程序等待时间
sed -i '/DefaultTimeoutStartSec=10s/d' /etc/systemd/system.conf
sed -i '/DefaultTimeoutStopSec=10s/d' /etc/systemd/system.conf
sed -i '$aDefaultTimeoutStartSec=10s' /etc/systemd/system.conf
sed -i '$aDefaultTimeoutStopSec=10s' /etc/systemd/system.conf
systemctl daemon-reload
# 创建磁盘清理脚本
rm -f /home/puppy/disk_clean.sh /home/puppy/watch-gnome-shell.sh
cat >> /home/puppy/disk_clean.sh << EOF
#!/bin/bash
imgs_dir=/opt/exhibition_191218/run_env/images_1/camera
avail_disk=\$(df -k | grep /opt$ | awk '{print int(\$4)}')
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
                avail_disk=\$(df -k | grep /opt$ | awk '{print int(\$4)}')
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
chmod +x /home/puppy/disk_clean.sh
cat >> /home/puppy/watch-gnome-shell.sh << EOF
#!/bin/bash
tmpPid=\$(pidof gnome-shell|awk '{print \$1}')
tmpNum=\$(top -n 1 -p \$tmpPid|grep gnome-shell|awk '{print \$(NF-4)}')
if [ \$(echo "\$tmpNum > 60" | bc) -eq 1 ]
then
  kill -9 \$tmpPid && echo "\$(date +%c) restart gnome-shell.">>/home/puppy/gnome-shell.out
fi
EOF
chmod +x /home/puppy/watch-gnome-shell.sh
green_echo "create scriptS success!"
# 创建计划任务
[ -e /var/spool/cron/crontabs/root ] && sed -i '/disk_clean.sh$/d' /var/spool/cron/crontabs/root
[ -e /var/spool/cron/crontabs/root ] && sed -i '/watch-gnome-shell.sh$/d' /var/spool/cron/crontabs/root
echo '0 3 * * 6 sudo /home/puppy/disk_clean.sh' >> /var/spool/cron/crontabs/root
echo '*/1 * * * * /home/puppy/watch-gnome-shell.sh' >> /var/spool/cron/crontabs/root
green_echo "create crontabs success!"
# 安装必要软件
apt-get update
apt-get install xorg ubuntu-desktop openssh-server vim chromium-browser ntp vlc ubuntu-drivers-common -y 
apt-get build-dep gcc -y
apt-get remove nano update-manager -y
timedatectl set-ntp no
systemctl enable ntp
green_echo "install packages success!"
# sudo免密
sed -i '/^puppy/d' /etc/sudoers
sed -i '/%sudo/apuppy\    ALL=(ALL)\    NOPASSWD:\ ALL' /etc/sudoers
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
systemctl restart ssh
green_echo "sudo nopass success!"
# 修改root密码
echo 'root:1qaz3edc'|chpasswd root
if [ $? -eq 0 ]
then
    green_echo "change root password success"
fi
# 固定默认启动内核
#uuid=$(grep 'root=UUID=' /boot/grub/grub.cfg|head -1|awk {'print $3'}|awk -F= {'print $3'})
#boot_uid="gnulinux-advanced-$uuid>gnulinux-$(uname -r)-advanced-$uuid"
#sed -i "s/GRUB_DEFAULT=0/GRUB_DEFAULT=\"${boot_uid}\"/" /etc/default/grub
#update-grub
#green_echo "hold start-kernel success!"

# 固定主机名不随升级内核而改变
[ -e /etc/cloud/cloud.cfg ] && sed -i 's/preserve_hostname: false/preserve_hostname: true/' /etc/cloud/cloud.cfg
# 设置frpc
[ -e /etc/systemd/system/frpc.service ] && sed -i '1,$d' /etc/systemd/system/frpc.service
cat >> /etc/systemd/system/frpc.service << EOF
[Unit]
Description=Frp Client Daemon
After=syslog.target network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/opt/frp_0.27.0_linux_amd64/frpc -c /opt/frp_0.27.0_linux_amd64/frpc.ini
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
# 禁用第三方显卡驱动
[ -e /etc/modprobe.d/blacklist-nouveau.conf ] && sed -i '1,$d' /etc/modprobe.d/blacklist-nouveau.conf
cat >> /etc/modprobe.d/blacklist-nouveau.conf << EOF
blacklist nouveau
options nouveau modeset=0
EOF
update-initramfs -u
green_echo "block third graphics driver success!"
# 启用rc.local并自启展示系统
[ -e /etc/systemd/system/rc-local.service ] && sed -i '1,$d' /etc/systemd/system/rc-local.service
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
[ -e /etc/rc.local ] && sed -i '1,$d' /etc/rc.local
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

#cd /opt/exhibition_191218/run_env && sudo docker-compose up -d
exit 0
EOF
chmod +x /etc/rc.local && sudo systemctl enable rc-local
green_echo "enable rc.local success!"
# 设置时区
timedatectl set-local-rtc 1 --adjust-system-clock && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
green_echo "set timezone success!"
# 拉取必要软件包
[ ! -e /home/puppy/Desktop/ad.mp4 ] && cd /home/puppy/Desktop && wget http://10.58.122.61:8000/ad.mp4
cd /opt
[ ! -d teamviewer ] && wget http://10.58.122.61:8000/teamviewer_14.6.2452_amd64.deb && apt install ./teamviewer_14.6.2452_amd64.deb -y
# [ ! -e NVIDIA-Linux-x86_64-430.26.run ] && wget http://10.58.122.61:8000/other/NVIDIA-Linux-x86_64-430.26.run && chmod +x NVIDIA-Linux-x86_64-430.26.run
# [ ! -e videoanalyse ] && wget http://10.58.122.61:8000/videoanalyse/videoanalyse.tgz && tar xvf videoanalyse.tgz
[ ! -e faceshow ] && wget http://10.58.122.61:8000/faceshow/faceshow.tgz && tar xvf faceshow.tgz && /opt/faceshow/desktop_start/desktop.install
[ ! -e frp_0.27.0_linux_amd64 ] && wget http://10.58.122.61:8000/other/frp_0.27.0_linux_amd64.tgz && tar xvf frp_0.27.0_linux_amd64.tgz
[ ! -e exhibition_191218 ] && wget http://10.58.122.61:8000/exhibition/v0.6/exhibition_191218.tgz && tar xvf exhibition_191218.tgz
rm -rf exhibition_191218.tgz frp_0.27.0_linux_amd64.tgz videoanalyse.tgz teamviewer_14.6.2452_amd64.deb faceshow.tgz
green_echo "get all needs apps success!"
#安装docker
yellow_echo "Start to install docker"
apt-get -y install apt-transport-https ca-certificates curl software-properties-common
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
# apt-get -y install python-pip
# pip install docker-compose
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
https_proxy="socks5://10.58.120.49:10808" && apt-get update && apt-get install -y nvidia-docker2
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
# 拉取docker镜像
cd /opt/exhibition_191218/run_env && docker-compose pull
# docker pull 10.58.122.61:90/production/videoanalyse:0.14
docker pull 10.58.122.61:90/build/faceshow:v3
green_echo "pull docker images success!"
# 安装显卡驱动
apt install nvidia-driver-440 -y
# autoremove
apt-get autoremove -y