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
        if not (d / 'ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll').exists():
            print(f'Error: {d / "ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll"} does not exist')
            continue
        if not (d / 'ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll').is_dir():
            print(f'Error: {d / "ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll"} is not a directory')
            continue
        l = d / 'ttRes2L_v12_fit_inverted_deltaEta_2dRew_slim_SysAll'
        if not (l / 'Limits' / 'asymptotics').exists():
            print(f'Error: {l / "Limits" / "asymptotics"} does not exist')
            continue
        if not (l / 'Limits' / 'asymptotics').is_dir():
            print(f'Error: {l / "Limits" / "asymptotics"} is not a directory')
            continue
        l = l / 'Limits' / 'asymptotics'

        stem = d.stem
        split = stem.split('_')
        inj_mass = split[1]
        
        try:
            limit_file = [f for f in l.glob('*.root')][0]
        except IndexError:
            print(f'Error: no limit file found in {l}')
            continue
        # move limit file to out path
        shutil.copy(limit_file, out_path / f'Zprime_{inj_mass}.root')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dirs', nargs='+', help='directories to move')
    parser.add_argument('--out', default='.', help='out directory')
    args = parser.parse_args()
    move_limits(args.dirs, Path(args.out))
    