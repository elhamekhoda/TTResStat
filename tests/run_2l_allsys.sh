for SIGNAL in zprime grav gluon
do
    python scripts/run_trexfitter.py -c combined --ops wfl --batch_system af --signal $SIGNAL --region_1l none
done