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
from _ast import Module
import ast
from typing import Any
from pypal.logger import logger
from pypal.review.agents.openai import AgentOpenAI
from pypal.review.formats import ElementType

def indent_docstring(docstring: str, indent: int):
    """
    Review each function in the file.
    
    This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
    
    Parameters
    ----------
    filepath : str
        The path to the file which contains the Python functions to be reviewed.
    
    Returns
    -------
    None
        None
    """
    lines = docstring.split('\n')
    spaced_lines = [' ' * indent + line for line in lines]
    if len(lines) > 1:
        spaced_lines = [''] + spaced_lines + [' ' * indent]
    formatted_docstring = '\n'.join(spaced_lines)
    return formatted_docstring

class ReviewerDocstring(ast.NodeTransformer):
    """
    Review each function in the file.
    
    This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
    
    Parameters
    ----------
    filepath : str
        The path to the file which contains the Python functions to be reviewed.
    
    Returns
    -------
    None
        None
    """

    def __init__(self, source, review_agent) -> None:
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        super().__init__()
        self.source = source
        self.review_agent = review_agent

    def make_docstring(self, node, type):
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        code = ast.get_source_segment(self.source, node)
        logger.warning('\n' + code)
        try:
            output = {'doc_string': 'Review each function in the file.\n\nThis method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.\n\nParameters\n----------\nfilepath : str\n    The path to the file which contains the Python functions to be reviewed.\n\nReturns\n-------\nNone\n    None'}
        except AssertionError:
            assert False, 'Review agent failed to review the function.'
        docstring = output['doc_string']
        function_indent = node.col_offset
        docstring = indent_docstring(docstring, function_indent + 4)
        return ast.Expr(value=ast.Str(docstring))

    def review_node(self, node, type):
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        new_docstring_node = self.make_docstring(node, type)
        if ast.get_docstring(node):
            node.body[0] = new_docstring_node
        else:
            node.body.insert(0, new_docstring_node)
        return node

class ReviewerDocstringFunction(ReviewerDocstring):
    """
    Review each function in the file.
    
    This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
    
    Parameters
    ----------
    filepath : str
        The path to the file which contains the Python functions to be reviewed.
    
    Returns
    -------
    None
        None
    """

    def visit_FunctionDef(self, node):
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        return self.review_node(node, ElementType.FUNCTION)

class ReviewerDocstringClass(ReviewerDocstring):
    """
    Review each function in the file.
    
    This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
    
    Parameters
    ----------
    filepath : str
        The path to the file which contains the Python functions to be reviewed.
    
    Returns
    -------
    None
        None
    """

    def visit_ClassDef(self, node):
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        return self.review_node(node, ElementType.CLASS)

class ReviewerDocstringModule(ReviewerDocstring):
    """
    Review each function in the file.
    
    This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
    
    Parameters
    ----------
    filepath : str
        The path to the file which contains the Python functions to be reviewed.
    
    Returns
    -------
    None
        None
    """

    def visit_Module(self, node: Module) -> Any:
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        return self.review_node(node, ElementType.FILE)

class Reviewer:
    """
    Review each function in the file.
    
    This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
    
    Parameters
    ----------
    filepath : str
        The path to the file which contains the Python functions to be reviewed.
    
    Returns
    -------
    None
        None
    """

    def __init__(self) -> None:
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        self.review_agent = AgentOpenAI()
        logger.info('Hello! I am your code review agent.')
        logger.warning('I will destroy your shit code 😀')

    def review(self, filepath: str) -> None:
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Parameters
        ----------
        filepath : str
            The path to the file which contains the Python functions to be reviewed.
        
        Returns
        -------
        None
            None
        """
        source = open(filepath).read()
        tree = ast.parse(source)
        for transformer in [ReviewerDocstringFunction(source, self.review_agent), ReviewerDocstringClass(source, self.review_agent)]:
            transformer.visit(tree)
        ast.fix_missing_locations(tree)
        new_source = ast.unparse(tree)
        with open(filepath.split('.py')[0] + '_review.py', 'w') as fd:
            fd.write(new_source)