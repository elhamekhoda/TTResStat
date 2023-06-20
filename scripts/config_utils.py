from collections import defaultdict


def has_indentation(line):
    return line.startswith(' ') or line.startswith('\t')

def remove_quotes(s):
    # check if s is not a string
    if not isinstance(s, str):
        return [remove_quotes(a) for a in s]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    else:
        return s
    
def add_quotes(s):
    # check if s is not a string
    if not isinstance(s, str):
        return [add_quotes(a) for a in s]
    if s.startswith('"') and s.endswith('"'):
        return s
    else:
        return '"' + s + '"'

def split_objects(config, sep=';'):
    """Split objects with names separated by semicolons."""
    new_config = defaultdict(dict)
    for obj_type, obj_dict in config.items():
        for obj_name, obj_config in obj_dict.items():
            obj_names = [x for x in obj_name.split(sep) if x]
            unified_keys = set()
            for key, value in obj_config.items():
                obj_config[key] = [v for v in value.split(sep) if v]
                if len(obj_config[key]) == 1:
                    unified_keys.add(key)
                elif len(obj_config[key]) != len(obj_names):
                    raise RuntimeError('Number of values for key ' + key + ' does not match number of objects.')
            for obj_name in obj_names:
                new_obj_dict = {}
                for key, values in obj_config.items():
                    if key in unified_keys:
                        new_obj_dict[key] = values[0].strip()
                    else:
                        new_obj_dict[key] = values.pop(0).strip()
                new_config[obj_type][obj_name.strip()] = new_obj_dict
    return new_config

def parse_config_string(config_string, statonly=False):
    """Parse a config string into a dictionary. Each object type is a key in the dictionary, and the value is list of (object name, dictionary) pairs, where dictionary contains the object's attributes.
    
    Parameters
    ----------
    config_string : str
        The config string
    statonly : bool
        If True, ignore systematics"""
    
    lines = config_string.split('\n')

    config = defaultdict(dict)
    current_obj_name = None
    current_obj_type = None
    current_obj_dict = {}
    
    for line in lines:
        # Ignore comments and blank lines
        stripped_line = line.strip()
        if stripped_line.startswith('%') or stripped_line.startswith('#') or not stripped_line:
            continue
        
        if has_indentation(line):
            # This is a continuation of the current object
            if ':' in stripped_line:
                key, value = stripped_line.split(':', 1)
                key = key.strip()
                value = value.strip()
                current_obj_dict[key] = value
        else:
            # This is a new object
            # First, save the current object
            if current_obj_name is not None:
                assert current_obj_name not in config[current_obj_type], f'Object {current_obj_name} already exists in config'
                config[current_obj_type][current_obj_name] = current_obj_dict
            current_obj_dict = {}
            # Now, parse the new object
            if ':' in stripped_line:
                current_obj_type, current_obj_name = stripped_line.split(':', 1)
                current_obj_type = current_obj_type.strip()
                current_obj_name = current_obj_name.strip()
            else:
                current_obj_type = None
                current_obj_name = None

    # Save the last object
    if current_obj_name is not None:
        assert current_obj_name not in config[current_obj_type], f'Object {current_obj_name} already exists in config'
        config[current_obj_type][current_obj_name] = current_obj_dict

    # Remove systematics if statonly is True
    if statonly:
        if 'Systematic' in config:
            del config['Systematic']

    # split objects with names separated by semicolons
    config = split_objects(config)

    return config

def parse_config_file(file_path, statonly=False):
    """Parse a config file into a dictionary. Each object type is a key in the dictionary, and the value is list of (object name, dictionary) pairs, where dictionary contains the object's attributes.
    
    Parameters
    ----------
    file_path : str
        Path to the config file
    statonly : bool
        If True, ignore systematics"""
    
    with open(file_path, 'r') as f:
        config_string = f.read()
    
    return parse_config_string(config_string, statonly)

def config_to_string(config, statonly):
    def align_entries(obj_dict, sep=';'):
        # combine the values of each key into a single string, separated by sep.
        # Ensure that the separators are aligned by padding with spaces.

        # first, find the maximum length of each value for each column
        max_lengths = [0] * max([len(values) for values in obj_dict.values() if type(values) is not str], default=0)
        for i in range(len(max_lengths)):
            for values in obj_dict.values():
                if type(values) is str:
                    continue
                max_lengths[i] = max(len(values[i]), max_lengths[i])

        # now, pad each value with spaces
        for key, values in obj_dict.items():
            if type(values) is str:
                obj_dict[key] = values
            else:
                obj_dict[key] = [value.ljust(max_lengths[i]) for i, value in enumerate(values)]

        # finally, combine the values into a single string
        for key, values in obj_dict.items():
            if type(values) is str:
                obj_dict[key] = values
            else:
                obj_dict[key] = sep.join(values)

        return obj_dict
    
    def combine_objects(obj_dict_list):
        # check that all dicts have the same keys
        keys = set()
        for _, obj_dict in obj_dict_list:
            keys.update(obj_dict.keys())
        for _, obj_dict in obj_dict_list:
            if set(obj_dict.keys()) != keys:
                breakpoint()
                raise RuntimeError('Cannot combine objects with different keys: ' + str(obj_dict.keys()) + ' and ' + str(keys))

        new_obj_dict = {}
        for key in keys:
            new_obj_dict[key] = []
            for obj_name, obj_dict in obj_dict_list:
                new_obj_dict[key].append(obj_dict[key])
            # if all values are the same, just keep one
            if len(set(new_obj_dict[key])) == 1:
                new_obj_dict[key] = new_obj_dict[key][0]
        new_obj_dict = align_entries(new_obj_dict)
        return new_obj_dict
    
    config_string = ''
    for obj_type, obj_dict in config.items():
        if obj_type.lower() == 'systematic' and statonly:
            continue
        if obj_type.lower() == 'systematic':
            # combine systematics with the same category and subcategory
            new_obj_dict = defaultdict(dict)
            # map from (category, subcategory) to list of (name, dict) pairs
            category_dict = defaultdict(list)
            for obj_name, obj_settings in obj_dict.items():
                if 'Category' not in obj_settings:
                    category = 'None'
                else:
                    category = obj_settings['Category']
                if 'SubCategory' not in obj_settings:
                    subcategory = 'None'
                else:
                    subcategory = obj_settings['SubCategory']
                if subcategory == 'None' or category == 'None':
                    new_obj_dict[obj_name] = obj_settings
                else:
                    category_dict[(category, subcategory)].append((obj_name, obj_settings))
            
            for _, obj_list in category_dict.items():
                # check that all dicts have the same keys
                keys = set()
                for _, obj_dict in obj_list:
                    keys.update(obj_dict.keys())
                can_combine = True
                for _, obj_dict in obj_list:
                    if set(obj_dict.keys()) != keys:
                        can_combine = False
                if not can_combine:
                    for name, obj_dict in obj_list:
                        new_obj_dict[name] = obj_dict
                    continue
                
                names = [name for name, _ in obj_list]
                new_name = ';'.join(names)
                new_obj_dict[new_name] = combine_objects(obj_list)
            
            obj_dict = new_obj_dict

        if obj_type.lower() == 'sample':
            # combine samples with the same prefix, either 'Zprime', 'Grav', or 'KKg'
            new_obj_dict = defaultdict(dict)
            # map from prefix to list of (name, dict) pairs
            prefix_dict = defaultdict(list)
            for obj_name, obj_settings in obj_dict.items():
                if obj_name.startswith('"Zprime'):
                    prefix = 'Zprime'
                elif obj_name.startswith('"Grav'):
                    prefix = 'Grav'
                elif obj_name.startswith('"KKg'):
                    prefix = 'KKg'
                else:
                    new_obj_dict[obj_name] = obj_settings
                    continue
                prefix_dict[prefix].append((obj_name, obj_settings))
            
            for _, obj_list in prefix_dict.items():
                # check that all dicts have the same keys
                keys = set()
                for _, obj_dict in obj_list:
                    keys.update(obj_dict.keys())
                can_combine = True
                for _, obj_dict in obj_list:
                    if set(obj_dict.keys()) != keys:
                        can_combine = False
                if not can_combine:
                    for name, obj_dict in obj_list:
                        new_obj_dict[name] = obj_dict
                    continue
                
                names = [name for name, _ in obj_list]
                new_name = ';'.join(names)
                new_obj_dict[new_name] = combine_objects(obj_list)

            obj_dict = new_obj_dict

        for obj_name, obj_settings in obj_dict.items():
            config_string += f'{obj_type}: {obj_name}\n'
            # get the length of the longest key
            max_key_length = max([len(key) for key in obj_settings.keys()])
            for key, value in sorted(obj_settings.items(), key=lambda x: x[0]):
                # Pad between the '{key}:' and the value with spaces so that the values line up. Make sure the spaces are after the colon.
                config_string += f'  {(key+":").ljust(max_key_length+1)} {value}\n'
            config_string += '\n'
    return config_string

def write_config(config, file_path, statonly=False):
    """Write a config dictionary to a file."""
    with open(file_path, 'w') as f:
        f.write(config_to_string(config, statonly))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Parse and write a config file')
    parser.add_argument('input_file', help='Input config file')
    parser.add_argument('output_file', help='Output config file')
    parser.add_argument('--statonly', action='store_true', help='Ignore systematics')
    args = parser.parse_args()

    config = parse_config_file(args.input_file, args.statonly)
    write_config(config, args.output_file, args.statonly)


if __name__ == '__main__':
    main()