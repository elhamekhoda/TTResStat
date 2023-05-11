for SIGNAL in zprime grav gluon
do
    for MASS in 750 3000
    do
        python scripts/make_combined_config.py --region combined --suff zprime_inj_$MASS\_unblind_manual_inj -sigm $MASS -sign $SIGNAL --unblind
    done
done