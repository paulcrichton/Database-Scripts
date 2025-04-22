#!/bin/bash

oh=/opt/app/oracle/product/19.3/dbhome_1
nh="$oh/network/admin"
ls_file="$nh/listener.ora"
ls_names=`grep -E '^[[:space:]]*[A-Za-z0-9_]+[[:space:]]*=' "$ls_file" | grep -v "SID_LIST_" | cut -d " " -f1`
pslist="`ps -ef | grep tnslsnr`"

for i in $ls_names ; do
echo "$pslist" | grep "$i" 
if (($?)); then
echo "Oracle Listener - $i:       Down"
else
echo "Oracle Listener - $i:       Up"
fi
done