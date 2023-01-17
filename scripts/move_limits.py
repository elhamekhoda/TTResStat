from pathlib import Path 
import subprocess
import shutil

def move_limits(dirs, out_path):

    for d in dirs:
        d = Path(d)
        if not d.exists():
            print(f'Error: {d} does not exist')
            continue
        if not d.is_dir():
            print(f'Error: {d} is not a directory')
            continue
        if not (d / 'limits').exists():
            print(f'Error: {d / "limits"} does not exist')
            continue

        stem = d.stem
        split = stem.split('_')
        for i, s in enumerate(split):
            if s == 'inj':
                inj_mass = int(split[i+1])
                break
        
        try:
            limit_file = [f for f in d.glob('limits/*.root')][0]
        except IndexError:
            print(f'Error: no limit file found in {d / "limits"}')
            continue
        # move limit file to out path
        shutil.copy(limit_file, out_path / f'{inj_mass}.root')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dirs', nargs='+', help='directories to move')
    parser.add_argument('--out', default='.', help='out directory')
    args = parser.parse_args()
    move_limits(args.dirs, Path(args.out))
    