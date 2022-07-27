#!/usr/bin/bash

cp /home/scada/software/hopeview-converter/recordosc_comtradecfg.lua /app/bin/hopeview/compress_eventrecord_faultosc/cfg/recordosc_comtradecfg.lua
MYSQL_PING=`mysqladmin -h hopeview-mysql -u intr-user -phopeview-db ping`
while [[ "$MYSQL_PING" != "mysqld is alive" ]]
do
    sleep 10
    MYSQL_PING=`mysqladmin -h hopeview-mysql -u intr-user -phopeview-db ping`
done
mysql -h hopeview-mysql -u intr-user -phopeview-db hwm_station_0001_db < /home/scada/software/hopeview-converter/create_device.sql

#rmysql="mysql -h hopeview-mysql -u root -p hopeview-db "
#count=0
#while true
#do
#  $rmysql "-e show databases;"
#  if [[ $? -eq 0 ]]; then
#    break
#  fi
#  count=$(($count+1))
#  if [ $count -ge 120 ]; then
#    echo "hopeview-mysql不可用，请检查"
#    exit 1
#  fi
#  echo "正在等待hopeview-mysql可用，请稍等"
#  sleep 1
#done
#
#$rmysql "< /home/scada/software/hopeview-converter/create_device.sql"
#if [[ $? -ne 0 ]]; then
#  echo "sql初始化失败"
#fi



SERVER_HOME=/app/bin/hopeview
source /etc/profile
sleep 5
cd ${SERVER_HOME}

echo "start appmain.sh" > startlog
./initcore.sh
./initevn.sh
./startapp.sh 

cd -

nohup ./ServerStart.sh &

tail -f /app/mycat/logs/mycat.log
