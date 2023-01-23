for SIGNAL in zprime grav gluon
do
    python scripts/run_trexfitter.py -c 2l --ops wfl --batch_system af_short --signal $SIGNAL
done