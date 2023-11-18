"""
Code review element types.

This module defines the structure and types used in a code review process.
It includes an enumeration for different types of code elements,
along with specifications for input and output formats in the review process.

The module primarily consists of:
- `ElementType`:
    An enumeration that categorizes various elements in a code base,
    such as functions, methods, classes, files, and the entire code base.
- `INPUT_FORMAT`:
    A dictionary format that outlines the expected structure of input data
    for a review process, including the type of code element and its content.
- `OUTPUT_FORMAT`:
    A dictionary format defining the expected structure of output data from
    the review process, including a docstring and a list of comments.

This module is intended to be used in systems that automate or assist
with the code review process, providing standard formats and types
for consistent processing and analysis of code.
"""

from enum import Enum


class ElementType(Enum):
    """
    Enumeration representing different types of elements in a code base.

    This enum is used to categorize various elements that can be found
    in a code base, facilitating operations that need
    to differentiate between these types.

    Attributes:
        FUNCTION (int): Represents a function in the code.
        METHOD (int): Represents a method in the code.
        CLASS (int): Represents a class in the code.
        FILE (int): Represents a file in the code.
        CODE_BASE (int): Represents the entire code base.
    """

    FUNCTION = 0
    METHOD = 1
    CLASS = 2
    FILE = 3
    CODE_BASE = 4


# Dictionary representing the expected format of input data.

# The `INPUT_FORMAT` dictionary is used to specify the structure and types of
# data that are expected as input. It includes keys for 'type',
# indicating the ElementType of the code element, and 'content',
# which contains the actual code as a string.

# Attributes:
#     type (ElementType): The type of code element.
#     content (str): The actual code content as a string.
INPUT_FORMAT = {
    "type": ElementType,
    "content": str,
}

# Dictionary representing the format of the output data.

# The `OUTPUT_FORMAT` dictionary outlines the structure and types of data that
# are expected as output. It includes a 'doc_string' key
# for the docstring of the reviewed code snippet,
# and a 'comments' key, which is a list of comments.

# Attributes:
#     doc_string (str): The docstring of the reviewed code snippet.
#     comments (list): A list of comments related to the code review.
OUTPUT_FORMAT = {
    "doc_string": str,
    # "comments": [],
}
