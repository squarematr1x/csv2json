import os
import time
import argparse
import csv
import json


def csv2json(csv_path, json_path, indent_size=4):
    json_arr = []

    with open(csv_path, encoding='utf-8-sig') as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=';,')
        csv_file.seek(0)
        csv_reader = csv.DictReader(csv_file, dialect=dialect)

        for row in csv_reader:
            json_arr.append(row)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_str = json.dumps(json_arr, indent=int(indent_size))
        json_str = json_str.replace('\\u00a0', '')
        json_file.write(json_str)


def valid_path(path):
    return os.path.exists(path)


def valid_file_extension(path, extension):
    return path[-len(extension):] == extension


def validate_input_file(path):
    if not valid_path(path):
        print('Error: Invalid file path for input csv file')
        quit()
    if not valid_file_extension(path, '.csv'):
        print('Error: Input file extension must be ".csv"')
        quit()


def validate_output_file(path):
    if not valid_file_extension(path, '.json'):
        print('Error: output file extension must be ".json"')
        quit()


def main():
    parser = argparse.ArgumentParser(description='Convert csv to json')

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
        '-i',
        '--indent',
        nargs=1,
        metavar='indent size',
        default=None,
        help='indent size of json file',
    )
    args = parser.parse_args()

    input_file = None
    output_file = None
    indent_size = 4

    if args.read != None:
        input_file = args.read[0]
    if args.write != None:
        output_file = args.write[0]
    if args.indent != None:
        indent_size = args.indent[0]

    validate_input_file(input_file)
    validate_output_file(output_file)

    start_t = time.time()
    csv2json(input_file, output_file, indent_size)
    end_t = time.time()
    print(f'Converted in time: {end_t - start_t}')


if __name__ == '__main__':
    main()
