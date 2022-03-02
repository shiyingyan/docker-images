#!/usr/bin/env bash

databases=$(influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'show databases')

if ( [[ -z $databases ]] || [[ ! $databases =~ $db_name ]] ) then
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'CREATE DATABASE "$db_name"'
fi

if ( [[ -z $databases ]] || [[ ! $databases =~ telegraf ]] ) then
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'CREATE DATABASE "telegraf"'
fi


retention_policies=$(influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'show retention policies on $db_name')
if ( [[ -z $retention_policies ]] || [[ ! $retention_policies =~ rp_7d ]] ) then
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'CREATE RETENTION POLICY "rp_7d" ON "$db_name" DURATION 7d REPLICATION 1'
fi


if ( [[ -z $retention_policies ]] || [[ ! $retention_policies =~ rp_30d ]] ) then
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'CREATE RETENTION POLICY "rp_30d" ON "$db_name" DURATION 30d REPLICATION 1'
fi


if ( [[ -z $retention_policies ]] || [[ ! $retention_policies =~ rp_ems_60d ]] ) then
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'CREATE RETENTION POLICY "rp_ems_60d" ON "$db_name" DURATION inf REPLICATION 1'
else
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'ALTER RETENTION POLICY "rp_ems_60d" ON "$db_name" DURATION inf REPLICATION 1'
fi


retention_policies=$(influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'show retention policies on telegraf')
if ( [[ -z $retention_policies ]] || [[ ! $retention_policies =~ autogen ]] ) then
  influx -host 127.0.0.1 -port 58086 -username 'root' -password 'root'  -execute 'CREATE RETENTION POLICY "autogen" ON "telegraf" DURATION 30d REPLICATION 1'
fi
