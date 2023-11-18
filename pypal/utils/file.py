"""
File utils.

Utilities to handle yaml, and json files.
"""

import yaml


def read_file_as_string(file_path: str) -> str:
    """Read file as a single string.

    Parameters
    ----------
    file_path : str
        Path of the file.

    Returns
    -------
    str
        Contents of the file as a string.
    """
    with open(file_path, "r") as file:
        data = file.read()
    return data


def load_yaml_file(file_path):
    """
    Load the contents of a YAML file into a Python dictionary.

    Args:
    file_path (str): The file path of the YAML file to be loaded.

    Returns:
    dict: The contents of the YAML file as a dictionary.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data
