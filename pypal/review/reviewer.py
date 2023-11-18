"""
This module provides functionality for reviewing Python source code files.

It focuses on function implementations and documentation, using an AI-based
review agent from `pypal.review.agents.openai` to analyze functions in a file.

Classes:
    Reviewer: Handles reviewing Python functions in a file. It reads the file,
    uses the AI agent for review, and writes the output to a new file.

The module works with Python source files, extracting functions and docstrings,
and applies AI-based analysis for insights or suggestions.

Example:
    To use `Reviewer`, initialize with a file path:
    ```python
    from pypal.review import Reviewer

    reviewer = Reviewer("path/to/python_file.py")
    reviewer.review()
    ```

Dependencies:
    - ast: Parses Python code into abstract syntax trees.
    - pypal.logger: Logs details during the review process.
    - pypal.review.agents.openai: Provides the AI-based review agent.
    - pypal.review.formats: Defines review process formats.
    - pypal.utils.file: Manages file operations.
"""

import ast

from pypal.logger import logger
from pypal.review.agents.openai import AgentOpenAI

# Import necessary modules
from pypal.review.formats import OUTPUT_FORMAT, ElementType
from pypal.utils.file import File


class Reviewer:
    """Class to handle the review process of Python functions in a file."""

    def __init__(self, filepath: str) -> None:
        """
        Initialize the Reviewer class with a specific file.

        Parameters
        ----------
        filepath : str
            The path to the file which contains the
            Python functions to be reviewed.
        """
        self.filepath = filepath  # Store the provided file path
        self.file = File(
            self.filepath
        )  # Create a File object for handling file operations
        logger.info("Hello! I am your code review agent.")
        logger.warning("I will destroy your shit code \U0001F600")
        self.write_offset = 0

    def review(self):
        """
        Review each function in the file.

        This method uses an AI-based review agent to review
        each function in the file and then writes the review
        output back to a new file.
        """
        review_agent = AgentOpenAI()  # Initialize the AI-based review agent

        # Iterate over functions in the file
        for function in self.file.functions:
            function_name = function.name  # Extract the function name
            logger.critical(f"Currently analyzing this shit : {function_name}")
            # Logging various details about the function
            # Review the function code
            code = self.file.get_node_body(function)
            logger.warning(code)
            try:
                output: OUTPUT_FORMAT = review_agent.review(
                    ElementType.FUNCTION,
                    code,
                )
            except AssertionError:
                logger.error(
                    (
                        f"Function {function_name} ",
                        "could not be processed",
                    )
                )

            logger.warning("YOUR DOCSTRING SUCK")
            self.write_review_to_file(
                function, output
            )  # Write the review to a new file

    def write_review_to_file(self, function, review: OUTPUT_FORMAT):
        """
        Write the review output to a new file.

        Parameters
        ----------
        function : ast.FunctionDef
            The function node being reviewed.
        review : OUTPUT_FORMAT
            The review output format containing the reviewed docstring.
        """
        print(self.write_offset)
        # Define the path for the reviewed file
        self.outpath = self.filepath.split(".py")[0] + "_review.py"
        indent = function.col_offset  # Indentation level of the function

        # Get the initial docstring of the function, if it exists
        initial_docstring = ast.get_docstring(function)
        original_length = len(initial_docstring.splitlines())

        # Format the new docstring with proper indentation
        docstring = review["doc_string"]
        formatted_docstring = '"""\n' + docstring + '\n"""'
        lines = formatted_docstring.split("\n")
        spaced_lines = [(" " * (indent + 4)) + line for line in lines]
        formatted_docstring = "\n".join(spaced_lines)
        new_length = len(formatted_docstring.splitlines())

        if initial_docstring is not None:
            # Replace the old docstring with the new one
            lines = self.file.content.splitlines()
            quotes = [i for i, line in enumerate(lines) if '"""' in line]
            for idx in reversed(range(quotes[0], quotes[1] + 1)):
                del lines[self.write_offset + idx]
            lines.insert(quotes[0] + self.write_offset, formatted_docstring)
            self.file.content = "\n".join(lines)
            self.write_offset += new_length - original_length
        else:
            # Insert the new docstring
            lines = self.file.content.splitlines()
            lines.insert(
                self.write_offset + function.lineno,
                formatted_docstring,
            )
            self.file.content = "\n".join(lines)
            self.write_offset += new_length

        logger.timing(f"Find a better file at :{self.outpath}")
        # Write the updated content with the new docstring to a file
        with open(self.outpath, "w") as file:
            file.write(self.file.content)


# Main execution block
if __name__ == "__main__":
    rev = Reviewer(
        "pypal/mock_data/test_function.py"
    )  # Initialize the Reviewer with a file path
    rev.review()  # Start the review process
