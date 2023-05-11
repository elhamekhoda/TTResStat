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
    new_config = defaultdict(list)
    for obj_type, obj_pairs in config.items():
        for obj_name, obj_dict in obj_pairs:
            obj_names = [x for x in obj_name.split(sep) if x]
            unified_keys = set()
            for key, value in obj_dict.items():
                obj_dict[key] = [v for v in value.split(sep) if v]
                if len(obj_dict[key]) == 1:
                    unified_keys.add(key)
                elif len(obj_dict[key]) != len(obj_names):
                    raise RuntimeError('Number of values for key ' + key + ' does not match number of objects.')
            for obj_name in obj_names:
                new_obj_dict = {}
                for key, values in obj_dict.items():
                    if key in unified_keys:
                        new_obj_dict[key] = values[0].strip()
                    else:
                        new_obj_dict[key] = values.pop(0).strip()
                new_config[obj_type].append((obj_name.strip(), new_obj_dict))
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

    config = defaultdict(list)
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
                config[current_obj_type].append((current_obj_name, current_obj_dict))
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
        config[current_obj_type].append((current_obj_name, current_obj_dict))

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
    config_string = ''
    for obj_type, obj_pairs in config.items():
        if obj_type.lower() == 'systematic' and statonly:
            continue
        for obj_name, obj_dict in obj_pairs:
            config_string += f'{obj_type}: {obj_name}\n'
            for key, value in sorted(obj_dict.items(), key=lambda x: x[0]):
                config_string += f'  {key}: {value}\n'
            config_string += '\n'
    return config_string

def write_config(config, file_path, statonly=False):
    """Write a config dictionary to a file."""
    with open(file_path, 'w') as f:
        f.write(config_to_string(config, statonly))



def main():
    from pathlib import Path
    nosig_config_path = Path('/home/schuya/ttres1lepstat/run/statResults_ttres1L2L_2023-05-09_1l_nosigsyst_test/zprime_4000/ttres1L.config')
    nosig_config = parse_config_file(nosig_config_path)
    out_path = nosig_config_path.parent / 'ttres1L_nosigsyst_test.config'
    write_config(nosig_config, out_path)


if __name__ == '__main__':
    main()