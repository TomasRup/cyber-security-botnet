#!/bin/sh


HOST='0.0.0.0'
PORT='8080'

COMMAND="curl --silent http://$HOST:$PORT" # add -v for verbose; "--stderr -" to redirect err to out
echo $COMMAND

while true
do
RESP=`$COMMAND`
echo $RESP
# todo RESP parsing
SLEEP=
sleep "${SLEEP:-5}"
done