#!/bin/bash

date +"%T.%N - max96751 RESET_LINK=0"
i2ctransfer -f -y 1 w3@0x40 0x00 0x10 0x11

reg=0

while [ $(($reg & 0x08)) -ne 8 ]  # check for LOCKED bit
do
    i2ctransfer -f -y 1 w3@0x48 0x00 0x10 0x11
	reg=$(i2ctransfer -f -y 1 w2@0x40 0x00 0x13 r1)
	date +"%T.%N - waiting for LOCK..."
done
date +"%T.%N - link is locked"

date +"%T.%N - max96752 SLEEP=0"

echo "hello world"
