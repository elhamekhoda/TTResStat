# TTResStat
The scripts used for the statistical analysis of ttbar resonance search are kept in this repository.


## Configuration
Configuration files are located at `configs/ttres{channel}`. They are standard trex-fitter config files, but with some options set to keywords that are replaced when `run_trexfitter.py` is run. For example, `OutputDir: "OUTPUTDIR/"`. 

### Step 0: Setup
The setup script is `setup.sh`:
```
source setup.sh
```

Within this file, two environment variables are set:

1. `DATA_DIR_1L`
2. `DATA_DIR_2L` 

These should point to the input histograms/ntuples for the 1l/2l channels, respectively. Alternatively, trexfitter histograms are written/read from `histograms/ttres{channel}/{config_name}/`. For example, the 2l config file `ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll` has histograms saved at `histograms/ttres2l/ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll/`. You can copy histograms to these locations directly, in which case you do not need the environment variables. 

As an example, to make the trexfitter histograms for the 1l channel from `DATA_DIR_1L`, run:
```
python scripts/run_trexfitter.py --ops h -c 1l --signal all -m 1000
```

If you wish to run a signal injection test with manually-injected data, the trexfitter histograms must be updated. The histograms including signal-injected data are expected to be at `histograms/ttres{channel}/{config_name}/{signal_name}_{mass}_mu{mu}`. These histograms can be automatically generated by calling `scripts/make_pseudo_data_1l.py`, for example:

```
python scripts/make_pseudo_data_1l.py -sigm 1000 -sign zprime -mu 1.0
```


### 
### Step 1: Run TRExFitter
```python
python scripts/run_trexfitter.py [...]
```
See descriptions in `run_trexfitter.py` for information on arguments.


### Step 2: Read TRExFitter outputs and make limit plot
Use `plotLimit.py` script
```python
python scripts/plotLimit.py --indir TREX_FILES --outdir OUT_PLOTS --suff SUFFIX
```
_run from the main directiory_
