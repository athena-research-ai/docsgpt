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
from typing import Any
import ast_comments as astcom
from pypal.logger import logger
from pypal.review.agents.openai import AgentOpenAI
# Import necessary modules
from pypal.review.formats import ElementType

def indent_docstring(docstring: str, indent: int):
    """
    Add indentation to docstrings.
    
        Args:
            docstring (str): The input docstring to be indented.
            indent (int): The number of spaces to indent the docstring.
    
        Returns:
            str: The indented docstring.
    """
    # Add indentation to docstrings
    lines = docstring.split('\n')
    spaced_lines = [' ' * indent + line for line in lines]
    if len(lines) > 1:
        spaced_lines = [''] + spaced_lines + [' ' * indent]
    formatted_docstring = '\n'.join(spaced_lines)
    return formatted_docstring

class ReviewerDocstring(astcom.NodeTransformer):
    """
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
        Initializes the ReviewProcess class.
        
            Initializes the ReviewProcess class with the given source and review agent.
        
            Args:
                source (type): Description of source.
                review_agent (type): Description of review_agent.
        
            Returns:
                None: This method does not return anything.
        """
        super().__init__()
        self.source = source
        self.review_agent = review_agent

    def make_docstring(self, node, type):
        """
        Review each function in the file.
        
        This method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.
        
        Args:
            arg1 (str): The path to the file which contains the Python functions to be reviewed.
            arg2 (str): Description of the second argument.
        
        Returns:
            None: None
        """
        code = astcom.get_source_segment(self.source, node)
        # Review the function code
        logger.warning('\n' + code)
        try:
            output = self.review_agent.review(type, code)
        # output = { "doc_string": "Review each function in the file.\n\nThis method uses an AI-based review agent to review each function in the file and then writes the review output back to a new file.\n\nParameters\n----------\nfilepath : str\n    The path to the file which contains the Python functions to be reviewed.\n\nReturns\n-------\nNone\n    None"}
        except AssertionError:
            assert False, 'Review agent failed to review the function.'
        docstring = output['doc_string']
        function_indent = node.col_offset
        docstring = indent_docstring(docstring, function_indent + 4)
        return astcom.Expr(value=astcom.Str(docstring))

    def review_node(self, node, type):
        """
        Updates or adds a docstring to the given node.
        
        This function takes a node and a type as input and generates a new docstring for the given node based on the provided type. If the node already has a docstring, it updates it; otherwise, it adds a new docstring to the beginning of the node's body.
        
        Args:
          node (node): The node for which the docstring is to be updated or added.
          type (type): The type based on which the new docstring is generated.
        
        Returns:
          node: The updated node with the new or modified docstring.
        """
        new_docstring_node = self.make_docstring(node, type)
        if astcom.get_docstring(node):
            # Assumes the existing docstring is the first node
            # in the function body.
            node.body[0] = new_docstring_node
        else:
            node.body.insert(0, new_docstring_node)
        return node

class ReviewerDocstringFunction(ReviewerDocstring):
    """
    class ReviewerDocstringFunction(ReviewerDocstring):
        def visit_FunctionDef(self, node):
            '''
            Short description of the function.
    
            Long description of the function.
            '''
    """

    def visit_FunctionDef(self, node):
        """
        This method is used to visit a FunctionDef node and review the node for a specific element type.
        
        Args:
            self: The instance of the class.
            node: The FunctionDef node to be visited.
        
        Returns:
            review_node: The review_node method applied to the given node.
        """
        return self.review_node(node, ElementType.FUNCTION)

class ReviewerDocstringClass(ReviewerDocstring):
    """
    Class ReviewerDocstringClass
    
        Short description of the class.
    
        Long description of the class.
    
    """

    def visit_ClassDef(self, node):
        """
        This function visits a ClassDef node and reviews it.
        
        Args:
            self: The object itself.
            node (type): The ClassDef node to be visited.
        
        Returns:
            type: The result of reviewing the ClassDef node.
        """
        return self.review_node(node, ElementType.CLASS)

class ReviewerDocstringModule(ReviewerDocstring):
    """
    visit_Module(self, node) -> Any:
        Short description of the method.
    
        Long description of the method.
    
    """

    def visit_Module(self, node) -> Any:
        """
        This function visits the Module node.
        
            Args:
                self: A reference to the current instance of the class.
                node: The Module node to visit.
        
            Returns:
                Any: The result of reviewing the node for the FILE element type.
        """
        return self.review_node(node, ElementType.FILE)

class Reviewer:
    """
    This class represents a code reviewer.
    
            The Reviewer class provides a method to review each function in a given
            file using an AI-based review agent. The initialized review agent
            will attempt to improve the quality of the code and write the review
            output back to a new file. This class includes methods for initializing
            the class and conducting the review process.
            
    """

    def __init__(self) -> None:
        """
        Initialize the Reviewer class with a specific file.
        
                Args:
                    self: the object instance
        
                Returns:
                    None: This function does not return anything.
            
        """
        self.review_agent = AgentOpenAI()  # Initialize the review agent
        logger.info('Hello! I am your code review agent.')
        logger.warning('I will destroy your shit code 😀')

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
        
        Returns
        -------
        None
        
        """
        if filepath.split('.')[-1] != 'py':
            print(f"Extension not supported ({filepath.split('.')[-1]})")
            return
        source = open(filepath).read()
        tree = astcom.parse(source)
        for transformer in [ReviewerDocstringFunction(source, self.review_agent), ReviewerDocstringClass(source, self.review_agent)]:
            transformer.visit(tree)
        astcom.fix_missing_locations(tree)
        new_source = astcom.unparse(tree)
        with open(filepath, 'w') as fd:
            fd.write(new_source)