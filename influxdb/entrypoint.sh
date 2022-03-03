#!/bin/bash
set -e

if [[ -z $DB_NAME ]]; then
  echo "请设置环境变量DB_NAME"
  if [[ ! -e /etc/profile ]]
  then
    touch /etc/profile
  fi
  sed -i "/DB_NAME=F0000/d" /etc/profile 2>/dev/null
  echo "DB_NAME=F0000" >> /etc/profile
  source /etc/profile
  echo "环境变量DB_NAME未设置，默认为F0000"
fi

mkdir -p /sy
mkdir -p  /docker-entrypoint-initdb.d
/bin/cp -fu /influxdb.sh /sy/
/bin/cp -fu /influxdb.conf /sy/
cat /sy/influxdb.sh | sed "s/\$db_name/$DB_NAME/g" > /docker-entrypoint-initdb.d/influxdb_new.sh
cat /sy/influxdb.conf | sed "s/\$db_name/$DB_NAME/g" > /etc/influxdb/influxdb.conf

influxd &
        
INIT_QUERY="show databases"
INFLUXDB_INIT_PORT=58086
INFLUX_USER="root"
INFLUX_PASSWORD="root"
INFLUX_CMD="influx -host 127.0.0.1 -port $INFLUXDB_INIT_PORT -username $INFLUX_USER -password $INFLUX_PASSWORD -execute "

        for i in {50..0}; do
                if $INFLUX_CMD "$INIT_QUERY" &> /dev/null; then
                        break
                fi
                echo 'influxdb init process in progress...'
                sleep 1
        done

        if [ "$i" = 0 ]; then
                echo >&2 'influxdb init process failed.'
                exit 1
        fi

        echo "influxdb启动完成"

        for f in /docker-entrypoint-initdb.d/*; do
                case "$f" in
                        *.sh)     echo "$0: running $f"; . "$f" ;;
                        *.iql)    echo "$0: running $f"; $INFLUX_CMD "$(cat ""$f"")"; echo ;;
                        *)        echo "$0: ignoring $f" ;;
                esac
                echo
        done



#if [ "${1:0:1}" = '-' ]; then
#    set -- influxd "$@"
#fi

#/init-influxdb.sh "${@:2}"
#if [ "$1" = 'influxd' ]; then
#        /init-influxdb.sh "${@:2}"
#fi


#exec "$@"
while true; do sleep 10000000; done;
