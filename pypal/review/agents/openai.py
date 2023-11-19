"""
Agent class implementation with OpenAI model.

See Agent.
"""

import json
import os
from pathlib import Path
from typing import Dict

from openai import OpenAI

from pypal.review.agents.agent import Agent
from pypal.review.formats import ElementType
from pypal.utils.file import DIR_CONFIG, load_yaml_file


class AgentOpenAI(Agent):
    """
    Implementation of CodeReview Agent class with OpenAI LLM.

    See base class Agent.
    """

    def __init__(self) -> None:
        """
        Initialize the AgentOpenAI instance.

        Loads necessary secrets and configurations for the OpenAI client.
        """
        super().__init__()

        self.config = load_yaml_file(DIR_CONFIG / Path("openai.yaml"))

        self.client = OpenAI(
            organization=os.environ.get("OPENAI_ORGANIZATION"),
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def _review(self, type: ElementType, content: str) -> Dict:
        """
        Implement review method with OpenAI model.

        See documentation in Agent base class.
        """
        response = self.client.chat.completions.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            top_p=self.config["top_p"],
            frequency_penalty=self.config["frequency_penalty"],
            presence_penalty=self.config["presence_penalty"],
            response_format={"type": "json_object"},
            messages=self._get_system_messages(type)
            + [{"role": "user", "content": content}],
        )

        review = json.loads(response.choices[0].message.content)

        return {
            "doc_string": review["doc_string"],
            # 'comments': []
        }

    def _get_system_messages(self, type: ElementType) -> Dict:
        """
        Get system messages for OpenAI model.

        Args:
            type (ElementType):
                The type of element to be reviewed. It determines the nature
                of the review process.
        """
        base_message = {
            "role": "user",
            "content": """
                Return a single JSON file that contains a
                key 'doc_string' and the associated value
                is a numpy style docstring compliant documentation
                of the function that the users send you as message.

                If the element already has a docstring which is compliant
                and correct, you should return the same docstring.
                Otherwise, you should return a docstring that is compliant
                and correct.

                You should follow the following format for the docstring,
                    make sure to add \n at the end of each line:
                """,
        }

        specific_message = None

        if ElementType.FUNCTION == type or ElementType.METHOD == type:
            specific_message = {
                "role": "user",
                "content": """
                    Short description of the function.

                    Long description of the function.

                    Args:
                        arg1 (type): Description of arg1.
                        arg2 (type): Description of arg2.

                    Returns:
                        type: Description of return value.
                """,
            }
        elif ElementType.CLASS == type:
            specific_message = {
                "role": "user",
                "content": """
                    Short description of the class.

                    Long description of the class.
                """,
            }
        elif ElementType.FILE == type:
            specific_message = {
                "role": "user",
                "content": """
                    Short description of the scope of file.

                    Long description of the file.
                """,
            }
        else:
            assert False, "Not implemented yet!"

        return [base_message, specific_message]
