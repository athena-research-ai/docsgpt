#!/usr/bin/python3
# author: Charlotte Bunne
# imports
import jax
import yaml
import collections
import ml_collections
def count_parameters(model):
    """
    Count the total number of parameters in the model.
    
    
    Args:
        model (object): The model for which the parameters need to be counted.
    
    Returns:
        int: The total number of parameters in the model.
    """
    return sum(map(lambda x: x.size, jax.tree_flatten(model)[0]))
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    """
    dot.notation access to dictionary attributes. This class provides dot.notation access to dictionary attributes. It allows accessing dictionary values as if they were object attributes.
    
    Args:
        arg1 (type): Description of arg1.
        arg2 (type): Description of arg2.
    
    Returns:
        type: Description of return value.
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self):
        """
        Initializes a new instance of the class.
        
        This method is the constructor for the class and is called when a new instance of the class is created.
        
        Args:
            self (object): The object itself.
        
        Returns:
            None: This method does not return anything.
        """
        pass
def nest_dict(d):
    """
    Creates a recursively nested dictionary from the given input dictionary.
    
    This function splits the keys of the input dictionary to form a nested dictionary.
    
    Args:
        d (dict): The input dictionary.
    
    Returns:
        dict: The recursively nested dictionary.
    """
    result = {}
    for k, v in d.items():
        # for each key split_rec splits keys to form recursively nested dict
        split_rec(k, v, result)
    return result
def split_rec(k, v, out, sep='.'):
    """
    This function takes a key-value pair, splits the key by a specified separator, and recursively calls itself to break items on '.'. If the key contains a '.', it will split the key into multiple parts and create nested dictionaries accordingly. If no further splitting is needed, the value is assigned to the resulting key. The default separator is '.'.
    
    Args:
        k (str): The key to be split.
        v (any): The value associated with the key.
        out (dict): The output dictionary for storing the split key-value pairs.
        sep (str): The separator used for splitting the key (default is '.').
    
    Returns:
        None: This function does not return a value.
    """
    # splitting keys in dict, calling recursively to break items on '.'
    k, *rest = k.split(sep, 1)
    if rest:
        split_rec(rest[0], v, out.setdefault(k, {}))
    else:
        out[k] = v
def flat_dict(d, parent_key='', sep='.'):
    """
    Flattens a dictionary by converting nested keys into a single level, using a separator if needed.
    
    This function takes a dictionary 'd' and recursively flattens it by combining nested keys into a single level with the specified separator. If a value is a nested dictionary, the function recursively flattens it as well.
    
    Args:
      d (dict): The input dictionary to be flattened.
      parent_key (str, optional): The parent key to be used in recursion. Defaults to ''.
      sep (str, optional): The separator used to combine nested keys. Defaults to '.'.
    
    Returns:
      dict: The flattened dictionary with combined keys.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flat_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
def config_from_wandb(path):
    config = yaml.load(open(path), yaml.UnsafeLoader)
    del config['wandb_version']
    del config['_wandb']
    for key, val in config.items():
        val = val['value']
        config[key].pop('desc', None)
        config[key].pop('value', None)
        config[key] = val
    return ml_collections.ConfigDict(nest_dict(config))