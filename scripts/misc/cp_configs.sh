for MASS in 500 750 1000 1250 1500 1750 2000 2500 3000 4000 5000
do
    mkdir -p /home/schuya/ttres1lepstat/run/pull_constrained/zprime_${MASS}
    cp /home/schuya/ttres1lepstat/run/statResults_ttres1L2L_2023-01-12_combined_blind_allsys/zprime_${MASS}/run.sh /home/schuya/ttres1lepstat/run/pull_constrained/zprime_${MASS}/run.sh
    cp /home/schuya/ttres1lepstat/run/statResults_ttres1L2L_2023-01-12_combined_blind_allsys/zprime_${MASS}/ttres1L.config /home/schuya/ttres1lepstat/run/pull_constrained/zprime_${MASS}/ttres1L.config
done