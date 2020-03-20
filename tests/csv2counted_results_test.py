#!/usr/bin/env python
# encoding: utf-8
'''

Test the csv2counted_results engine for unified file

'''
import ursgal
import csv
import os


R = ursgal.UController()

csv2counted_results_main = R.unodes['csv2counted_results_1_0_0']['class'].import_engine_as_python_function()
input_csv = os.path.join(
    'tests',
    'data',
    'csv2counted_results_1_0_0',
    'csv2counted_results_test.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'csv2counted_results_1_0_0',
    'csv2counted_results_test_counted.csv'
)
csv2counted_results_main(
    input_file     = input_csv,
    output_file    = output_csv,
    identifier_colum_names = ['Protein ID', 'Charge'],
    count_column_names = ['Sequence', 'Modifications'],
    count_by_file = True,
)

correct_values_dict = {
    'ProteinA#3' : {
        'test' : '3',
        'test2' : '0',
    },
    'ProteinA#2' : {
        'test' : '1',
        'test2' : '0',
    },
    'ProteinC#3' : {
        'test' : '1',
        'test2' : '0',
    },
    'ProteinC#2' : {
        'test' : '2',
        'test2' : '0',
    },
    'ProteinD#2' : {
        'test' : '0',
        'test2' : '1',
    },
    'ProteinD#1' : {
        'test' : '0',
        'test2' : '1',
    },
}

test_dict = {}
csv_out = csv.DictReader(open(output_csv, 'r'))
for line_dict in csv_out:
    test_dict[
        '#'.join([
            line_dict['Protein ID'],
            line_dict['Charge']
        ])
    ] = {
        'test' : line_dict['test'],
        'test2' : line_dict['test2'],
    }

def csv2counted_results_test():
    for test_id, test_key in enumerate(correct_values_dict.keys()):
        yield csv2counted_results, test_key, test_dict


def csv2counted_results( test_key, test_dict ):
    assert os.path.isfile(output_csv)

    print(test_key, correct_values_dict[test_key], test_dict[test_key])
    assert correct_values_dict[test_key] == test_dict[test_key]


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_key in enumerate(correct_values_dict.keys()):
        csv2counted_results(test_key, test_dict)
