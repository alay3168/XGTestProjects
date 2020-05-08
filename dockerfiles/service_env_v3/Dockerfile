FROM ubuntu:14.04

ADD sources.list /etc/apt/sources.list

RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# Refer to https://docs.opencv.org/3.4.0/d7/d9f/tutorial_linux_install.html for install opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    python-dev \
    python-numpy \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    libdc1394-22-dev && \
    rm -rf /var/lib/apt/lists/*

#Install gcc-5.0 g++-5.0
ADD gcc-5.5.0 /tmp/gcc-5.5.0 
WORKDIR /tmp/gcc-5.5.0
RUN ./contrib/download_prerequisites 
WORKDIR /tmp/gcc-build-5.5.0
RUN ../gcc-5.5.0/configure --enable-checking=release --enable-languages=c,c++ --disable-multilib && make -j ${nproc} && make install
RUN cp /usr/local/lib64/libstdc++.so.6.0.21  /usr/lib/x86_64-linux-gnu && \
    rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && \
    ln -s /usr/local/lib64/libstdc++.so.6.0.21 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
WORKDIR /tmp
RUN rm -r gcc-5.5.0 && rm -r gcc-build-5.5.0
 
#Install cmake for opencv4.0
Add cmake-3.13.1 /tmp/cmake-3.13.1
WORKDIR /tmp/cmake-3.13.1 
Run ./configure && make && make install
WORKDIR /tmp
RUN rm -rf cmake-3.13.1 

#Install Opencv-4.0.0 for Watchmen
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
     
WORKDIR /workspace

