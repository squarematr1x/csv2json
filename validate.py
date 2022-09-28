import os
import re

from typing import List


def valid_path(file_path: str) -> bool:
    return os.path.exists(file_path)


def valid_file_name(name: str) -> bool:
    allowed_name = re.compile('^[^<>:;,?"*|/]+$')
    return allowed_name.match(name)


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
    valid_name = valid_file_name(path)

    if '/' in path:
        path_tokens = path.rsplit('/', 1)
        if not valid_path(path_tokens[0]):
            print('Error: Invalid file path for output json file')
            return False

        valid_name = valid_file_name(path_tokens[1])

    if not valid_name:
        print('Error: Invalid file name')
        return False

    if not valid_file_extension(path, '.json'):
        print('Error: output file extension must be ".json"')
        return False

    return True


def valid_files(input_path: str, output_path: str) -> bool:
    return valid_input_file(input_path) and valid_output_file(output_path)


def valid_row_input(args: List[str]) -> bool:
    '''
    Validate input csv rows to be included in the output json.
    Strings such as "2 4 6", "7-11" and "3 6-8 12" are allowed.
    '''

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
