#!/bin/bash
shopt -s expand_aliases

SCRIPT_DIR=$1
source $SCRIPT_DIR/../setup.sh
source $SCRIPT_DIR/../TRExFitter/setup.sh

CMD=$2
echo Running: \"python $SCRIPT_DIR/run_trexfitter.py $CMD\"
python $SCRIPT_DIR/run_trexfitter.py $CMD