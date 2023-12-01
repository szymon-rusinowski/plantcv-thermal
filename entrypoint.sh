#!/bin/bash
set -x

sleep 2
ls ./inputdir
pip3 list
echo ${INPUT_FILE}
python3 src/thermal_scripts.py -i ${INPUT_FILE} -c ${COORDS} -t ${TEMP} -o ./results

