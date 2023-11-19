"""
Example usage of AgentOpenAI.

This file includes an example on how to use the code review Agent.
"""

from pypal.review.reviewer import Reviewer

# Fiel you want to document
filepath: str = "pypal/review/reviewer.py"

reviewer = Reviewer(filepath)
reviewer.review()
