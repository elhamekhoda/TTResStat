import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_utils import parse_config_file, write_config

def update_config(config, merge):
    breakpoint()
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--merge', choices=['leptons', 'btag', 'both'], required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)

    args = parser.parse_args()

    config = parse_config_file(args.input)
    
    new_config = update_config(config, args.merge)



if __name__ == '__main__':
    main()