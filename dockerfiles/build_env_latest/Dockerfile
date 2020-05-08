FROM nvidia/cuda:8.0-devel-ubuntu14.04

ADD sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        vim \
        ssh \
        lshw \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        libopenblas-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*


#Install gcc-4.9 g++-4.9 gcc-5 gcc-5 
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository ppa:ubuntu-toolchain-r/test && \
    apt-get update && \
    apt-get install -y gcc-4.9 g++-4.9 && \
    apt-get install -y gcc-5 g++-5 && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/g++-4.9 /usr/bin/g++ -f && \
    ln -s /usr/bin/gcc-4.9 /usr/bin/gcc -f
    

#Install conan
RUN pip install --index https://pypi.tuna.tsinghua.edu.cn/simple/ --ignore-installed conan

ENV PROTOBUF=protobuf-3.5.1
ENV GRPC=grpc

#Install protobuf 3.5
#WORKDIR /tmp
#RUN wget https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-all-3.5.1.tar.gz && \
#    tar -xf protobuf-all-3.5.1.tar.gz
#WORKDIR /tmp/protobuf-3.5.1
#RUN ./configure && make && make check && make install
#WORKDIR /tmp
#RUN rm -r protobuf-3.5.1 && rm protobuf-all-3.5.1.tar.gz

ADD ${PROTOBUF} /tmp/${PROTOBUF}
WORKDIR /tmp/${PROTOBUF}
RUN ./configure && make && make check && make install
WORKDIR /tmp
RUN rm -r protobuf-3.5.1
    

#Install grpc
#RUN git clone https://github.com/grpc/grpc.git && \
#WORKDIR /tmp/grpc
#RUN git submodule update --init && \
#    make -j8 && make install
#WORKDIR /tmp
#RUN rm -rf grpc

ADD grpc /tmp/grpc
WORKDIR /tmp/grpc
#RUN git submodule update --init
RUN apt-get remove -y libprotobuf-dev && export LD_LIBRARY_PATH=/usr/local/lib && make -j8 && make install 
WORKDIR /tmp
RUN rm -rf grpc

#Add lib for xgface
ADD Solace/registry.txt /root/.conan/registry.txt
ADD Solace/conan_data/data /root/.conan/data
ADD Solace/conan /workspace/conan

ADD Solace/libcudnn.so.5 /usr/local/cuda/lib64/  

WORKDIR /workspace/conan
RUN conan install . -r=local

#Add lib for DeviceManager
ADD libcamctrl.so /usr/lib/libcamctrl.so 

#Add web code build environments
ADD node-v8.12.0 /tmp/node-v8.12.0
WORKDIR /tmp/node-v8.12.0
RUN ./configure && make && make install
WORKDIR /tmp
RUN rm -rf node-v8.12.0 

#Install cmake for opencv4.0
Add cmake-3.13.1 /tmp/cmake-3.13.1
WORKDIR /tmp/cmake-3.13.1 
Run ./configure && make && make install
WORKDIR /tmp
RUN rm -rf cmake-3.13.1 

#Install Opencv-3.4.4 for Watchmen
ADD opencv-4.0.0 /tmp/opencv-4.0.0
ADD opencv_contrib-4.0.0 /tmp/opencv_contrib-4.0.0
WORKDIR /tmp/opencv-4.0.0
RUN mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-4.0.0/modules -DOPENCV_GENERATE_PKGCONFIG=ON -DCPU_DISPATCH=AVX .. && \
    make -j $(nproc) && \
    make install
WORKDIR /tmp
RUN rm -rf opencv-4.0.0 && rm -rf opencv_contrib-4.0.0

# Fix bug for can not find opencv lib .so file
RUN echo "/usr/local/lib/x86_64-linux-gnu" > /etc/ld.so.conf.d/opencv.conf && ldconfig

RUN apt-get update && apt-get install -y --no-install-recommends \
        openssl \
        libssl-dev && \
    rm -rf /var/lib/apt/lists/*

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
