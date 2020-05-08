FROM nsqio/nsq:latest

Add repositories /etc/apk/repositories

RUN apk update && apk add --no-cache bash tzdata \
    && cp -r -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

