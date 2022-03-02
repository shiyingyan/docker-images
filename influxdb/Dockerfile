FROM  influxdb:1.6.1
COPY *.sh influxdb.conf /

RUN sed -i 's/archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y procps && \
    apt-get install -y vim && \
    apt-get install -y nano && \
    apt-get install -y telnet && \
    apt-get install -y psmisc
