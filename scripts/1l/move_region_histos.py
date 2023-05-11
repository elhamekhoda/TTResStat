import sys
import os
import argparse
from pathlib import Path
import shutil
import subprocess
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    in_dirs = ['re', 'rmu']
    limit_inputs_path = Path('/home/schuya/ttres1lepstat/data/1l/fullrun2_aug2022/combined/limit_inputs')
    out_dir = limit_inputs_path / 'r'

    if not out_dir.exists():
        out_dir.mkdir()

    files = os.listdir(limit_inputs_path / in_dirs[0])
    for file in tqdm(files):
        input_paths = [limit_inputs_path / in_dir / file for in_dir in in_dirs]
        output_path = out_dir / file
        print(f'hadd {output_path} {" ".join(str(p) for p in input_paths)}')
        subprocess.run(['hadd', output_path, *input_paths])


if __name__ == '__main__':
    main()