#/bin/bash

echo "Setting up combined fitting"
echo "***********Converting 2l config***********"
python scripts/manual_combination/convert_2l_config.py --statonly configs/ttres2l/ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim.tmp
echo "***********Converting 2l histograms***********"
rm -r data/2l/For_Alex_Thesis/converted && python scripts/manual_combination/convert_2l_histos.py data/2l/For_Alex_Thesis/Histograms/ data/2l/For_Alex_Thesis/converted
echo "***********Combining configs***********"
python scripts/manual_combination/combine_configs.py --statonly configs/ttres1l/tt1lep_config_wbtagSR_1b2b.tmp configs/ttres2l/ttRes2L_converted.tmp configs/ttres1l2l/
echo "***********Combining histograms***********"
rm -r data/1l2l/ && python scripts/manual_combination/combine_histos.py data/1l/fullrun2_aug2022/combined/limit_inputs/ data/2l/For_Alex_Thesis/converted/ data/1l2l/
