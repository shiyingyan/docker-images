#!/bin/bash
dir=$1
op=$2
f=$3
file=$dir$f

echo $file

permission_cron_table=/etc/incron.d/permission_cron


if [[ $op == "IN_CREATE" && -d $file && -z $(grep "$file" $permission_cron_table) ]]; then
    echo "$file IN_ATTRIB /bin/sh /usr/local/cron.sh" >> $permission_cron_table
fi

if [[ $op == "IN_ATTRIB" ]]; then
    user_id=$(stat $file | grep "Uid" | awk -F '/' '{print $2}' | awk '{print $NF}')
    group_id=$(stat $file | grep "Uid" | awk -F '/' '{print $(NF-1)}' | awk '{print $NF}')

    if [[ $user_id != '3188' || $group_id != '3166' ]]; then
        chown 3188:3166 $file
    fi

fi

