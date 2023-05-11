for SIGNAL in zprime grav gluon
do
    python scripts/run_trexfitter.py -c combined --ops wfl --batch_system af --signal $SIGNAL --region_2l none --fit_mu_asimov 0.0
done