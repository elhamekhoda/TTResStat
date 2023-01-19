#!/bin/bash

SCRIPT_DIR=$1
source $SCRIPT_DIR/../setup.sh

CONFIG_DIR=$2
OPS=$3
SUFFIX=$4
MASS=$5
CHANNEL=$6
SIGNAL=$7
python $SCRIPT_DIR/run_trexfitter.py $CONFIG_DIR --ops $OPS -s $SUFFIX -c $CHANNEL --signal $SIGNAL -m $MASS 