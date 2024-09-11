#!/bin/bash

date +"%T.%N - setting remote device to sleep"
i2ctransfer -f -y 1 w3@0x48 0x00 0x10 0x19
date +"%T.%N - max96752 SLEEP=1"
i2ctransfer -f -y 1 w3@0x40 0x00 0x10 0x51
date +"%T.%N - max96751 RESET_LINK=1"

echo "goodbye world"
