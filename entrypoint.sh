#!/bin/bash
set -x

sleep 2
ls ./inputdir
pip3 list
python3 src/thermal_scripts.py -i ./inputdir/B_A0_3.csv -o ./results

