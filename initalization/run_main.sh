#!/bin/bash

if [ -e /var/run/docker.sock ]; then
  chmod 0777 /var/run/docker.sock
fi

chown 3188:3166 /data /logs

find /logs \( \! -uid 3188 -o \! -gid 3166 \) -exec chown 3188:3166 {} \;
find /data \( \! -uid 3188 -o \! -gid 3166 \) -exec chown 3188:3166 {} \;

exec python3 /usr/local/main.py

