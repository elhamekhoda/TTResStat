from pathlib import Path 
import subprocess

# Move limit file from each sub directory.
def move_limits(dir):
    for zprime_dir in dir.iterdir():
        if zprime_dir.is_dir() and zprime_dir.name.startswith('zprime'):
            mass = zprime_dir.name.split('_')[1]
            limit_file = zprime_dir / 'ttRes1L' / 'Limits' / 'asymptotics' / 'zprimeMASS_CL95.root'
            if limit_file.exists():
                subprocess.call(['cp', str(limit_file), str(dir / 'limits' / f'zprime{mass}_CL95.root')])
            else:
                print(f'limit file not found: {str(limit_file)}')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=Path)
    args = parser.parse_args()
    move_limits(args.dir)