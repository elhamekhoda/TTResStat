# zprime
for MASS in 500 750 1000 1500 2000 2500 3000 
do
    python scripts/run_combined_trexfitter.py --ops hwfl -s zprime_inj_$MASS\_statonly_unblind_auto_inj -c 1l configs/configs_2023-01-12_zprime_inj_$MASS\_unblind_auto_inj/statonly --batch_system af_short -m 500 750 1000 1500 2000 2500 3000
    python scripts/run_combined_trexfitter.py --ops hwfl -s zprime_inj_$MASS\_statonly_unblind_manual_inj -c 1l configs/configs_2023-01-12_zprime_inj_$MASS\_unblind_manual_inj/statonly --batch_system af_short -m 500 750 1000 1500 2000 2500 3000
done

# # grav
# for MASS in 400 500 750 1000 2000 3000
# do
#     python scripts/run_combined_trexfitter.py --ops hwfl -s grav_inj_$MASS\_statonly -c 1l configs/configs_2023-01-10_grav_inj_$MASS\_unblind/statonly --batch_system af_short
# done