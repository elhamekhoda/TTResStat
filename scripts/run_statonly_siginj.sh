for MASS in 500 750 1000 2000 3000 
do
    python scripts/run_combined_trexfitter.py --ops hwfl -s zprime_inj_$MASS\_statonly -c 1l configs/configs_2022-12-16_zprime_inj_$MASS/statonly --batch_system af_short
done