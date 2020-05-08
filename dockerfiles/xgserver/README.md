### 用来构建xgface和xgindex编译环境docker镜像

- 构建步骤


```
# 1.拷贝grpc到当前目录
scp -r user@10.58.122.61:/home1/share_files/grpc .

# 2.构建镜像
docker build -t ${image_name}:${tag} .
```
