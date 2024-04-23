import argparse
import os
import re
from typing import Any, Callable

import tqdm

from .printer import print_log


def _walk_files_internal(
    root: str,
    current_dir: str,
    callback: Callable[[str, str], None],
    compiled_pattern: re.Pattern[str],
    progress_bar: tqdm.tqdm | None = None,
) -> None:
    """
    Internal function for recursively walking files in a directory and applying a callback function.

    Args:
        root (str): The root directory to start the search from.
        current_dir (str): The current directory being processed.
        callback (Callable[[str, str], None]): The callback function to apply to matching files.
        compiled_pattern (re.Pattern[str]): A regular expression pattern to match file names.
        progress_bar (tqdm.tqdm | None): An optional progress bar.

    Returns:
        None: The function returns nothing.
    """
    for entry in os.scandir(current_dir):
        full_path = entry.path
        if entry.is_dir():
            _walk_files_internal(
                root, full_path, callback, compiled_pattern, progress_bar
            )
        elif entry.is_file() and compiled_pattern.search(entry.name):
            callback(root, full_path)
            if progress_bar:
                progress_bar.update()


def walk_files(
    root: str,
    callback: Callable[[str, str], None],
    file_name_regex: str | re.Pattern[str] | None,
) -> None:
    """
    Recursively walks through files in a directory and applies a callback function to matching files.

    Args:
        root (str): The root directory to start the search from.
        callback (Callable[[str, str], None]): A callback function that takes two string arguments
            (full file path and file name) and returns None.
        file_name_regex (str | re.Pattern[str]): A regular expression pattern (str or compiled pattern)
            to match file names.

    Returns:
        None: This function returns nothing.

    Example:
        To print the names of all text files in a directory and its subdirectories:

        ```python
        import re

        def print_text_files(full_path, file_name):
            if re.search(r'\.txt$', file_name):
                print(file_name)

        walk_files('/path/to/directory', print_text_files, r'.*\.txt$')
        ```
    """
    if file_name_regex is None:
        file_name_regex = r".*"
    if isinstance(file_name_regex, str):
        compiled_pattern: re.Pattern[Any] = re.compile(file_name_regex, re.I)
    else:
        compiled_pattern = file_name_regex

    progress_bar = tqdm.tqdm(total=0, unit="file(s)", desc="Walking Directory")

    def count_total_files(file_path, file_name):
        progress_bar.reset(progress_bar.total + 1)

    print_log(f"Calculating directory size...")
    _walk_files_internal(root, root, count_total_files, compiled_pattern)
    _walk_files_internal(root, root, callback, compiled_pattern, progress_bar)


def validate_file_path(file_path):
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(
            f"'{file_path}' is neither a file nor a directory!"
        )
    return file_path


def validate_file_path_dir(file_path):
    fp = validate_file_path(file_path)
    if not os.path.isdir(fp):
        raise argparse.ArgumentTypeError(f"'{file_path}' is not a directory!")
    return fp


def validate_regex(pattern):
    try:
        a = re.compile(pattern)
        return pattern
    except re.error as e:
        raise argparse.ArgumentTypeError(f"Invalid regular expression: {e}")
