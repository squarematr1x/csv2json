import os
import time
import csv
import json

from argparse import ArgumentParser
from typing import List, Dict, Optional


def include_row(rows: Dict[int, bool], index: int, mode: str) -> bool:
    if index in rows:
        return rows[index]

    if mode == 'include':
        return False
    elif mode == 'exclude':
        return True


def csv2json(csv_path: str, json_path: str, indent_size: int = 4, rows: Optional[Dict[int, bool]] = None, mode: Optional[str] = None):
    """
    Converts input csv to json.

    """
    ALLOWED_MODES = [
        None,
        'include',
        'exclude',
    ]

    if mode not in ALLOWED_MODES:
        raise ValueError(f'Invalud mode. Expected one of: {ALLOWED_MODES}')

    json_arr = []

    with open(csv_path, encoding='utf-8-sig') as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=';,')
        csv_file.seek(0)
        csv_reader = csv.DictReader(csv_file, dialect=dialect)

        for index, row in enumerate(csv_reader):
            if include_row(rows, index, mode):
                json_arr.append(row)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_str = json.dumps(json_arr, indent=int(indent_size))
        # Remove non-breaking spaces
        json_str = json_str.replace('\\u00a0', '')
        json_file.write(json_str)


def valid_path(path: str) -> bool:
    return os.path.exists(path)


def valid_file_extension(path: str, extension: str) -> bool:
    return path[-len(extension):] == extension


def validate_input_file(path: str):
    if not valid_path(path):
        print('Error: Invalid file path for input csv file')
        quit()
    if not valid_file_extension(path, '.csv'):
        print('Error: Input file extension must be ".csv"')
        quit()


def validate_output_file(path: str):
    if not valid_file_extension(path, '.json'):
        print('Error: output file extension must be ".json"')
        quit()


def parse_row_numbers(args: List[str], mode: str) -> Dict[int, bool]:
    rows = {}

    for arg in args:
        # TODO: Only allow positive integers (8, 1, 55) and ranges (1-5)
        if mode == 'include':
            rows[int(arg)] = True
        elif mode == 'exculde':
            rows[int(args)] = False

    return rows


def add_arguments(parser: ArgumentParser):
    parser.add_argument(
        '-r',
        '--read',
        nargs=1,
        metavar='csv file name',
        default=None,
        required=True,
        help='csv file that needs to be converted to json',
    )
    parser.add_argument(
        '-w',
        '--write',
        nargs=1,
        metavar='json file name',
        default=None,
        required=True,
        help='name of the resulting json file',
    )
    parser.add_argument(
        '--indent',
        nargs=1,
        metavar='indent size',
        default=None,
        help='number of indent spaces in json file',
    )
    parser.add_argument(
        '--rows',
        nargs='*',
        metavar='rows that are included in output json',
        default=None,
        help='rows that are included in output json e.g. 1 3 8, 2-6 or 2-6 9 11-12',
    )


def main():
    parser = ArgumentParser(description='Convert csv to json')
    add_arguments(parser)
    args = parser.parse_args()

    input_file = None
    output_file = None
    indent_size = 4
    rows = {}
    mode = None

    if args.read != None:
        input_file = args.read[0]
    if args.write != None:
        output_file = args.write[0]
    if args.indent != None:
        indent_size = args.indent[0]
    if args.rows != None:
        mode = 'include'
        rows = parse_row_numbers(args.rows, mode)

    validate_input_file(input_file)
    validate_output_file(output_file)

    start_t = time.time()
    csv2json(input_file, output_file, indent_size, rows, mode)
    end_t = time.time()
    print(f'Converted in time: {end_t - start_t}')


if __name__ == '__main__':
    main()
