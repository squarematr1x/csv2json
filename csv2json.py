import time

import pandas as pd

from argparse import ArgumentParser
from typing import List, Dict, Optional

from validate import *


def csv2json(csv_path: str, json_path: str, indent: int = 4,
             rows: Optional[List[int]] = None, row_mode: Optional[str] = None,
             columns: Optional[List[str]] = None, column_mode: Optional[str] = None):
    """
    Converts input csv to json.

    """

    ALLOWED_ROW_MODES = [
        None,
        'include',
        'exclude',
        'head',
        'tail',
    ]

    ALLOWED_HEADER_MODES = [
        None,
        'include',
        'exclude',
    ]

    if row_mode not in ALLOWED_ROW_MODES:
        raise ValueError(f'Invalud mode. Expected one of: {ALLOWED_ROW_MODES}')

    if column_mode not in ALLOWED_HEADER_MODES:
        raise ValueError(f'Invalud mode. Expected one of: {ALLOWED_ROW_MODES}')

    df = pd.read_csv(csv_path, engine='python', sep=None)

    if row_mode == 'tail':
        df = df.tail()
    elif row_mode == 'head':
        df = df.head()
    elif row_mode == 'include':
        df = df.iloc[rows]
    elif row_mode == 'exclude':
        df.drop(rows, inplace=True)

    if column_mode == 'include':
        df = df[columns]
    elif column_mode == 'exclude':
        df.drop(columns=columns, inplace=True)

    json_str = df.to_json(orient='records', indent=indent)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def get_row_numbers(arg: str) -> Dict[int, bool]:
    """
    Get user defined input row numbers.
    """

    input_numbers = arg.split('-')
    rows = []

    if len(input_numbers) == 1:
        rows.append(int(input_numbers[0]))
    else:
        range_start, range_end = int(input_numbers[0]), int(input_numbers[1])

        if range_start >= range_end:
            error = 'Error: starting index must be smaller than ending index in number ranges'
            print(error)
            quit()

        for i in range(range_start, range_end + 1):
            rows.append(i)

    return rows


def parse_row_numbers(args: List[str]) -> List[int]:
    """
    Get user defined row numbers.
    Rows can be defined as integers or ranges.
    Example:    --rows 0 2-4 8
                returns a list of integers [0, 2, 3, 4, 8]      
    """
    rows = []

    for arg in args:
        rows += get_row_numbers(arg)

    return rows


def add_arguments(parser: ArgumentParser):
    parser.add_argument(
        '-c',
        '--convert',
        nargs=2,
        metavar=['csv file name', 'json file name'],
        required=True,
        help=' convert csv file to json',
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
        help='returns first 5 rows of input as json'
    )
    parser.add_argument(
        '--tail',
        action='store_true',
        help='returns last 5 rows of input as json'
    )


def main():
    parser = ArgumentParser(description='Convert csv to json')
    add_arguments(parser)
    args = parser.parse_args()

    input_file = None
    output_file = None
    valid_input = True
    indent = 4
    rows = []
    row_mode = None
    invalid_rows = False
    columns = None
    column_mode = None
    invalid_columns = False

    if args.convert:
        input_file = args.convert[0]
        output_file = args.convert[1]
    if args.indent:
        indent = args.indent[0]
    if args.rows:
        row_mode = 'include'
        valid_input = valid_row_input(args.rows)
        rows = parse_row_numbers(args.rows)
    if args.xrows:
        if row_mode:
            invalid_rows = True
        if not invalid_rows:
            row_mode = 'exclude'
            rows = parse_row_numbers(args.xrows)
    if args.columns:
        column_mode = 'include'
        columns = args.columns
    if args.xcolumns:
        if column_mode:
            invalid_columns = True
        if not invalid_columns:
            column_mode = 'exclude'
            columns = args.xcolumns
    if args.head:
        if row_mode:
            invalid_rows = True
        if not invalid_rows:
            row_mode = 'head'
    if args.tail:
        if row_mode:
            invalid_rows = True
        if not invalid_rows:
            row_mode = 'tail'

    if invalid_rows:
        print("Error: you cannot include and exclude rows at the same time")
        quit()

    if invalid_columns:
        print("Error: you cannot include and exclude columns at the same time")
        quit()

    valid_input = valid_files(input_file, output_file)

    if not valid_input:
        quit()

    start_t = time.time()
    csv2json(input_file, output_file, indent, rows, row_mode,
             columns, column_mode)
    end_t = time.time()
    print(f'Converted in time: {end_t - start_t}')


if __name__ == '__main__':
    main()
