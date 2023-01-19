# TTResStat
The scripts used for the statistical analysis of ttbar resonance search are kept in this repository.

### Step 0: Setup StatAnalysis
```
source setup.sh
```

### Step 1: Run TRExFitter
```python
python scripts/runTRExFitter.py --configdir CONFIG_DIR --action hwfl --suff SUFFIX
```
`--runStatOnly` will run the stat only limit    


Default: running with all systematics.    
_run from the main directiory_

### Step 2: Read TRExFitter outputs and make limit plot
Use `plotLimit.py` script
```python
python scripts/plotLimit.py --indir TREX_FILES --outdir OUT_PLOTS --suff SUFFIX
```
_run from the main directiory_
