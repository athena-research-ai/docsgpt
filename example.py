"""
Example usage of AgentOpenAI.

This file includes an example on how to use the code review Agent.
"""

from pypal.review.reviewer import Reviewer

# Fiel you want to document
filepath: str = "pypal/mock_data/test_function.py"

reviewer = Reviewer(filepath)
reviewer.review()
