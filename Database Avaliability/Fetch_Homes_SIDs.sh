#!/bin/sh
###oracle home arrays function

###Global Variables
declare -A db_arr
declare -A oh_arr

###Create Arrays Function

create_db_name_home_array()
{
#fetch information from oratab file
ot=/etc/oratab
db=`egrep -i ":Y|:N" $ot | cut -d ":" -f1 | grep -v "#" | grep -v "*"`
oh=`egrep -i ":Y|:N" $ot | cut -d ":" -f2 | grep -v "#" | grep -v "*"`

#Clear Arrays
db_arr=()
oh_arr=()

#Populate arrays
for i in $db ; do
db_arr+=$i
done

for i in $oh ; do
oh_arr+=$i
done

#Display Output
echo ${db_arr[0]}
echo ${oh_arr[0]}
}

create_db_name_home_array
