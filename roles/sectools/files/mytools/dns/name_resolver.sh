#!/bin/bash

echo "DNS: "$1
echo "Reading: "$2
while read $ip 
do
    h=$(dig @$1 +short $ip);
    echo "$h | $ip "
done < $2