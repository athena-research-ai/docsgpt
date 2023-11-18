"""
Agent class implementation with OpenAI model.

See Agent.
"""

import json
from pathlib import Path
from typing import Dict

from openai import OpenAI

from pypal.review.agents.agent import Agent
from pypal.review.formats import ElementType
from pypal.utils.file import DIR_CONFIG, DIR_SECRETS, load_yaml_file


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
        secrets = load_yaml_file(
            DIR_SECRETS / Path("openai") / Path("secrets.yaml"),
        )

        self.config = load_yaml_file(DIR_CONFIG / Path("openai.yaml"))

        self.client = OpenAI(
            organization=secrets["org"],
            api_key=secrets["key"],
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
        Generate system messages.

        Args:
            type (ElementType):
                The type of element for which messages are being generated.

        Returns:
            Dict:
                A list of system messages to be sent to the OpenAI model.

        Raises:
            AssertionError: If the ElementType is not supported.
        """
        if ElementType.FUNCTION != type:
            assert False, "Not implemented yet!"

        return [
            {
                "role": "system",
                "content": """
                    You are a helpful assistant designed to output JSON.
                """,
            },
            {
                "role": "system",
                "content": """
                    The JSON contains a key 'doc_string' and
                    the associated value is a docstring compliant documentation
                    of the function that the users send you as message.
                """,
            },
        ]
