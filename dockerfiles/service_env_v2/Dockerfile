FROM alpine:3.8

RUN apk update && apk add --no-cache bash tzdata \
    && cp -r -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo -ne "Alpine Linux 3.8 image. (`uname -rsv`)\n" >> /root/.built

CMD ["/bin/bash"]
