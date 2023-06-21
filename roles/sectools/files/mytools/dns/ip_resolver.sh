#!/bin/bash

echo "DNS: "$1
echo "Reading: "$2
filename=$2
while read host; do
    h=$(dig @$1 +short $host);
    echo "$h | $host "
done < $filename