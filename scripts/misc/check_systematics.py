from pathlib import Path
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from collections import namedtuple

# define named tuple with three fields: fit value, +1 sigma, -1 sigma
systematic_fit = namedtuple('systematic_fit', ['fit', 'plus', 'minus'])

def parse_fit_file(fit_path):
    with open(fit_path, 'r') as f:
        lines = f.readlines()
        systematic_scores = {}
        for line in lines:
            if 'NUISANCE_PARAMETERS' in line:
                continue
            if 'gamma' in line or 'CORRELATION_MATRIX' in line:
                break
            try:
                name, fit, plus, minus = line.split()
            except ValueError:
                breakpoint()
            systematic_scores[name] = systematic_fit(float(fit), float(plus), float(minus))
    return systematic_scores

def main():
    parser = argparse.ArgumentParser(description='Check for over/underconstrained systematics in a fit.')
    parser.add_argument('fit_path')
    parser.add_argument('--compare_1l', help='Path to another fit file to compare to.')
    parser.add_argument('--compare_2l', help='Path to another fit file to compare to.')
    args = parser.parse_args()

    fit_path = Path(args.fit_path)
    if not fit_path.exists():
        raise FileNotFoundError(f'Fit file {fit_path} does not exist.')
    
    systematic_scores = parse_fit_file(fit_path)
    if args.compare_1l or args.compare_2l:
        compare_1l_path = Path(args.compare_1l)
        if not compare_1l_path.exists():
            raise FileNotFoundError(f'Fit file {compare_1l_path} does not exist.')
        compare_1l_systematic_scores = parse_fit_file(compare_1l_path)

        compare_2l_path = Path(args.compare_2l)
        if not compare_2l_path.exists():
            raise FileNotFoundError(f'Fit file {compare_2l_path} does not exist.')
        compare_2l_systematic_scores = parse_fit_file(compare_2l_path)

    def get_constrained_systs(systematic_scores):
        overconstrained_systematics = {}
        for name, systematic in systematic_scores.items():
            if systematic.plus < 0.8 or systematic.minus > -0.8:
                overconstrained_systematics[name] = systematic
    
        underconstrained_systematics = {}
        for name, systematic in systematic_scores.items():
            if systematic.plus > 1.2 or systematic.minus < -1.2:
                underconstrained_systematics[name] = systematic
        
        return overconstrained_systematics, underconstrained_systematics

    overconstrained_systematics, underconstrained_systematics = get_constrained_systs(systematic_scores)
    if args.compare_1l or args.compare_2l:
        compare_1l_overconstrained_systematics, compare_1l_underconstrained_systematics = get_constrained_systs(compare_1l_systematic_scores)
        compare_2l_overconstrained_systematics, compare_2l_underconstrained_systematics = get_constrained_systs(compare_2l_systematic_scores)

        # check for new overconstrained systematics
        new_overconstrained_systematics_names = set(overconstrained_systematics.keys()) - set(compare_1l_overconstrained_systematics.keys()) - set(compare_2l_overconstrained_systematics.keys())
        new_overconstrained_systematics = {name: systematic_scores[name] for name in sorted(new_overconstrained_systematics_names)}

        print('New overconstrained systematics:')
        for name, systematic in new_overconstrained_systematics.items():
            print(f'{name}: {systematic.fit} +{systematic.plus} {systematic.minus}')
        
        # check for new underconstrained systematics
        new_underconstrained_systematics_names = set(underconstrained_systematics.keys()) - set(compare_1l_underconstrained_systematics.keys()) - set(compare_2l_underconstrained_systematics.keys())
        new_underconstrained_systematics = {name: systematic_scores[name] for name in sorted(new_underconstrained_systematics_names)}
        print('New underconstrained systematics:')
        for name, systematic in new_underconstrained_systematics.items():
            print(f'{name}: {systematic.fit} +{systematic.plus} {systematic.minus}')
    else:
        print('Overconstrained systematics:')
        for name, systematic in overconstrained_systematics.items():
            print(f'{name}: {systematic.fit} +{systematic.plus} {systematic.minus}')
        print('Underconstrained systematics:')
        for name, systematic in underconstrained_systematics.items():
            print(f'{name}: {systematic.fit} +{systematic.plus} {systematic.minus}')


if __name__ == "__main__":
    main()