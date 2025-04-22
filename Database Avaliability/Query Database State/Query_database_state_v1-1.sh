#!/bin/sh

###oracle home arrays function

###Global Variables
declare -A db_arr
declare -A oh_arr
script=/home/oracle/paul/test.sql

##Create Arrays Function

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
}


query_db_state()
{

echo $1 $2

export ORACLE_SID=$1
export ORACLE_HOME=$2
export PATH=$ORACLE_HOME/bin:$PATH

sqlplus / as sysdba @$3 $1 > /dev/null 2&>1

}

###Main Script
create_db_name_home_array
#Get lenth of array
n=${#db_arr[@]}
#call db query for all CDBS
for ((i = 0; i < n; ++i)); do
	query_db_state ${db_arr[$i]} ${oh_arr[$i]} $script
done
