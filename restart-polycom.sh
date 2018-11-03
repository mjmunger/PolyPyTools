#!/bin/bash
LIST=`asterisk -rx "sip show peers" | awk '{ print $2 }'`
for PEER in $LIST
do
	if [ ! "$PEER" == "(Unspecified)" ] &&  ! [ "$PEER" == "Host" ] &&  ! [ "$PEER" == "sip" ]; then
		asterisk -rx "sip notify polycom-check-cfg $PEER"
	fi
done
