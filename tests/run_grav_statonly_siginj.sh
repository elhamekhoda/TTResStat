# grav
for MASS in 400 500 750 1000 2000 3000
do
    python scripts/run_combined_trexfitter.py --ops hwfl -s grav_inj_$MASS\_statonly -c 1l configs/configs_2023-01-10_grav_inj_$MASS\_unblind/statonly --batch_system af_short
done