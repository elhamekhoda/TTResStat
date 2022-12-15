 #!/usr/bin/env python
from pathlib import Path
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs_dir', default='/eos/atlas/atlascerngroupdisk/phys-exotics/hqt/ttRes_semilep/TNA_outputs/histOutput_21.2.180_syst/fullrun2_aug2022/combined/limit_inputs')

    args = parser.parse_args()
    root_dir = Path(args.inputs_dir)
    for channel in ['be', 'bmu', 're', 'rmu']:
        channel_dir = root_dir / channel
        grav_paths = [f for f in channel_dir.glob('hist_grav*.root')]
        backgrounds = ['tt', 'wjets', 'singletop', 'zjets', 'vv']
        background_paths = [str(channel_dir / f'hist_{b}.root') for b in backgrounds]
        for p in grav_paths:
            grav_name = p.stem
            subprocess.call(['hadd', str(channel_dir / f'{grav_name}_pseudodata.root'), str(p)] + background_paths)


if __name__ == '__main__':
    main()