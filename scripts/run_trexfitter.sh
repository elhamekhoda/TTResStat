#!/bin/bash

source /home/schuya/ttres1lepstat/TRExFitter/setup.sh

CONFIG_DIR=$1
OPS=$2
SUFFIX=$3
MASS=$4
CHANNEL=$5
SIGNAL=$6
EXCLUDE_SYSTEMATICS=$7
python /home/schuya/ttres1lepstat/scripts/run_combined_trexfitter.py $CONFIG_DIR --ops $OPS -s $SUFFIX -c $CHANNEL --signal $SIGNAL $EXCLUDE_SYSTEMATICS -m $MASS 