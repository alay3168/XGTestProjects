FROM ubuntu:14.04

ADD sources.list /etc/apt/sources.list

RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y --no-install-recommends \
    # gdal-bin used for MapManager
    gdal-bin && \
    rm -rf /var/lib/apt/lists/*

