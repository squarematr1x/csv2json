import unittest

import json

from csv2json import csv2json

CSV_PATH = 'test/files/test.csv'
CSV_PATH_COMMA = 'test/files/test_comma.csv'
CSV_EMPTY = 'test/files/empty.csv'


def json_str_from_file(path: str) -> str:
    with open(path, 'r') as expected_result_file:
        expected_result = json.load(expected_result_file)

    return json.dumps(expected_result, indent=4)


class TestCsv2Json(unittest.TestCase):
    def test_conversion_semicolon_delimiter(self):
        json_str = csv2json(CSV_PATH)
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file('test/files/basic.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_comma_delimiter(self):
        json_str = csv2json(CSV_PATH_COMMA)
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file('test/files/basic.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_include_single_row(self):
        json_str = csv2json(CSV_PATH, rows=[3], row_mode='include')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/include_single_row.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_include_several_rows(self):
        rows = [0, 1, 2, 7, 8]
        json_str = csv2json(CSV_PATH, rows=rows, row_mode='include')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/include_several_rows.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_exclude_single_row(self):
        json_str = csv2json(CSV_PATH, rows=[6], row_mode='exclude')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/exclude_single_row.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_exclude_several_rows(self):
        rows = [1, 2, 8, 9]
        json_str = csv2json(CSV_PATH, rows=rows, row_mode='exclude')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/exclude_several_rows.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_tail(self):
        json_str = csv2json(CSV_PATH, row_mode='tail')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file('test/files/tail.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_head(self):
        json_str = csv2json(CSV_PATH, row_mode='head')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file('test/files/head.json')

        self.assertEqual(json_str, expected_result)

    def test_coversion_include_single_column(self):
        json_str = csv2json(CSV_PATH, columns=['Name'], column_mode='include')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/include_single_column.json')

        self.assertEqual(json_str, expected_result)

    def test_coversion_include_several_columns(self):
        columns = ['Id', 'Name', 'Job']
        json_str = csv2json(CSV_PATH, columns=columns, column_mode='include')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/include_several_columns.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_exclude_single_column(self):
        json_str = csv2json(CSV_PATH, columns=[
                            'Country'], column_mode='exclude')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/exclude_single_column.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_exclude_several_columns(self):
        columns = ['Name', 'Age', 'Job']
        json_str = csv2json(CSV_PATH, columns=columns, column_mode='exclude')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/exclude_several_columns.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_multiple_options(self):
        # Include rows 3,4 and 6
        rows = [3, 4, 6]
        # Exclude columns Id
        columns = ['Id']

        json_str = csv2json(CSV_PATH, rows=rows, row_mode='include',
                            columns=columns, column_mode='exclude')
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file(
            'test/files/multiple_options.json')

        self.assertEqual(json_str, expected_result)

    def test_conversion_only_headers(self):
        json_str = csv2json(CSV_EMPTY)
        json_str = json.dumps(json.loads(json_str), indent=4)
        expected_result = json_str_from_file('test/files/empty.json')

        self.assertEqual(json_str, expected_result)


if __name__ == '__main__':
    unittest.main()
