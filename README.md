# PyPrinter Module

## Description

PyPrinter is a Python module designed to provide a set of utilities for printing messages in different formats and colors. It also includes a function to run subprocesses and handle their output.

## Features

- **Verbose Mode**: PyPrinter can operate in a verbose mode, printing additional log messages.
- **Color Support**: PyPrinter uses the colorama library to print messages in different colors.
- **Progress Bar Support**: PyPrinter can use tqdm to display progress bars.
- **Subprocess Support**: PyPrinter can run subprocesses and capture their output.

## Installation

To install the PyPrinter module, you can clone the repository and import it into your Python project.

## Usage

Here's a basic usage example:

```python
from PyPrinter import print_success, print_error, run_proc

print_success("This is a success message.")
print_error("This is an error message.")
run_proc(["ls", "-l"])
