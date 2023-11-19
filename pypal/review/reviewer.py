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
from _ast import Module
from typing import Any

from pypal.logger import logger
from pypal.review.agents.openai import AgentOpenAI

# Import necessary modules
from pypal.review.formats import ElementType


def indent_docstring(docstring: str, indent: int):
    # Add indentation to docstrings
    lines = docstring.split("\n")
    spaced_lines = [(" " * (indent)) + line for line in lines]
    if len(lines) > 1:
        spaced_lines = [""] + spaced_lines + [(" " * (indent))]
    formatted_docstring = "\n".join(spaced_lines)
    return formatted_docstring


class ReviewerDocstring(ast.NodeTransformer):
    def __init__(self, source, review_agent) -> None:
        super().__init__()
        self.source = source
        self.review_agent = review_agent

    def make_docstring(self, node, type):
        code = ast.get_source_segment(self.source, node)
        # Review the function code
        logger.warning("\n" + code)
        try:
            output = self.review_agent.review(
                type,
                code,
            )

            # output = { "doc_string": "Review each function in the file.\n\nThis method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.\n\nParameters\n----------\nfilepath : str\n    The path to the file which contains the Python functions to be reviewed.\n\nReturns\n-------\nNone\n    None"}
        except AssertionError:
            assert False, "Review agent failed to review the function."

        docstring = output["doc_string"]
        function_indent = node.col_offset
        docstring = indent_docstring(docstring, function_indent + 4)

        return ast.Expr(value=ast.Str(docstring))

    def review_node(self, node, type):
        new_docstring_node = self.make_docstring(node, type)
        if ast.get_docstring(node):
            # Assumes the existing docstring is the first node
            # in the function body.
            node.body[0] = new_docstring_node
        else:
            node.body.insert(0, new_docstring_node)
        return node


class ReviewerDocstringFunction(ReviewerDocstring):
    def visit_FunctionDef(self, node):
        return self.review_node(node, ElementType.FUNCTION)


class ReviewerDocstringClass(ReviewerDocstring):
    def visit_ClassDef(self, node):
        return self.review_node(node, ElementType.CLASS)


class ReviewerDocstringModule(ReviewerDocstring):
    def visit_Module(self, node: Module) -> Any:
        return self.review_node(node, ElementType.FILE)


class Reviewer:
    def __init__(self) -> None:
        """Initialize the Reviewer class with a specific file."""
        self.review_agent = AgentOpenAI()  # Initialize the review agent
        logger.info("Hello! I am your code review agent.")
        logger.warning("I will destroy your shit code \U0001F600")

    def review(self, filepath: str) -> None:
        """
        Review each function in the file.

        This method uses an AI-based review agent to review
        each function in the file and then writes the review
        output back to a new file.

        Parameters
        ----------
        filepath : str
            The path to the file which contains the
            Python functions to be reviewed.
        """
        if filepath.split(".")[-1] != "py":
            print(f"Extension not supported ({filepath.split('.')[-1]})")
            return
        source = open(filepath).read()
        tree = ast.parse(source)
        for transformer in [
            ReviewerDocstringFunction(source, self.review_agent),
            ReviewerDocstringClass(source, self.review_agent),
        ]:
            transformer.visit(tree)
        ast.fix_missing_locations(tree)

        new_source = ast.unparse(tree)

        with open(filepath, "w") as fd:
            fd.write(new_source)
