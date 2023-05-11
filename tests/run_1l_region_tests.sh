for region in be1 be2 be3 re1 re2 re3 bmu1 bmu2 bmu3 rmu1 rmu2 rmu3; do
    python scripts/run_trexfitter.py --ops wf -c 1l --signal zprime -m 4000 --fit_mu_asimov 1.0 --opts Regions=$region -s 1l_$region --batch_system af_short
done