FROM ubuntu:14.04

ADD sources.list /etc/apt/sources.list

RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        vim \
        ssh \
        lshw \
        autoconf \
        automake \
        libtool \
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

#Install gcc-4.9 g++-4.9
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    apt-get update && \
    apt-get install -y gcc-4.9 g++-4.9 && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/g++-4.9 /usr/bin/g++ -f && \
    ln -s /usr/bin/gcc-4.9 /usr/bin/gcc -f
    
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
RUN git submodule update --init
RUN apt-get remove -y libprotobuf-dev && export LD_LIBRARY_PATH=/usr/local/lib && make -j8 && make install 
WORKDIR /tmp
RUN rm -rf grpc

RUN apt-get update && apt-get install -y --no-install-recommends \
        openssl \
        libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ['/bin/bash']
