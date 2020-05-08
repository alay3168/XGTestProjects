FROM ubuntu:14.04

#ADD apache-tomcat-9.0.7 /workspace/apache-tomcat-9.0.7 

RUN echo "Asia/Shanghai" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

ADD jdk1.8.0_172 /usr/java/jdk1.8.0_172

RUN echo 'export JAVA_HOME=/usr/java/jdk1.8.0_172' >> /etc/profile && \
    echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile && \
    echo 'source /etc/profile' >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc"

ENV LANG C.UTF-8

WORKDIR /workspace/apache-tomcat-9.0.7/bin
CMD ["catalina.sh", "run"]
