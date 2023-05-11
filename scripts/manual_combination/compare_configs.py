from collections import defaultdict
import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_utils import parse_config_file, split_objects


def compare_configs(config_1l, config_2l):
    """Compare the configs using parser in utils and print the differences."""
    config_1l_dicts = defaultdict(dict)
    for object_type, object_tuples in config_1l.items():
        for object_name, object_dict in object_tuples:
            config_1l_dicts[object_type][object_name] = object_dict
    
    config_2l_dicts = defaultdict(dict)
    for object_type, object_tuples in config_2l.items():
        for object_name, object_dict in object_tuples:
            config_2l_dicts[object_type][object_name] = object_dict

    # Compare the objects
    for object_type in config_1l_dicts:
        print(f'{object_type}:')
        duplicate_objects = set(config_1l_dicts[object_type]) & set(config_2l_dicts[object_type])
        if duplicate_objects:
            print(f'  Duplicate objects:')
            for duplicate_object in duplicate_objects:
                print(f'    {duplicate_object}')
        only_1l = set(config_1l_dicts[object_type]) - set(config_2l_dicts[object_type])
        if only_1l:
            print(f'  Only in 1l:')
            for object_name in only_1l:
                print(f'    {object_name}')
        only_2l = set(config_2l_dicts[object_type]) - set(config_1l_dicts[object_type])
        if only_2l:
            print(f'  Only in 2l:')
            for object_name in only_2l:
                print(f'    {object_name}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_1l', type=str, help='Config for 1l histograms')
    parser.add_argument('config_2l', type=str, help='Config for 2l histograms')

    args = parser.parse_args()
    config_1l = parse_config_file(args.config_1l)
    config_2l = parse_config_file(args.config_2l)
    compare_configs(config_1l, config_2l)


if __name__ == '__main__':
    main()