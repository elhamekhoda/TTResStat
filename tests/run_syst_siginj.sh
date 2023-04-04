# zprime
for SIGNAL in zprime grav gluon
do
    for INJ_SIGNAL in zprime grav gluon
    do
        for INJ_MASS in 1000 3000
        do
            python scripts/run_trexfitter.py --ops hwfl -s $SIGNAL\_inj$INJ_SIGNAL\_$INJ_MASS\_unblind_allsys -c 1l --signal zprime --batch_system af_short -sigm $INJ_MASS -sign $INJ_SIGNAL --unblind 
        done
    done
done
# # grav
# for MASS in 400 500 750 1000 2000 3000
# do
#     python scripts/run_combined_trexfitter.py --ops hwfl -s grav_inj_$MASS\_statonly -c 1l configs/configs_2023-01-10_grav_inj_$MASS\_unblind/statonly --batch_system af_short
# done