#!/bin/bash
user="cassandra"
pass="cassandra"
echo "DNS: "$1
echo "Reading: "$2
echo "hostname | ip | result" > result.txt
while read host 
do
    h=$(dig @$1 +short $host);
    out=$(cqlsh $host -u $user -p $pass 2> err )
    out=$(cat err | grep -q "Bad credentials")
    if [ $? -eq 1 ]; 
    then 
        result="valid login"
        echo "$host | $h | $result" >> result.txt
    fi
done < $2