"""
File utils.

Utilities to handle yaml, and json files.
"""

from pathlib import Path
from typing import Dict

import yaml

DIR_CONFIG = Path("configs")
DIR_SECRETS = Path("keys")


def load_yaml_file(file_path: Path) -> Dict:
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
