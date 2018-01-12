#!/usr/bin/env python3
# encoding: utf-8
'''

Test the xtandem2csv function

'''
import ursgal
import csv
import pickle
import os


R = ursgal.UController(
    profile = 'LTQ XL low res',
    params  = {
        'database': os.path.join( 'data', 'BSA.fasta')
    },
    force   = False
)

xtandem2csv_main = R.unodes['xtandem2csv_1_0_0']['class'].import_engine_as_python_function()
input_xml = os.path.join(
    'tests',
    'data',
    'xtandem_sledgehammer',
    'test_BSA1_xtandem.xml'
)
output_csv = os.path.join(
    'tests',
    'data',
    'xtandem_sledgehammer',
    'test_BSA1_xtandem.csv'
)
expected_csv = os.path.join(
    'tests',
    'data',
    'xtandem_sledgehammer',
    'test_BSA1_xtandem_expected.csv'
)
xtandem2csv_main(
    input_file     = input_xml,
    output_file    = output_csv,
    decoy_tag = 'decoy_',
)

ident_list = [ ]
for line_dict in csv.DictReader(open(output_csv, 'r')):
    ident_list.append( line_dict )
expected_list = []
for line_dict in csv.DictReader(open(expected_csv, 'r')):
    expected_list.append( line_dict )
# print(ident_list)

def unify_xtandem_test():
    for test_id, expected_dict in enumerate(expected_list):
        test_dict = ident_list[test_id]
        yield unify_xtandem, test_dict, expected_dict


def unify_xtandem( test_dict, expected_dict ):
    for key in [
        'Raw data location',
        'Spectrum ID',
        'Spectrum Title',
        'Retention Time (s)',
        'Rank',
        'Calc m/z',
        'Exp m/z',
        'Charge',
        'Sequence',
        'Modifications',
        'X\!Tandem:expect',
        'X\!Tandem:hyperscore',
        'proteinacc_start_stop_pre_post_;',
        'Is decoy',
        ]:
        test_value = test_dict[key]
        expected_value = expected_dict[key]
        assert test_value == expected_value, print(
            test_value,
            expected_value
        )

if __name__ == '__main__':
    print(__doc__)
    for test_id, expected_dict in enumerate(expected_list):
        test_dict = ident_list[test_id]
        unify_xtandem(test_dict, expected_dict)

