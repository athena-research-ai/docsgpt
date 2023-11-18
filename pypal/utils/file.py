"""
File utils.

Utilities to handle yaml, and json files.
"""

import ast
from pathlib import Path
from typing import Dict

import yaml

DIR_CONFIG = Path("configs")
DIR_SECRETS = Path("keys")


class File:
    """A class to represent and interact with a Python source code file."""

    def __init__(self, filepath: str) -> None:
        """
        Initialize the File class with a specific file path.

        This constructor opens the file, reads its content,
        and parses the content to an AST.

        It also identifies functions, classes, and methods
        within the file.

        Parameters
        ----------
        filepath : str
            The path to the file to be processed.
        """
        self.filepath = filepath  # Store the file path
        with open(self.filepath, "r") as file:
            self.content: str = file.read()  # Read the file's content

        self.__content = self.content

        # Parse the file content to an AST (Abstract Syntax Tree)
        self.ast = ast.parse(self.content)

        # Extract functions and classes from the AST
        self.functions = [
            node for node in self.ast.body if isinstance(node, ast.FunctionDef)
        ]
        self.classes = [
            node for node in self.ast.body if isinstance(node, ast.ClassDef)
        ]
        self.methods = (
            []
        )  # Placeholder for methods, can be populated similarly if needed

    def get_node_body(self, node) -> str:
        """
        Retrieve the body of a given node (function or method) as a string.

        This method extracts the source code of a specified AST
        node (typically a function or a method)
        from the file's content.

        Parameters
        ----------
        node : ast.Node
            The AST node for which the body will be extracted.

        Returns
        -------
        str
            The source code of the node as a string.
        """
        # Extract the lines of code corresponding to the node
        return "\n".join(
            self.__content.splitlines()[node.lineno - 1 : node.end_lineno],
        )


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
