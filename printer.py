"""
Purpose: Wrappers for various CLI use cases
Author: Michael K. Steinberg
Created: 23/04/2024
Name: printer.py
"""

import subprocess

import tqdm
from colorama import Fore, Style

from .settings import get_delimiter, is_verbose_mode, use_tqdm


class ExternalProcedureException(Exception):
    """
    Exception raised when an external procedure returns a non-zero code.
    """

    pass


def write(s, **kwargs):
    """
    Writes a string to the console.

    Args:
        s (str): The string to write.
        **kwargs: Arbitrary keyword arguments.
    """
    print_function = tqdm.tqdm.write if use_tqdm() else print
    print_function(s, **kwargs)


def _concat_arguments(s, *args) -> str:
    """
    Concatenates arguments with a delimiter.

    Args:
        s (str): The initial string.
        *args: Variable length argument list.

    Returns:
        str: The concatenated string.
    """
    return f"{get_delimiter()}".join(str(x) for x in (s, *args))


def print_info(s, *args, **kwargs):
    """
    Prints an info message.

    Args:
        s (str): The initial string.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    write("[~] " + _concat_arguments(s, *args), **kwargs)


def print_log(s, *args, **kwargs):
    """
    Prints a log message if verbose mode is enabled.

    Args:
        s (str): The initial string.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    if not is_verbose_mode():
        return
    write(
        Style.DIM + "[=] " + _concat_arguments(s, *args) + Style.RESET_ALL,
        **kwargs,
    )


def print_success(s, *args, **kwargs):
    """
    Prints a success message.

    Args:
        s (str): The initial string.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    write(Fore.CYAN + "[+] " + _concat_arguments(s, *args) + Style.RESET_ALL, **kwargs)


def print_error(s, *args, **kwargs):
    """
    Prints an error message.

    Args:
        s (str): The initial string.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    write(Fore.RED + "[!] " + _concat_arguments(s, *args) + Style.RESET_ALL, **kwargs)


def run_proc(params, *args, **kwargs) -> subprocess.CompletedProcess[str]:
    """
    Executes a subprocess with the given parameters and arguments.

    This function runs a subprocess with the provided parameters and optional arguments.
    If the verbose mode is enabled, it prints the command line string.
    It captures the output of the subprocess by default.
    If the subprocess returns a non-zero code, it raises an ExternalProcedureException.

    Args:
        params (list): The list of parameters to pass to the subprocess.
        *args: Variable length argument list to pass to the subprocess.
        **kwargs: Arbitrary keyword arguments to pass to the subprocess.

    Returns:
        subprocess.CompletedProcess: The completed process object.

    Raises:
        ExternalProcedureException: If the subprocess returns a non-zero code.
    """
    if is_verbose_mode():
        cmd_line_str = subprocess.list2cmdline(params)
        write(Style.DIM + "> " + cmd_line_str + Style.RESET_ALL)
    if "capture_output" not in kwargs:
        kwargs["capture_output"] = True
    proc = subprocess.run(params, *args, **kwargs)
    if proc.returncode != 0:
        raise ExternalProcedureException(
            f"External procedure returned {proc.returncode}"
        )
    return proc
