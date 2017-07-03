#!/usr/bin/env python3
# encoding: utf-8
'''

Test the csv2ssl engine for unified file

'''
import ursgal
import csv
import os


R = ursgal.UController()

csv2ssl_main = R.unodes['csv2ssl_1_0_0']['class'].import_engine_as_python_function()
input_csv = os.path.join(
    'tests',
    'data',
    'csv2ssl_1_0_0',
    'BSA1_csv2ssl_test_unified.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'csv2ssl_1_0_0',
    'BSA1_csv2ssl_test_unified_converted.csv'
)
csv2ssl_main(
    input_file     = input_csv,
    output_file    = output_csv,
    score_column_name = 'MS-GF:EValue',
    score_type        = 'TANDEM EXPECTATION VALUE',
)

ident_list = [ ]
csv_in = csv.DictReader(open(input_csv, 'r'))
fieldnames = csv_in.fieldnames
for line_dict in csv_in:
    ident_list.append( line_dict )

out_list = [ ]
csv_out = csv.DictReader(open(output_csv, 'r'), delimiter='\t')
for line_dict in csv_out:
    out_list.append( line_dict )

def csv2ssl_test():
    for test_id, test_dict in enumerate(ident_list):
        yield csv2ssl, test_dict, test_id


def csv2ssl( test_dict, test_id ):
    assert os.path.isfile(output_csv)

    for key in fieldnames:
        if key.startswith('Expected'):
            expected_value = test_dict[key]
            test_value = out_list[test_id][key[9:]]
            print(test_value, expected_value)
            assert test_value == expected_value


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(ident_list):
        csv2ssl(test_dict, test_id)
