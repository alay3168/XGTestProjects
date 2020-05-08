FROM ubuntu:14.04

ADD sources.list /etc/apt/sources.list

RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    # gdal-bin used for MapManager
    gdal-bin && \
    rm -rf /var/lib/apt/lists/*

#Install gcc-4.9 g++-4.9 gcc-5 gcc-5 
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    apt-get update && \
    apt-get install -y gcc-4.9 g++-4.9 && \
    apt-get install -y gcc-5 g++-5 && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/g++-4.9 /usr/bin/g++ -f && \
    ln -s /usr/bin/gcc-4.9 /usr/bin/gcc -f
 
#Add lib for DeviceManager
ADD libcamctrl.so /usr/lib/libcamctrl.so 

#Go environment
ADD go_path/go /workspace/go
ADD go_root/go /usr/local/go

RUN echo 'export GOPATH=/workspace/go' >> /etc/profile && \
    echo 'export GOROOT=/usr/local/go' >> /etc/profile && \
    echo 'export PATH=$PATH:$GOROOT/bin' >> /etc/profile && \
    echo 'source /etc/profile' >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc"

WORKDIR /workspace

CMD ['/bin/bash']
