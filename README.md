# gpt-docs
GPT pre-commit + CI for mantaining up-to-date documentation and catch mis-specifications.

TODO Title, description, and beautiful image in assets/overview.png

<p align='center'><img src='assets/overview.png' alt='Overview.' width='100%'> </p>

## Installation

To setup the corresponding `conda` environment run:
```
conda create --name gpt-docs python=3.11.4
conda activate gpt-docs

conda update -n base -c defaults conda
pip install --upgrade pip
```
Install requirements and dependencies via:
```
pip install -r requirements.txt
```
To install `gpt-docs` run:
```
python setup.py develop
```
Package requirements and dependencies are listed in `requirements.txt`.

## Usage
TODO explain here how to run the main, the arguments, etc.

## Support & Contributing
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

### pre-commit
pre-commit automatically formats code to ensure a consistent style.
You need to install the following python packages (already in requirements.txt):
```
pip install pre-commit pep8-naming flake8 flake8-docstrings
```
Your code will be checked before each commit after you installed the git hook in your git repository:
```
pre-commit install
```
If you want to remove checking for a certain error, you can add it to the ignore list in the .flake8 file (try to comply with your code first).


## Contact
In case you have questions, please contact [Pietro Zullo](mailto:pzullo@alter-ego.ai) and [Antonio Terpin](mailto:aterpin@ethz.ch).

## License
TODO MIT
