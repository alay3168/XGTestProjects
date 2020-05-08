---
### 测试环境和生产环境部署脚本

---


#### 环境配置
1. 安装Docker
```
curl -sSL https://get.docker.com/ | sh 
sudo usermod -aG docker username #username为server的用户名，需要重新登录server生效
sudo service docker start
```

2. 安装docker-compose
```
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. 安装nvidia-docker2
参考：https://github.com/NVIDIA/nvidia-docker
```
# Add the package repositories
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

# Install nvidia-docker2 and reload the Docker daemon configuration
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
```

4. 获取部署脚本
```
git clone git@47.111.178.139:Intelligentvision/publish_shell.git

#### 操作步骤
1. 进入脚本目录
```
cd publish_shell/scripts
```

2. 修改配置文件
```
# 修改映射到主机的端口和图片保存路径
vim publish_shell/configs/.env

# 修改设备管理服务端口，修改对应的mysql和redis端口（与publish_shell/configs/.env中mysql和redis映射到主机的端口一致）
vim publish_shell/configs/api_config/conf_DeviceManager.yaml

# 修改nginx.conf中设备管理服务端口(与设备管理服务配置文件一致)
vim publish_shell/configs/nginx.conf

                  location /api/v1/devices   {
                          proxy_pass http://10.58.122.61:9002;
```

3. 初始化构建环境(只需要运行一次)
```
# 在publish_shell目录下生成目录src，并将所有服务源码clone到该目录下
./init_build_env.sh 
```

4. 初始化运行环境(只需要运行一次)
```
# 自动创建运行环境目录run_env，与publish_shell同级
./init_run_env.sh
```

5. 拉取所有服务最新源码
```
./pull_code.sh
```

6. 构建服务并拷贝服务二进制到测试环境或生产环境
```
./publish.sh
```

7. 启动所有服务
```
cd run_env # 与publish_shell同级
docker-compose up -d
```

TODO:
不同server运行环境初始化配置和部署
