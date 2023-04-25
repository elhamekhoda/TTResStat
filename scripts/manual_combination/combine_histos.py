import argparse
from pathlib import Path
import shutil
from ROOT import *

import os
import sys
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import systematics

def get_variation(name, systematic):
    parts = name.split('_')
    i = -1
    bin_suffix = parts[i]
    if bin_suffix not in ['orig', 'regBin']:
        bin_suffix = ''
    else:
        i -= 1
    if systematic == 'nominal':
        return bin_suffix
    variation = parts[i]
    systematic_parts = systematic.split('_')
    if len(systematic_parts) >= 1:
        is_shape_systematic = systematic_parts[-1] == 'Shape'
    else:
        is_shape_systematic = False
    if variation in ['Up', 'Down']:
        if (parts[i-1] == 'Shape' and not is_shape_systematic) or (is_shape_systematic and parts[i-1] == 'Shape' and parts[i-2] == 'Shape'):
            variation = parts[i-1] + '_' + variation
    if bin_suffix != '':
        variation += '_' + bin_suffix
    return variation

def make_sample_map():
    sample_map = {}
    sample_map.update({f'Grav_{m}': f'Grav{m}' for m in [400, 500, 750, 1000, 2000, 3000]})
    sample_map.update({f'KKg_{m}': f'KKgMG{m}' for m in [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]})
    # sample_map.update({f'ZprimeTC2_{m}': f'ZprimeTC2_{m}' for m in [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]})
    return sample_map

def write_renamed_histos(input_tdir, output_tdir, systematic_map, sample_map, path='', debug=False, level=1):
    for key in (pbar:=tqdm(input_tdir.GetListOfKeys(), desc="Samples", disable=level != 2, position=1, leave=True, ncols=80)):
        obj = key.ReadObj()
        pbar.set_postfix_str(obj.GetName())
        if obj.InheritsFrom("TDirectory"):
            old_name = obj.GetName()
            if old_name in systematic_map:
                new_name = systematic_map[old_name]
                if debug:
                    print('\t\t Renaming directory {} to {}'.format(old_name, new_name))
            elif old_name in sample_map:
                new_name = sample_map[old_name]
                if debug:
                    print('\t\t Renaming directory {} to {}'.format(old_name, new_name))
            else:
                new_name = old_name

            new_path = path + '/' + new_name if path else new_name
            new_dir = output_tdir.mkdir(new_name)
            if debug:
                print(f"\t Recursing into {new_path}...")
            write_renamed_histos(obj, new_dir, systematic_map, sample_map, new_path, debug, level=level+1)

        elif obj.InheritsFrom("TH1"):
            name = obj.GetName()
            # If this is a histogram, convert it to the ttres1L format
            path_parts = path.split("/")
            region = path_parts[0]
            sample = path_parts[1]
            systematic = path_parts[2]
            variation = get_variation(name, systematic)
            if systematic == 'nominal':
                if variation != '':
                    new_name = f'{region}_{sample}_{variation}'
                else:
                    new_name = f'{region}_{sample}'
            else:
                new_name = f'{region}_{sample}_{systematic}_{variation}'
            # Write the histogram to the output file
            output_tdir.cd()
            obj.Write(new_name, TObject.kOverwrite)
        else:
            if debug:
                print(f"Found object of type {obj.ClassName()}")
                print(f"Name: {obj.GetName()}")
                print(f"Title: {obj.GetTitle()}")
                print(f"Path: {path}")


def move_histos(dir, output_dir, rename=False, debug=False):
    systematics_map = systematics.dilepNamesMap
    sample_map = make_sample_map()
    files = list(dir.iterdir())
    for file in (pbar:=tqdm(files, desc="Regions", unit="file", position=0, leave=True, ncols=80)):
        if file.is_file():
            if file.suffix != '.root':
                continue
            if 'preFit' in file.name:
                continue
            name = file.name
            split = name.split('_')
            if len(split) < 2:
                continue
            region = split[-2]
            if len(split) >= 3:
                if split[-3] == 'mllbb':
                    region = f'mllbb_{region}'
            pbar.set_postfix_str(region)
            out_name = f'ttRes1L2L_{region}_histos.root'
            if debug:
                print(f"Copying {file} to {output_dir / out_name}...")
            if rename:
                input_tfile = TFile(str(file), 'READ')
                output_tfile = TFile(str(output_dir / out_name), 'RECREATE')
                if debug:
                    print(f"Renaming histograms in {output_dir / out_name}...")
                # rename_histos(tfile, systematics.dilepNamesMap, debug=debug)
                write_renamed_histos(input_tfile, output_tfile, systematics_map, sample_map, debug=debug)
                input_tfile.Close()
                output_tfile.Close()
            else:
                shutil.copy(file, output_dir / out_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to move and rename histograms.")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('dir_1l', type=str, help='Directory with 1l histograms')
    parser.add_argument('dir_2l', type=str, help='Directory with 2l histograms')

    parser.add_argument('output', type=str, help='Output directory')
    parser.add_argument('--debug', action='store_true', help='Print debug messages')

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    dir_1l = Path(args.dir_1l)
    dir_2l = Path(args.dir_2l)

    # move_histos(dir_2l, output_dir, rename=False, debug=args.debug)
    move_histos(dir_1l, output_dir, rename=True, debug=args.debug)
    

if __name__ == '__main__':
    main()