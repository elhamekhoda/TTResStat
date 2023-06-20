import argparse
from pathlib import Path
from prettytable import PrettyTable

def get_limits(run_dir):
    # example name: limit_zprime500_limitBLIND.txt
    limit_txt_dir = run_dir / 'plots'
    limit_files = [l for l in limit_txt_dir.glob('*.txt')]
    limits = {}

    for limit_file in limit_files:
        mass = int(limit_file.stem.split('_')[1].replace('zprime', ''))
        with open(limit_file) as f:
            # example line: xsec      52.16285327513
            for line in f:
                if 'muexp' in line:
                    muexp = float(line.split()[1])
                if 'xsec' in line:
                    xsec = float(line.split()[1])
                    break
        limits[mass] = muexp * xsec
    
    return limits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", help="the input run directories", nargs="+")

    args = parser.parse_args()

    limits = {}
    for dir in args.dirs:
        # example dir name: /home/schuya/ttres1lepstat/run/statResults_ttres1L2L_2023-05-23_1l_zprime_rmu2
        dir = Path(dir)
        region = dir.stem.split('_')[-1]
        limits[region] = get_limits(dir)

    regions = list(limits.keys())
    regions.sort()
    masses = list(limits[regions[0]].keys())
    masses.sort()
    # display a table of limits, with columns for each region and rows for each mass
    table = PrettyTable()
    table.field_names = ['mass'] + regions
    for mass in masses:
        row = [mass]
        for region in regions:
            if mass in limits[region]:
                # get limit in scientific notation with 2 decimal places
                row.append('{:.2e}'.format(limits[region][mass]))
            else:
                row.append('nan')
        table.add_row(row)
    print(table)
    breakpoint()
    



if __name__ == "__main__":
    main()