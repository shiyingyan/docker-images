#!/bin/bash

if [ -e /var/run/docker.sock ]; then
  chmod 0777 /var/run/docker.sock
fi

chown -R 3188:3166 /data /logs;

#num=0
#until [ $num -gt 60000 ];
#do
#   chown -R 3188:3166 /data /logs;
#   num=$((num+1));
#   echo $num;
#done;

exec python3 /usr/local/main.py

