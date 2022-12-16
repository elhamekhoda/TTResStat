#!/bin/bash

source /home/schuya/ttres1lepstat/TRExFitter/setup.sh

CONFIG_DIR=$1
OPS=$2
SUFFIX=$3
MASS=$4
CHANNEL=$5
python /home/schuya/ttres1lepstat/scripts/run_combined_trexfitter.py $CONFIG_DIR --ops $OPS -s $SUFFIX -m $MASS -c $CHANNEL