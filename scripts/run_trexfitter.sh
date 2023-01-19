#!/bin/bash
shopt -s expand_aliases

SCRIPT_DIR=$1
source $SCRIPT_DIR/../setup.sh

CMD=$2
echo Command: \"$CMD\"
python $SCRIPT_DIR/run_trexfitter.py $CMD