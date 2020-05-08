## Dockerfiles


### 1. Build environment image

#### build env docker image for xgface
```
# go to build directory
cd ./dockerfiles/build_xgface_latest/

# get required software from file server
./get_package.sh

# build docker image with name build_xgface and tag latest
docker build -t build_xgface:latest .

# push docker image to harbor docker registry
docker tag build_xgface:latest 10.58.122.61:90/build/build_xgface:latest
docker push 10.58.122.61:90/build/build_xgface:latest
```

#### build env docker image for xgindex
```
# go to build directory
cd ./dockerfiles/build_xgindex_latest/

# get required software from file server
./get_package.sh

# build docker image with name build_xgindex and tag latest
docker build -t build_xgindex:latest .

# push docker image to harbor docker registry
docker tag build_xgindex:latest 10.58.122.61:90/build/build_xgindex:latest
docker push 10.58.122.61:90/build/build_xgindex:latest
```

#### build env docker image for web
```
# go to build directory
cd ./dockerfiles/build_web_latest/

# get required software from file server
./get_package.sh

# build docker image with name build_web and tag latest
docker build -t build_web:latest .

# push docker image to harbor docker registry
docker tag build_web:latest 10.58.122.61:90/build/build_web:latest
docker push 10.58.122.61:90/build/build_web:latest
```

#### build env docker image for watchmen
```
# go to build directory
cd ./dockerfiles/build_watchmen_latest/

# get required software from file server
./get_package.sh

# build docker image with name build_watchmen and tag latest
docker build -t build_watchmen:latest .

# push docker image to harbor docker registry
docker tag build_watchmen:latest 10.58.122.61:90/build/build_watchmen:latest
docker push 10.58.122.61:90/build/build_watchmen:latest
```

#### build env docker image for nvr
```
# go to build directory
cd ./dockerfiles/build_nvr_latest/

# get required software from file server
./get_package.sh

# build docker image with name build_nvr and tag latest
docker build -t build_nvr:latest .

# push docker image to harbor docker registry
docker tag build_nvr:latest 10.58.122.61:90/build/build_nvr:latest
docker push 10.58.122.61:90/build/build_nvr:latest
```

#### build env docker image for go
```
# go to build directory
cd ./dockerfiles/build_go_latest/

# get required software from file server
./get_package.sh

# build docker image with name build_go and tag latest
docker build -t build_go:latest .

# push docker image to harbor docker registry
docker tag build_go:latest 10.58.122.61:90/build/build_go:latest
docker push 10.58.122.61:90/build/build_go:latest
```

### 2. Running environment image

#### XgFace running docker image 
```
# Go to xgface directory
cd ./dockerfiles/xgface_env

# Get grpc and protobuf from file server
./get_package.sh

# Build docker image with name xgface_env and tag latest
docker build -t xgface_env:latest .

# Push docker image to Harbor docker registry
docker tag xgface_env:latest 10.58.122.61:90/production/xgface_env:latest
docker push 10.58.122.61:90/production/xgface_env:latest
```

#### XgIndex running docker image 
```
# Go to xgindex directory
cd ./dockerfiles/xgindex_env

# Get grpc and protobuf from file server
./get_package.sh

# Build docker image with name xgindex_env and tag latest
docker build -t xgindex_env:latest .

# Push docker image to Harbor docker registry
docker tag xgindex_env:latest 10.58.122.61:90/production/xgindex_env:latest
docker push 10.58.122.61:90/production/xgindex_env:latest
```

#### Go service running docker image 
- Tag v1 is used for DeviceManager which build with dynamic link
```
# Go to directory 
cd dockerfiles/service_env_v1

# Build docker image with name service_env and tag v1
docker build -t service_env:v1 .

# Push docker image to Harbor docker registry
docker tag service_env:v1 10.58.122.61:90/production/service_env:v1
docker push 10.58.122.61:90/production/service_env:v1
```

- Tag v2 is used for other go service which build with static link
```
# Go to directory 
cd dockerfiles/service_env_v2

# Build docker image with name service_env and tag v2
docker build -t service_env:v2 .

# Push docker image to Harbor docker registry
docker tag service_env:v2 10.58.122.61:90/production/service_env:v2
docker push 10.58.122.61:90/production/service_env:v2
```

- Tag v3 is used for other go service with opencv 
```
# Go to directory 
cd dockerfiles/service_env_v3

# Get required software from file server
./get_package.sh

# Build docker image with name service_env and tag v2
docker build -t service_env:v3 .

# Push docker image to Harbor docker registry
docker tag service_env:v2 10.58.122.61:90/production/service_env:v3
docker push 10.58.122.61:90/production/service_env:v3
```

- Tag nvr is used for nvr service
```
# Go to directory 
cd dockerfiles/service_env_nvr

# Get required software from file server
./get_package.sh

# Build docker image with name service_env and tag nvr
docker build -t service_env:nvr .

# Push docker image to Harbor docker registry
docker tag service_env:nvr 10.58.122.61:90/production/service_env:nvr
docker push 10.58.122.61:90/production/service_env:nvr
```


#### Mysql running docker image
```
# Go to mysql directory 
cd dockerfiles/mysql_env/5.6

# Build docker image with name mysql_env and tag latest
docker build -t mysql_env:latest .

# Push docker image to Harbor docker registry
docker tag mysql_env:latest 10.58.122.61:90/production/mysql_env:latest
docker push 10.58.122.61:90/production/mysql_env:latest
```

#### Redis running docker image
```
# Go to redis directory 
cd dockerfiles/redis_env

# Build docker image with name redis_env and tag latest
docker build -t redis_env:latest .

# Push docker image to Harbor docker registry
docker tag redis_env:latest 10.58.122.61:90/production/redis_env:latest
docker push 10.58.122.61:90/production/redis_env:latest
```

#### Openresty running docker image
```
# Go to Openresty directory 
cd dockerfiles/Openresty_env

# Build docker image with name openresty_env and tag latest
docker build -t openresty_env:latest .

# Push docker image to Harbor docker registry
docker tag openresty_env:latest 10.58.122.61:90/production/openresty_env:latest
docker push 10.58.122.61:90/production/openresty_env:latest
```

#### Nsq running docker image
```
# Go to nsq directory 
cd dockerfiles/nsq_env

# Build docker image with name nsq_env and tag latest
docker build -t nsq_env:latest .

# Push docker image to Harbor docker registry
docker tag nsq_env:latest 10.58.122.61:90/production/nsq_env:latest
docker push 10.58.122.61:90/production/nsq_env:latest
```

#### Xgmap running docker image
```
# Go to xgmap directory 
cd dockerfiles/xgmap_env

# Build docker image with name xgmap_env and tag latest
docker build -t xgmap_env:latest .

# Push docker image to Harbor docker registry
docker tag xgmap_env:latest 10.58.122.61:90/production/xgmap_env:latest
docker push 10.58.122.61:90/production/xgmap_env:latest
```

