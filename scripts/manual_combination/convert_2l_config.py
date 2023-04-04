import argparse
from collections import defaultdict
from pathlib import Path
import re

import yaml

from utils import parse_config_file, remove_quotes, write_config

bad_samples = ['zjets_LF_up', 'zjets_HF_up']

def rename_samples(config, suffix):
    """Rename samples in the config file."""

    def rename_sample(obj_name):
        obj_name = obj_name.strip()
        if obj_name.startswith('"') and obj_name.endswith('"'):
            return '"' + obj_name[1:-1] + suffix + '"'
        else:
            return obj_name + suffix
        
    def rename_samples_in_property(obj_dict, property):
        if property in obj_dict:
            sample_sections = obj_dict[property].split(';')
            new_sample_sections = []
            for sample_section in sample_sections:
                samples = sample_section.split(',')
                new_samples = []
                for sample in samples:
                    sample = sample.strip()
                    if '*' in sample:
                        print('Ignoring wildcard sample: ' + sample)
                        new_samples.append(sample)
                        continue
                    new_samples.append(rename_sample(sample))
                new_sample_sections.append(','.join(new_samples))
            obj_dict[property] = ';'.join(new_sample_sections)

    for obj_type, obj_pairs in config.items():
        if obj_type.lower() == 'sample':
            new_obj_pairs = []
            for obj_name, obj_dict in obj_pairs:
                obj_names = obj_name.split(';')
                new_obj_names = []
                for obj_name in obj_names:
                    if remove_quotes(obj_name.strip()) in bad_samples:
                        print('Ignoring bad sample: ' + remove_quotes(obj_name.strip()))
                        continue
                    new_obj_names.append(rename_sample(obj_name.strip()))
                new_obj_name = ';'.join(new_obj_names)
                if new_obj_name:
                    new_obj_pairs.append((new_obj_name, obj_dict))
            config[obj_type] = new_obj_pairs
        else:
            # check other objects for references to the sample
            for obj_name, obj_dict in obj_pairs:
                rename_samples_in_property(obj_dict, 'Samples')
                rename_samples_in_property(obj_dict, 'SampleUp')
                rename_samples_in_property(obj_dict, 'SampleDown')
                rename_samples_in_property(obj_dict, 'ReferenceSample')
                    

def convert_ntuple_to_histogram_paths(config):

    # change job settings
    job_settings = config['Job'][0][1]
    job_settings['HistoPath'] = job_settings['NtuplePaths']
    job_settings['ReadFrom'] = 'HIST'
    # delete any setting that has 'ntuple' in it
    for key in list(job_settings.keys()):
        if 'ntuple' in key.lower():
            print('Deleting job setting: ' + key)
            del job_settings[key]
    other_ntuple_options = ['MCweight', 'Selection', 'CustomIncludePaths', 'CustomFunctions']
    for option in other_ntuple_options:
        if option in job_settings:
            print('Deleting job setting: ' + option)
            del job_settings[option]


    # change region settings
    new_config = config.copy()
    for i, (region_name, region_dict) in enumerate(config['Region']):
        region_names = region_name.split(';')
        region_dict['HistoPathSuff'] = ';'.join([name.lower().strip() for name in region_names])
        region_dict['HistoName'] = ';'.join([name.lower().strip() for name in region_names])
        # delete any setting that has 'ntuple' in it
        for key in list(region_dict.keys()):
            if 'ntuple' in key.lower():
                print('Deleting region setting: ' + key)
                del region_dict[key]
            if 'Selection' in region_dict:
                del region_dict['Selection']
            if 'Variable' in region_dict:
                del region_dict['Variable']
        new_config['Region'][i] = (region_name, region_dict)
    config = new_config
    
    # change sample settings
    new_config = config.copy()
    for i, (sample_name, sample_dict) in enumerate(config['Sample']):
        sample_names = sample_name.split(';')
        sample_dict['HistoFile'] = ';'.join([name.lower().strip() for name in sample_names])
        sample_dict['NormalizedByTheory'] = 'FALSE'
        # delete any setting that has 'ntuple' in it
        for key in list(sample_dict.keys()):
            if 'ntuple' in key.lower():
                print('Deleting sample setting: ' + key)
                del sample_dict[key]
        if 'MCweight' in sample_dict:
            del sample_dict['MCweight']
        if 'Selection' in sample_dict:
            del sample_dict['Selection']
        new_config['Sample'][i] = (sample_name, sample_dict)

    return new_config

def convert_config(config_path, statonly):
    config = parse_config_file(config_path, statonly=statonly)

    # Rename samples
    rename_samples(config, '_dilep')

    # change ntuple paths to histogram paths
    config = convert_ntuple_to_histogram_paths(config)

    new_config_path = Path(config_path).parent / 'ttRes2L_converted.tmp'
    write_config(config, new_config_path)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="Path to the config file")
    parser.add_argument("--statonly", action="store_true", help="Ignore systematics")

    args = parser.parse_args()

    convert_config(args.config, args.statonly)

if __name__ == "__main__":
    main()