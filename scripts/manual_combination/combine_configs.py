
import os
from utils import remove_quotes, write_config, parse_config_file

import argparse


def combine_fit(fit_1l, fit_2l):
    fit_combined = {}
    keys = set(fit_1l.keys()) | set(fit_2l.keys())
    diff_keys = []
    for key in keys:
        if key not in fit_1l:
            fit_combined[key] = fit_2l[key]
        elif key not in fit_2l:
            fit_combined[key] = fit_1l[key]
        elif fit_1l[key] == fit_2l[key]:
            fit_combined[key] = fit_1l[key]
        else:
            diff_keys.append(key)
    if 'SetRandomInitialNPval' in diff_keys:
        fit_combined['SetRandomInitialNPval'] = str(min(float(fit_1l['SetRandomInitialNPval']), float(fit_2l['SetRandomInitialNPval'])))
        diff_keys.remove('SetRandomInitialNPval')
    if diff_keys:
        print('The following fit settings are different:')
        for key in diff_keys:
            print(f'{key}')
            print(f'  1l: {fit_1l[key]}')
            print(f'  2l: {fit_2l[key]}')
        raise RuntimeError('Fit settings are different.')
    return fit_combined


def combine_sample(sample_1l, sample_2l, regions_1l, regions_2l):
    sample_combined = []
    dict_1l = {k: v for k,v in sample_1l}
    dict_2l = {k: v for k,v in sample_2l}
    keys = set(dict_1l.keys()) | set(dict_2l.keys())
    for k in keys:
        if k not in dict_1l:
            dict_2l[k]['Regions'] = ','.join(regions_2l)
            sample_combined.append((k, dict_2l[k]))
        elif k not in dict_2l:
            dict_1l[k]['Regions'] = ','.join(regions_1l)
            sample_combined.append((k, dict_1l[k]))
        elif 'data' in k.lower():
            sample_combined.append((k, dict_1l[k]))
        else:
            raise RuntimeError('Sample is present in both 1l and 2l configs.')
    
    # sort sample_combined based on type, then name
    sample_combined.sort(key=lambda x: (x[1]['Type'], x[0]))
    # ensure that any sample with type 'Ghost' is at the front, while otherwise preserving the order
    sample_combined.sort(key=lambda x: x[1]['Type'] == 'GHOST', reverse=True)


    return sample_combined

def combine_systematic(systematic_1l, systematic_2l):
    breakpoint()

def combine_region(region_1l, region_2l):
    region_1l = {k: v for k,v in region_1l}
    region_2l = {k: v for k,v in region_2l}
    region_combined = []
    keys = set(region_1l.keys()) | set(region_2l.keys())
    for key in keys:
        if key not in region_1l:
            region_combined.append((key, region_2l[key]))
        elif key not in region_2l:
            region_combined.append((key, region_1l[key]))
        elif region_1l[key] == region_2l[key]:
            region_combined.append((key, region_1l[key]))
        else:
            raise RuntimeError('Region settings are different.')
        
    # sort region_combined based on type, then name
    region_combined.sort(key=lambda x: (x[1]['Type'], x[0]))

    
    return region_combined

def combine_limit(limit_1l, limit_2l):
    limit_combined = {}
    keys = set(limit_1l.keys()) | set(limit_2l.keys())
    diff_keys = []
    for key in keys:
        if key not in limit_1l:
            limit_combined[key] = limit_2l[key]
        elif key not in limit_2l:
            limit_combined[key] = limit_1l[key]
        elif limit_1l[key] == limit_2l[key]:
            limit_combined[key] = limit_1l[key]
        else:
            diff_keys.append(key)
    if 'LimitBlind' in diff_keys:
        limit_combined['LimitBlind'] = 'BLIND'
        diff_keys.remove('LimitBlind')
    if diff_keys:
        print('The following limit settings are different:')
        for key in diff_keys:
            print(f'{key}')
            print(f'  1l: {limit_1l[key]}')
            print(f'  2l: {limit_2l[key]}')
        raise RuntimeError('Limit settings are different.')
    return limit_combined

def combine_options(options_1l, options_2l):
    breakpoint()

def combine_normfactor(normfactor_1l, normfactor_2l):
    dict_1l = {k: v for k,v in normfactor_1l}
    dict_2l = {k: v for k,v in normfactor_2l}
    keys = set(dict_1l.keys()) | set(dict_2l.keys())
    normfactor_combined = []
    for k in keys:
        if k not in dict_1l:
            normfactor_combined.append((k, dict_2l[k]))
        elif k not in dict_2l:
            normfactor_combined.append((k, dict_1l[k]))
        else:
            normfactor_dict = {}
            normfactor_keys = set(dict_1l[k].keys()) | set(dict_2l[k].keys())
            diff_keys = []
            for normfactor_key in normfactor_keys:
                if normfactor_key not in dict_1l[k]:
                    normfactor_dict[normfactor_key] = dict_2l[k][normfactor_key]
                elif normfactor_key not in dict_2l[k]:
                    normfactor_dict[normfactor_key] = dict_1l[k][normfactor_key]
                elif dict_1l[k][normfactor_key] == dict_2l[k][normfactor_key]:
                    normfactor_dict[normfactor_key] = dict_1l[k][normfactor_key]
                elif normfactor_key == 'Title':
                    normfactor_dict[normfactor_key] = dict_1l[k][normfactor_key]
                elif normfactor_key == 'Nominal':
                    normfactor_dict[normfactor_key] = str(min(float(dict_1l[k][normfactor_key]), float(dict_2l[k][normfactor_key])))
                elif normfactor_key == 'Min':
                    normfactor_dict[normfactor_key] = str(min(float(dict_1l[k][normfactor_key]), float(dict_2l[k][normfactor_key])))
                elif normfactor_key == 'Max':
                    normfactor_dict[normfactor_key] = str(max(float(dict_1l[k][normfactor_key]), float(dict_2l[k][normfactor_key])))
                else:
                    diff_keys.append(normfactor_key)
            if diff_keys:
                print(f'The following normfactor settings are different for {k}:')
                for normfactor_key in diff_keys:
                    print(f'   {normfactor_key}')
                    print(f'     1l: {dict_1l[k][normfactor_key]}')
                    print(f'     2l: {dict_2l[k][normfactor_key]}')
                raise RuntimeError('Normfactor settings are different.')
            normfactor_combined.append((k, normfactor_dict))
    return normfactor_combined

def combine_job(job_1l, job_2l):
    job_combined = {}
    keys = set(job_1l.keys()) | set(job_2l.keys())
    diff_keys = []
    for key in keys:
        if key not in job_1l:
            job_combined[key] = job_2l[key]
        elif key not in job_2l:
            job_combined[key] = job_1l[key]
        elif job_1l[key] == job_2l[key]:
            job_combined[key] = job_1l[key]
        else:
            diff_keys.append(key)
    if 'SystControlPlots' in diff_keys:
        job_combined['SystControlPlots'] = 'TRUE'
        diff_keys.remove('SystControlPlots')
    if 'RankingPlot' in diff_keys:
        job_combined['RankingPlot'] = '"all"'
        diff_keys.remove('RankingPlot')
    if 'SystPruningNorm' in diff_keys:
        job_combined['SystPruningNorm'] = str(max(float(job_1l['SystPruningNorm']), float(job_2l['SystPruningNorm'])))
        diff_keys.remove('SystPruningNorm')
    if 'Label' in diff_keys:
        job_combined['Label'] = '"t#bar{t} 1-lepton/2-lepton search'
        diff_keys.remove('Label')
    if 'SmoothingOption' in diff_keys:
        job_combined['SmoothingOption'] = 'COMMONTOOLSMOOTHPARABOLIC'
        diff_keys.remove('SmoothingOption')
    if 'SystPruningShape' in diff_keys:
        job_combined['SystPruningShape'] = str(max(float(job_1l['SystPruningShape']), float(job_2l['SystPruningShape'])))
        diff_keys.remove('SystPruningShape')
    if 'LegendNColumns' in diff_keys:
        job_combined['LegendNColumns'] = str(max(int(job_1l['LegendNColumns']), int(job_2l['LegendNColumns'])))
        diff_keys.remove('LegendNColumns')
    if 'AtlasLabel' in diff_keys:
        job_combined['AtlasLabel'] = '"Internal"'
        diff_keys.remove('AtlasLabel')
    if 'LumiLabel' in diff_keys:
        job_combined['LumiLabel'] = '"139 fb#kern[-0.5]{^{-1}}"'
        diff_keys.remove('LumiLabel')
    if 'ImageFormat' in diff_keys:
        job_combined['ImageFormat'] = '"pdf","png"'
        diff_keys.remove('ImageFormat')
    if 'RatioYmin' in diff_keys:
        job_combined['RatioYmin'] = str(min(float(job_1l['RatioYmin']), float(job_2l['RatioYmin'])))
        diff_keys.remove('RatioYmin')
    if 'PlotOptions' in diff_keys:
        job_combined['PlotOptions'] = '"NOSIG,NORMSIG,POISSONIZE,NOXERR,OPRATIO"'
        diff_keys.remove('PlotOptions')
    if diff_keys:
        print('The following job settings are different in the two configs:')
        for key in diff_keys:
            print(f'{key}')
            print(f'  1l: {job_1l[key]}')
            print(f'  2l: {job_2l[key]}')
        raise RuntimeError('Job settings are different.')
    if 'InputName' in job_combined:
        del job_combined['InputName']
    return job_combined

def combine_significance(significance_1l, significance_2l):
    raise NotImplementedError

def combine_objects(obj_pairs_1l, obj_pairs_2l, obj_type, regions_1l, regions_2l):
    assert len(obj_pairs_1l) > 0 or len(obj_pairs_2l) > 0, f'No objects of type {obj_type} found in either config'
    if len(obj_pairs_1l) == 0:
        return obj_pairs_2l
    if len(obj_pairs_2l) == 0:
        return obj_pairs_1l
    if obj_type == 'Fit':
        return [('fit', combine_fit(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'Sample':
        return combine_sample(obj_pairs_1l, obj_pairs_2l, regions_1l, regions_2l)
    elif obj_type == 'Systematic':
        return combine_systematic(obj_pairs_1l, obj_pairs_2l)
    elif obj_type == 'Region':
        return combine_region(obj_pairs_1l, obj_pairs_2l)
    elif obj_type == 'Limit':
        return [('limit', combine_limit(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'Options':
        return [('options', combine_options(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'NormFactor':
        return combine_normfactor(obj_pairs_1l, obj_pairs_2l)
    elif obj_type == 'Job':
        return [('ttres1l2l', combine_job(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'Significance':
        return [('significance', combine_significance(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    else:
        raise RuntimeError(f'Unknown object type {obj_type}')


def combine_configs(config_1l, config_2l, out_dir, statonly=False):
    """Combine the 1l and 2l configs into a single config."""
    config_1l = parse_config_file(config_1l, statonly=statonly)
    config_2l = parse_config_file(config_2l, statonly=statonly)
    # go through each object type and combine the objects
    obj_types = set(config_1l.keys()) | set(config_2l.keys())
    type_order = ['Job', 'Options', 'Fit', 'Limit', 'Significance', 'Region', 'Sample', 'NormFactor', 'Systematic']
    config_combined = {}
    regions_1l = set(remove_quotes(t[0]) for t in config_1l['Region'])
    regions_2l = set(remove_quotes(t[0]) for t in config_2l['Region'])
    for obj_type in type_order:
        if obj_type not in obj_types:
            continue
        combined_objects = combine_objects(config_1l[obj_type], config_2l[obj_type], obj_type=obj_type, regions_1l=regions_1l, regions_2l=regions_2l)
        config_combined[obj_type] = combined_objects

    # write the combined config
    out_path = os.path.join(out_dir, 'ttres1l2l.tmp')
    write_config(config_combined, out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_1l", type=str, help="Path to the 1l config file")
    parser.add_argument("config_2l", type=str, help="Path to the 2l config file")
    parser.add_argument("out_dir", type=str, help="Path to the output directory")
    parser.add_argument("--statonly", action="store_true", help="Ignore systematics")

    args = parser.parse_args()
    combine_configs(args.config_1l, args.config_2l, args.out_dir, args.statonly)

if __name__ == "__main__":
    main()