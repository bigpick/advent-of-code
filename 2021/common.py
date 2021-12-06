#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from os.path import exists


def valid_file(file_path: str) -> str:
    """Check whether a given path is an existent file.

    If not, raises and ArgumentTypeError, as the intended purpose of
    this helper utility is a type for an argparse argument.

    Args:
        file_path (str): The path to the file to check exists.
    """
    if not exists(file_path):
        raise ArgumentTypeError(f"{file_path} does not exist")
    return file_path


def chall_file_parser(parser: ArgumentParser) -> ArgumentParser:
    """Configure CLI parser for a single named filepath argument.

    Will raise "ArgumentTypeError" if the specified value for the named file argument does not
    exist on the local filesystem/is not accessible.

    Args:
        parser (ArgumentParser): The argument parser to configure.
    """
    parser.add_argument(
        "--chall-input",
        dest="chall_input",
        metavar="FILE",
        type=valid_file,
        required=True,
    )
    return parser


def parse_single_named_file_cli() -> Namespace:
    """Configure and parse a single named file argument from the CLI."""
    return chall_file_parser(ArgumentParser()).parse_args()


def parse_file(fpath: str) -> str:
    """Parse and return a filepath's contents.

    Args:
        fpath (str): The path to the file to parse.

    Returns:
        str: The filepath's contents.
    """
    with open(fpath, "r") as infile:
        return infile.read()
