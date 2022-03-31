num=0
while true;do
	chown -R 3188:3166 /data /logs;
	if [ $num -lt 6000 ]; then
	   num=$((num+1));
	   echo $num;
	   sleep 0.01;
        else
	   sleep 5;
	fi;
   done;
