#!/usr/bin/env python
import os
from os import path
from sigXsec_1lep import *
from ROOT import *
import argparse
from datetime import datetime
from pathlib import Path
import json

def plot_limits(run_dir):
    #Setting up ATLAS style
    dirpath = os.path.dirname(os.path.realpath(__file__))
    gROOT.SetBatch()
    gROOT.LoadMacro('{}/AtlasStyle.C'.format(dirpath))
    gROOT.LoadMacro('{}/AtlasUtils.C'.format(dirpath))
    SetAtlasStyle()

    # get args from json file
    with open(path.join(run_dir, 'settings.json')) as f:
        settings = json.load(f)
    breakpoint()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('run_dir', help='the input run directory')

    args = parser.parse_args()
    plot_limits(args.run_dir)


if __name__ == "__main__":
    main()





