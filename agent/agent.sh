#!/bin/sh
set -e

HOST=localhost:8080/commands
TIMEOUT=3

while true; do
    EXECUTE_COMMANDS=$(curl -s -H "Accept: application/json" -H "Content-Type: application/json" $HOST)
    eval $EXECUTE_COMMANDS
    sleep $TIMEOUT
done
