"""
Code review agent.

This module defines the architecture for creating agents that perform
code reviews in an automated system.
It provides the `Agent` class, an abstract base class for such agents,
along with necessary imports and utilities to support the review process.
"""

from abc import ABC, abstractmethod
from typing import Dict

from pypal.review.formats import OUTPUT_FORMAT, ElementType
from pypal.utils.dict import check_format


class Agent(ABC):
    """
    Abstract base class responsible for performing code reviews.

    This class provides a framework for agents that can review code.
    It defines an abstract method `review` that must be implemented
    by subclasses.
    The method is intended to take a type of element and its content,
    then return a dictionary with the review results.

    Attributes:
        None

    Methods:
        review(type: ElementType, content: str) -> Dict
            Perform the review of content
        _review(type: ElementType, content: str) -> Dict
            Abstract method to be implemented by subclasses for reviewing code.
    """

    def review(self, type: ElementType, content: str) -> Dict:
        """
        Perform a code review based on the specified element type and content.

        This method serves as a wrapper around the `_review` method.
        It calls `_review` with the given parameters and then validates
        the format of the result against a predefined `OUTPUT_FORMAT`.
        If the result does not conform to the expected format,
        an AssertionError is raised.

        Args:
            type (ElementType):
                The type of element to be reviewed. It determines the nature
                of the review process.

            content (str):
                The actual content of the code element to be reviewed.

        Returns:
            Dict:
                A dictionary containing the results of the review.
                It complies with `OUTPUT_FORMAT`.

        Raises:
            AssertionError: If the result from `_review` does not comply
            with the expected `OUTPUT_FORMAT`.

        Note:
            The actual review logic should be implemented in
            the `_review` method by subclasses.
            This method is intended to be a common interface that also
            includes result validation.
        """
        review_result = self._review(type, content)
        assert check_format(
            review_result, OUTPUT_FORMAT
        ), "Result provided by _review is not compliant"

        return review_result

    @abstractmethod
    def _review(self, type: ElementType, content: str) -> Dict:
        """
        Abstract method to perform a review of the given content.

        This method should be implemented by subclasses to define how
        the review process is carried out.
        The implementation should analyze the content based
        on the provided type and return the review findings.

        Args:
            type (ElementType): The type of element to be reviewed.
            content (str): The content of the element to be reviewed.

        Returns:
            Dict: A dictionary containing the results of the review.
        """
        pass
