for SIGNAL in zprime grav gluon
do
    for INJ_SIGNAL in zprime grav gluon
    do
        for INJ_MASS in 1000 3000
        do
            python scripts/run_trexfitter.py --ops wfl -c 1l --signal $SIGNAL --batch_system af_short -sigm $INJ_MASS -sign $INJ_SIGNAL --unblind 
        done
    done
done