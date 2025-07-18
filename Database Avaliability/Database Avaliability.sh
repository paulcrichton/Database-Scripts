#!/bin/sh

ot=/etc/oratab
db=`egrep -i ":Y|:N" $ot | cut -d ":" -f1 | grep -v "#" | grep -v "*"`
pslist="`ps -ef | grep pmon`"

for i in $db ; do
echo "$pslist" | grep "ora_pmon_$i" 
if (($?)); then
echo "Oracle Instance - $i:       Down"
else
echo "Oracle Instance - $i:       Up"
fi
done


