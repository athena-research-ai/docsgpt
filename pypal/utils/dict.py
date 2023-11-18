"""
Dictionaries utils.

Contains various utils to handle dictionaries.
"""

from typing import Dict


def check_format(input_dict: Dict, format_spec: Dict) -> bool:
    """
    Check if the given dictionary complies with the specified format.

    Args:
        input_dict (dict): The dictionary to be checked.
        format_spec (dict): A dictionary specifying the expected format.
                            The keys are the expected keys in input_dict,
                            and the values are the expected types for
                            the corresponding keys in input_dict.

    Returns:
        bool: True if input_dict complies with format_spec, False otherwise.

    Example:
    >>> format_spec = {'name': str, 'age': int, 'skills': list}
    >>> input_dict_correct
            = {'name': 'John', 'age': 30, 'skills': ['Python','JavaScript']}
    >>> input_dict_wrong
            = {'name': 'John', 'skills': ['Python','JavaScript']}
    >>> check_format(input_dict, input_dict_wrong) # False
    >>>

    """
    # Check if all keys in format_spec are in input_dict
    if not all(key in input_dict for key in format_spec):
        return False

    # Check if the type of each value in input_dict matches
    # the type in format_spec
    for key, value_type in format_spec.items():
        if not isinstance(input_dict.get(key, None), value_type):
            return False

    return True
