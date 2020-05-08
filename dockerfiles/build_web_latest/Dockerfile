FROM ubuntu:14.04

ADD sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        vim \
        python-dev && \
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
 
#Add web code build environments
ADD node-v8.12.0 /tmp/node-v8.12.0
WORKDIR /tmp/node-v8.12.0
RUN ./configure && make && make install
WORKDIR /tmp
RUN rm -rf node-v8.12.0 

WORKDIR /workspace

CMD ['/bin/bash']
