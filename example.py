"""
Example usage of AgentOpenAI.

This file includes an example on how to use the code review Agent.
"""

from pypal.review.agents.openai import AgentOpenAI
from pypal.review.formats import ElementType

review_agent = AgentOpenAI()

code = """
    def load_yaml_file(file_path):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
"""

print(review_agent.review(ElementType.FUNCTION, code))
