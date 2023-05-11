import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from make_config import add_systematics_to_1l_config_string

def add_systematics_to_1l_config(config_path, output_path):
    with open(config_path, 'r') as f:
        config = f.read()
    regions = "be1,be2,be3,re1,re2,re3,bmu1,bmu2,bmu3,rmu1,rmu2,rmu3"
    new_config = add_systematics_to_1l_config_string(config, regions=regions, use_dilep_names=True)
    with open(output_path, 'w') as f:
        f.write(new_config)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Path to config file')
    parser.add_argument('output', type=str, help='Output file')

    args = parser.parse_args()

    add_systematics_to_1l_config(args.config, args.output)

if __name__ == "__main__":
    main()