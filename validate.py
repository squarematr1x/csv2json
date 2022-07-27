import os
import re

from typing import List


def valid_path(path: str) -> bool:
    return os.path.exists(path)


def valid_file_extension(path: str, extension: str) -> bool:
    return path[-len(extension):] == extension


def valid_input_file(path: str) -> bool:
    if not valid_path(path):
        print('Error: Invalid file path for input csv file')
        return False

    if not valid_file_extension(path, '.csv'):
        print('Error: Input file extension must be ".csv"')
        return False

    return True


def valid_output_file(path: str) -> bool:
    if not valid_file_extension(path, '.json'):
        print('Error: output file extension must be ".json"')
        return False

    return True


def valid_row_input(args: List[str]) -> bool:
    """
    Validate input csv rows to be included in the output json.
    Strings such as "2 4 6", "7-11" and "3 6-8 12" are allowed.
    """

    allowed_str = re.compile('^[0-9]+$|^[0-9]+-[0-9]+$')
    allowed_input = True

    for arg in args:
        if not allowed_str.match(arg):
            allowed_input = False
            break

    if not allowed_input:
        print('Error: row input must a set of numbers "1 4 5", range "1-5"')
        return False

    return True
