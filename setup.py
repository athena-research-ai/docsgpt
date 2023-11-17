#!/usr/bin/python3
"""
setup.py for the gpt-docs package.

This setup script is used to install, build, and distribute the gpt-docs.
It defines the package's metadata, dependencies, and other configuration
necessary to package and distribute the project.

Examples of use (TODO test):
- Installing the package locally: `python setup.py install`
- Building the package: `python setup.py sdist`
- Uploading the package to PyPI: `python setup.py sdist upload`
"""

from setuptools import find_packages, setup

setup(
    name="gpt-docs",
    version="1.0",
    description="""
    GPT pre-commit + CI for mantaining up-to-date documentation
    and catch mis-specifications.""",
    url="https://github.com/antonioterpin/gpt-docs",
    author="Pietro Zullo, Antonio Terpin",
    author_email="aterpin@ethz.ch",
    license="TODO",
    packages=find_packages(),
    # test_suite='nose.collector',
    # tests_require=['nose'],
    install_requires=[],
    zip_safe=False,
)
