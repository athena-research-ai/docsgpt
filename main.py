"""
This module provides functionality for performing code reviews.

It includes a main function that parses command line arguments
and calls the appropriate function based on those arguments.
The options are:
* -f/--file to specify a file to process,
* -a/--all to process the entire repo,
* -c/--changes to process only changed files.

Functions
---------
main : The main function that parses command line arguments
        and performs code review.
get_all_files : Returns a list of all files in the repo.
get_changed_files : Returns a list of all files that have been changed.
"""


import argparse
import os
from pathlib import Path

from git import Repo

from pypal.review.reviewer import Reviewer
from pypal.utils.file import get_files

reviewer = Reviewer()


def main():
    """
    Parse command line arguments and perform code review.

    This function parses command line arguments using argparse.
    It supports three options:
        -f/--file to specify a file to process,
        -a/--all to process the entire repo,
        -c/--changes to process only changed files.

    If no arguments are provided, it prints a message asking for arguments.

    Returns
    -------
    None
    """
    parser = argparse.ArgumentParser(description="Perform code review.")
    parser.add_argument(
        "-f",
        "--filepath",
        help="Specify a file to process.",
    )
    parser.add_argument(
        "-c",
        "--changes",
        action="store_true",
        help="Process only changed files.",
    )
    args = parser.parse_args()

    filepaths = []

    if args.filepath:
        if os.path.isfile(args.filepath):
            filepaths = args.filepath
        else:
            filepaths = get_all_files(args.filepath)
    elif args.changes:
        filepaths = get_changed_files()
    else:
        print(
            """No arguments provided.
              Please specify --file, --all, or --changes."""
        )

    for file in filepaths:
        # reviewer.review(file)
        pass


def get_all_files(dir: Path):
    """
    Get all files in the repo.

    Returns
    -------
    list
        A list of all files in the repo.
    """
    return get_files(dir, extension=".py")


def get_changed_files():
    """
    Get all files that have been changed in the latest commit.

    Returns
    -------
    list
        A list of all files that have been changed in the latest commit.
    """
    repo = Repo(os.getcwd())
    changed_files = []

    # Untracked files
    changed_files.extend(repo.untracked_files)

    # Modified and staged files
    diffs = repo.index.diff(None) + repo.index.diff("HEAD")
    for diff in diffs:
        changed_files.append(diff.a_path)

    return list(set(changed_files))


if __name__ == "__main__":
    main()
