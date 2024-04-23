"""
Purpose: Settings for PyPrinter
Author: Michael K. Steinberg
Created: 23/04/2024
Name: settings.py
"""


class PyPrinterSettings:
    """
    Class to hold settings for PyPrinter.
    """

    verbose: bool = False
    use_tqdm: bool = True
    delimiter: str = " "


# Hack to make this a pointer
gs_settings = [PyPrinterSettings()]


def get_settings() -> PyPrinterSettings:
    """
    Returns the current settings.

    Returns:
        PyPrinterSettings: The current settings.
    """
    return gs_settings[0]


def is_verbose_mode() -> bool:
    """
    Checks if verbose mode is enabled.

    Returns:
        bool: True if verbose mode is enabled, False otherwise.
    """
    return get_settings().verbose


def set_verbose_mode(new_value: bool = True):
    """
    Sets the verbose mode.

    Args:
        new_value (bool, optional): The new value for verbose mode. Defaults to True.
    """
    get_settings().verbose = new_value


def use_tqdm() -> bool:
    """
    Checks if tqdm is used.

    Returns:
        bool: True if tqdm is used, False otherwise.
    """
    return get_settings().use_tqdm


def get_delimiter() -> str:
    """
    Gets the delimiter.

    Returns:
        str: The delimiter.
    """
    return get_settings().delimiter
