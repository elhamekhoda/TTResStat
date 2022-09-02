#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh

lsetup "root 6.14.04-x86_64-slc6-gcc62-opt" 
lsetup git
mkdir plots run

git clone ssh://git@gitlab.cern.ch:7999/TRExStats/TRExFitter.git

