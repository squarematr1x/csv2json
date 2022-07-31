import time
import csv
import json

from argparse import ArgumentParser
from typing import List, Dict, Optional

from validate import *


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
            if not rows:
                json_arr.append(row)
            else:
                if include_row(rows, index, mode):
                    json_arr.append(row)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_str = json.dumps(json_arr, indent=int(indent_size))
        # Remove non-breaking spaces
        json_str = json_str.replace('\\u00a0', '')
        json_file.write(json_str)


def parse_row_numbers(args: List[str], mode: str) -> Dict[int, bool]:
    rows = {}

    for arg in args:
        if mode == 'include':
            rows[int(arg)] = True
        elif mode == 'exclude':
            rows[int(arg)] = False

    return rows


def add_arguments(parser: ArgumentParser):
    parser.add_argument(
        '-r',
        '--read',
        nargs=1,
        metavar='csv file name',
        required=True,
        help='csv file that needs to be converted to json',
    )
    parser.add_argument(
        '-w',
        '--write',
        nargs=1,
        metavar='json file name',
        required=True,
        help='name of the resulting json file',
    )
    parser.add_argument(
        '--indent',
        nargs=1,
        metavar='indent size',
        help='number of indent spaces in json file',
    )
    parser.add_argument(
        '--rows',
        nargs='*',
        metavar='rows that are included in output json',
        help='rows that are included in output json e.g. 1 3 8, 2-6 or 2-6 9 11-12',
    )
    parser.add_argument(
        '--xrows',
        nargs='*',
        metavar='rows that are excluded from output json',
        help='rows that are excluded from output json e.g. 1 3 8, 2-6 or 2-6 9 11-12',
    )
    parser.add_argument(
        '--columns',
        nargs='*',
        metavar='columns that are included in output json',
        help='names of the columns that should be included in output'
    )
    parser.add_argument(
        '--xcolumns',
        nargs='*',
        metavar='columns that should be excluded from output json',
        help='names of the columns that should be excluded from output json'
    )
    parser.add_argument(
        '--head',
        action='store_true',
        # If arr len < 5 return just arr otherwise 0:4
        help='returns first 5 rows of input as json'
    )
    parser.add_argument(
        '--tail',
        action='store_true',
        # If arr len < 5 return just arr otherwise -5:-1
        help='returns last 5 rows of input as json'
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
    invalid_rows = False
    valid_input = True

    if args.read:
        input_file = args.read[0]
    if args.write:
        output_file = args.write[0]
    if args.indent:
        indent_size = args.indent[0]
    if args.rows:
        mode = 'include'
        valid_input = valid_row_input(args.rows)
        rows = parse_row_numbers(args.rows, mode)
    if args.xrows:
        if mode:
            invalid_rows = True
        mode = 'exclude'
        rows = parse_row_numbers(args.xrows, mode)
    if args.columns:
        pass
    if args.xcolumns:
        pass
    if args.head:
        pass
    if args.tail:
        pass

    if invalid_rows:
        print("Error: you cannot include and exclude rows at the same time")
        quit()

    valid_input = valid_files(input_file, output_file)

    if not valid_input:
        quit()

    start_t = time.time()
    csv2json(input_file, output_file, indent_size, rows, mode)
    end_t = time.time()
    print(f'Converted in time: {end_t - start_t}')


if __name__ == '__main__':
    main()
