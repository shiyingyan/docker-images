#!/bin/bash

if [ -e /var/run/docker.sock ]; then
  chmod 0777 /var/run/docker.sock
fi

find /home/scada/data \( \! -uid 3188 -o \! -gid 3166 \) -exec chown 3188:3166 {} \;
find /home/scada/logs \( \! -uid 3188 -o \! -gid 3166 \) -exec chown 3188:3166 {} \;

exec python3 /usr/local/main.py

