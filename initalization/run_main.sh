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
	   chown 3188:3166 /data /logs;
	   sleep 1m;
	fi;
done;
