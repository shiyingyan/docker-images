#!/bin/bash

permission_cron_table=/etc/incron.d/permission_cron
if [[ ! -f $permission_cron_table ]]; then
  touch $permission_cron_table
fi

if [[ -z $(grep "/home/scada/data" $permission_cron_table) ]]; then
  echo "/home/scada/data IN_ATTRIB /bin/sh /usr/local/cron.sh" >> $permission_cron_table
fi
if [[ -z $(grep "/home/scada/logs" $$permission_cron_table) ]]; then
  echo "/home/scada/logs IN_ATTRIB /bin/sh /usr/local/cron.sh" >> $permission_cron_table
fi

systemctl start incrond 2>/dev/null
systemctl enable incrond 2>/dev/null

num=0
while true;do
	if [ -e /var/run/docker.sock ]; then
	  chmod 0777 /var/run/docker.sock
	fi

	if [ $num -lt 60000 ]; then
	   chown -R 3188:3166 /data /logs;
	   num=$((num+1));
	   echo $num;
  else
	   sleep 1m;
	fi;
done;


