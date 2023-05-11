
import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from combine_histos import make_sample_map
from config_utils import add_quotes, parse_config_file, remove_quotes, write_config

bad_samples = ['zjets_LF_up', 'zjets_HF_up']
bad_systematics = ['ZjetsNorm_LF', 'ZjetsNorm_HF']

bad_signal = 'ZprimePY'

def rename_samples(config, suffix, name_map):
    """Rename samples in the config file."""

    def rename_sample(obj_name):
        obj_name = obj_name.strip()
        old_name = remove_quotes(obj_name)
        if old_name in name_map:
            new_name = name_map[old_name]
            if obj_name.startswith('"') and obj_name.endswith('"'):
                return '"' + new_name + '"'
            else:
                return new_name
        else:
            return obj_name

        
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
                    if 'data' in obj_name.lower():
                        print('including data sample without renaming...')
                        new_obj_names.append(obj_name.strip())
                    else:
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
                    

def prepend(s, prefix):
    # put prefix within the quotes, if necessary
    if s.startswith('"') and s.endswith('"'):
        return '"' + prefix + s[1:-1] + '"'
    else:
        return prefix + s


def rename_1l(config_1l):
    new_config = config_1l.copy()
    samples = config_1l['Sample']
    new_samples = []
    zprime_samples = []
    grav_samples = []
    kkg_samples = []
    for sample_name, sample_dict in samples:
        sample_name = remove_quotes(sample_name)
        if 'Zprime' in sample_name:
            mass = sample_name.split('_')[1]
            new_sample_name = f'"ZprimeTC2_{mass}"'
            new_samples.append((new_sample_name, sample_dict))
            zprime_samples.append(new_sample_name)
        elif 'Grav' in sample_name:
            mass = sample_name.split('_')[1]
            new_sample_name = f'"Grav{mass}"'
            new_samples.append((new_sample_name, sample_dict))
            grav_samples.append(new_sample_name)
        elif 'KKg' in sample_name:
            mass = sample_name.split('_')[1]
            new_sample_name = f'"KKgMG{mass}"'
            new_samples.append((new_sample_name, sample_dict))
            kkg_samples.append(new_sample_name)
        else:
            new_samples.append((add_quotes(sample_name), sample_dict))
    new_config['Sample'] = new_samples
    return new_config
    


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
        if remove_quotes(k) in bad_samples:
            print('Ignoring bad sample: ' + k)
            continue
        if k not in dict_1l:
            dict_2l[k]['Regions'] = ','.join(regions_2l)
            sample_combined.append((k, dict_2l[k]))
        elif k not in dict_2l:
            dict_1l[k]['Regions'] = ','.join(regions_1l)
            sample_combined.append((k, dict_1l[k]))
        elif 'data' in k.lower():
            sample_combined.append((k, dict_1l[k]))
        else:
            print('Warning: sample ' + k + ' is in both 1l and 2l configs. Combining them.')
            sample_combined.append((k, dict_1l[k]))
    
    # sort sample_combined based on type, then name
    sample_combined.sort(key=lambda x: (x[1]['Type'], x[0]))
    # ensure that any sample with type 'Ghost' is at the front, while otherwise preserving the order
    sample_combined.sort(key=lambda x: x[1]['Type'] == 'GHOST', reverse=True)

    return sample_combined

def combine_systematic(systematic_1l, systematic_2l, regions_1l, regions_2l, background_samples_1l, background_samples_2l, min_syst, max_syst):
    systematic_combined = []
    dict_1l = {k: v for k,v in systematic_1l}
    dict_2l = {k: v for k,v in systematic_2l}
    keys = set(dict_1l.keys()) | set(dict_2l.keys())
    for k in keys:
        if remove_quotes(k) in bad_systematics:
            print('Ignoring bad systematic: ' + k)
            continue
        if k not in dict_1l:
            obj_dict = dict_2l[k]
            obj_dict['Regions'] = ','.join(sorted(regions_2l))
            systematic_combined.append((k, obj_dict))
        elif k not in dict_2l:
            obj_dict = dict_1l[k]
            obj_dict['Regions'] = ','.join(sorted(regions_1l))
            systematic_combined.append((k, obj_dict))
        else:
            print('Warning: systematic ' + k + ' is in both 1l and 2l configs. Combining them.')
            obj_dict = dict_1l[k]
            obj_dict['Regions'] = ','.join(sorted(regions_1l.union(regions_2l)))  
            if 'Samples' in obj_dict and 'Samples' in dict_2l[k]:
                obj_dict['Samples'] = ','.join(sorted(set(remove_quotes(obj_dict['Samples'].split(','))).union(set(remove_quotes(dict_2l[k]['Samples'].split(','))))))
            elif 'Samples' in dict_2l[k] or 'Samples' in obj_dict:
                if 'Samples' in dict_2l[k]:
                    # add background_samples_1l to the list of samples
                    obj_dict['Samples'] = ','.join(sorted(set(remove_quotes(dict_2l[k]['Samples'].split(','))).union(background_samples_1l)))
                else:
                    # add background_samples_2l to the list of samples
                    obj_dict['Samples'] = ','.join(sorted(set(remove_quotes(obj_dict['Samples'].split(','))).union(background_samples_2l)))
                
                print('CHECK CAREFULLY: Samples are not present in one config but are present in the other. Using the union of the listed samples with background samples from the other channel:')
                print('  ' + obj_dict['Samples'])
            if 'Samples' in obj_dict:
                # sort samples by name and add quotes
                obj_dict['Samples'] = ','.join(sorted(remove_quotes(obj_dict['Samples'].split(','))))
                obj_dict['Samples'] = ','.join(['"' + s + '"' for s in obj_dict['Samples'].split(',')])
            # compare Symmetrisation
            if obj_dict.get('Symmetrisation', None) != dict_2l[k].get('Symmetrisation', None):
                print('Warning: Symmetrisation is different for systematic ' + k + '. Using Symmetrisation from 1l config.')
            systematic_combined.append((k, obj_dict))
    
    # Eliminate signal samples from systematics, for now
    print('***Removing signal samples from systematics***')
    for i, (k, obj_dict) in enumerate(systematic_combined):
        if 'Samples' in obj_dict:
            samples = remove_quotes(obj_dict['Samples'].split(','))
            samples = [s for s in samples if (not s.startswith('Zprime') and not s.startswith('Grav') and not s.startswith('KKg'))]
            systematic_combined[i] = (k, obj_dict)
            systematic_combined[i][1]['Samples'] = ','.join(['"' + s + '"' for s in sorted(samples)])

    # sort systematic_combined based on Category, Subcategory (if it exists), then Name
    systematic_combined.sort(key=lambda x: (x[1]['Category'], x[1].get('Subcategory', ''), x[0]))

    # limit the systematics to the range specified by min_syst and max_syst
    num_systs = len(systematic_combined)
    if min_syst < 0:
        min_syst = 0
    if max_syst > num_systs or max_syst < 0:
        max_syst = num_systs
    systematic_combined = systematic_combined[min_syst:max_syst]

    return systematic_combined


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
    if 'ReadFrom' in diff_keys:
        job_combined['ReadFrom'] = 'HIST'
        diff_keys.remove('ReadFrom')
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

def combine_objects(obj_pairs_1l, obj_pairs_2l, obj_type, regions_1l, regions_2l, background_samples_1l, background_samples_2l, min_syst, max_syst):
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
        return combine_systematic(obj_pairs_1l, obj_pairs_2l, regions_1l, regions_2l, background_samples_1l, background_samples_2l, min_syst, max_syst)
    elif obj_type == 'Region':
        return combine_region(obj_pairs_1l, obj_pairs_2l)
    elif obj_type == 'Limit':
        return [('limit', combine_limit(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'Options':
        return [('options', combine_options(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'NormFactor':
        return combine_normfactor(obj_pairs_1l, obj_pairs_2l)
    elif obj_type == 'Job':
        return [('ttRes1L2L', combine_job(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    elif obj_type == 'Significance':
        return [('significance', combine_significance(obj_pairs_1l[0][1], obj_pairs_2l[0][1]))]
    else:
        raise RuntimeError(f'Unknown object type {obj_type}')


def combine_configs(config_1l, config_2l, out_dir, statonly=False, min_syst=-1, max_syst=-1):
    """Combine the 1l and 2l configs into a single config."""
    config_1l = parse_config_file(config_1l, statonly=statonly)
    config_1l = rename_1l(config_1l)
    config_2l = parse_config_file(config_2l, statonly=statonly)
    # go through each object type and combine the objects
    obj_types = set(config_1l.keys()) | set(config_2l.keys())
    type_order = ['Job', 'Options', 'Fit', 'Limit', 'Significance', 'Region', 'Sample', 'NormFactor', 'Systematic']
    config_combined = {}
    regions_1l = set(remove_quotes(t[0]) for t in config_1l['Region'])
    regions_2l = set(remove_quotes(t[0]) for t in config_2l['Region'])
    background_samples_1l = set(remove_quotes(t[0]) for t in config_1l['Sample'] if t[1]['Type'] == 'BACKGROUND')
    background_samples_2l = set(remove_quotes(t[0]) for t in config_2l['Sample'] if t[1]['Type'] == 'BACKGROUND')
    for obj_type in type_order:
        if obj_type not in obj_types:
            continue
        combined_objects = combine_objects(config_1l[obj_type], config_2l[obj_type], obj_type=obj_type, regions_1l=regions_1l, regions_2l=regions_2l, background_samples_1l=background_samples_1l, background_samples_2l=background_samples_2l, min_syst=min_syst, max_syst=max_syst)
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
    parser.add_argument('--min_syst', default=-1, type=int, help='Minimum systematics to include')
    parser.add_argument('--max_syst', default=-1, type=int, help='Maximum systematics to include')

    args = parser.parse_args()
    combine_configs(args.config_1l, args.config_2l, args.out_dir, args.statonly, args.min_syst, args.max_syst)

if __name__ == "__main__":
    main()