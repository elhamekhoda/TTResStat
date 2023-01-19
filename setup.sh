#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh

asetup StatAnalysis,0.1.2

export DATA_DIR_1L=/data/schuya/ttbar_resonance/1l/fullrun2_aug2022/combined/limit_inputs/
export DATA_DIR_2L=/data/schuya/ttbar_resonance/2l/fullrun2-jan-2023/