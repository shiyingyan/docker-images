# FROM alpine:3.14
FROM python:3.8.12-slim-buster

# RUN apt-get update && \
#     apt-get install -y procps && \
#     apt-get install -y vim && \
#     apt-get install -y incron
RUN sed -i 's/archive.ubuntu.com/mirrors.163.com/g' /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y procps && \
    apt-get install -y inetutils-ping && \
    apt-get install -y vim && \
    apt-get install -y telnet && \
    apt-get install -y psmisc

WORKDIR /usr/local

COPY run_main.sh main.py requirements.txt /usr/local/
RUN pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple

ENTRYPOINT /usr/local/run_main.sh

# COPY sany-incron.service /etc/systemd/system/multi-user.target.wants
# COPY run_main.sh cron.sh /usr/local/
# RUN chmod 755 /usr/local/run_main.sh && \
#     chmod 755 /usr/local/cron.sh
# ENTRYPOINT /etc/init.d/dbus start && sleep 5 && ps -aux && /usr/bin/sh /usr/local/run_main.sh
# ENTRYPOINT /etc/init.d/dbus start && sleep 5 && ps -aux && systemctl start sany-incron.service
# ENTRYPOINT /usr/local/run_main.sh
#CMD sh -c "chown 3188:3166 /logs /data; while true; do chown 3188:3166 /logs/* /data/*; sleep 5; done;"
