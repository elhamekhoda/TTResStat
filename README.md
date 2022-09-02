# TTRes1lepStat



The scripts used for the statistical analysis of ttbar resonance search in 1-lepton channel are kept in this repository.
As of now the the minimal amount of scripts needed to run TRexFitter and produce a limit plot are kept. It will be updated with time.

### First time setup:
Need to create a `run` and `plots` directory. It will be created by `setup.sh` script. TRXeFitter will also be checked out by the setup script.
**No need to run this in subsequent logins**

### Step 1: Create the config files
The config files will be created by running the `makeConfig.py` script. It takes several arguments.
```python
python scripts/makeConfig.py --indir INPUTFILE --outdir TRExFitter_OUTPUT --configdir CONFIG_DIR --region REGION --suff SUFFIX
```
_run from the main directiory_

### Step 2: Run TRExFitter
Make sure TRExFitter is checked out from git. `runTRExFitter.py` script will be used
```python
python scripts/runTRExFitter.py --configDir CONFIG_DIR --action hwfl --suff SUFFIX
```
`--runStatOnly` will run the stat only limit    


Default: running with all systematics.    
_run from the main directiory_

### Step 3: Read TRExFitter outputs and make limit plot
Use `plotLimit.py` script
```python
python scripts/plotLimit.py --indir TREX_FILES --outdir OUT_PLOTS --suff SUFFIX
```
_run from the main directiory_
