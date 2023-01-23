for MASS in 1000 3000
do
    for SIGNAL in zprime grav gluon
    do
        python scripts/make_pseudo_data_1l.py -sigm $MASS -sign $SIGNAL -mu 1.0
    done
done