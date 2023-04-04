import argparse
from pathlib import Path
import shutil

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('dir_1l', type=str, help='Directory with 1l histograms')
    parser.add_argument('dir_2l', type=str, help='Directory with 2l histograms')

    parser.add_argument('output', type=str, help='Output directory')

    args = parser.parse_args()

    # copy everything in dir_1l and dir_2l to output, creating output if necessary. There is no need to combine the histograms themselves.
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    dir_1l = Path(args.dir_1l)
    dir_2l = Path(args.dir_2l)
    print(f'Copying files from {dir_1l} and {dir_2l} to {output_dir}...')
    shutil.copytree(dir_1l, output_dir, dirs_exist_ok=True)
    shutil.copytree(dir_2l, output_dir, dirs_exist_ok=True)
        
    

if __name__ == '__main__':
    main()