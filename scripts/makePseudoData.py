from pathlib import Path
import argparse
import subprocess

def make_pseudodata(root_dir, signal_name):
    # iterate over all subdirectories in root_dir
    for channel_dir in root_dir.iterdir():
        signal_paths = [f for f in channel_dir.glob(f'hist_{signal_name}*.root')]
        backgrounds = ['tt', 'wjets', 'singletop', 'zjets', 'vv']
        background_paths = [str(channel_dir / f'hist_{b}.root') for b in backgrounds]
        for p in signal_paths:
            subprocess.call(['hadd', str(channel_dir / f'{p.stem}_pseudodata.root'), str(p)] + background_paths)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs_dir', default='/data/schuya/ttbar_resonance/1l/fullrun2_aug2022/combined/limit_inputs/')
    parser.add_argument('--signal_name', default='grav')

    args = parser.parse_args()
    root_dir = Path(args.inputs_dir)

    make_pseudodata(root_dir, args.signal_name)


if __name__ == '__main__':
    main()