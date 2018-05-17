#!/usr/bin/env python3
# encoding: utf-8
'''

Test the filter_csv function for xtandem engine

'''
import ursgal
import csv
import os


R = ursgal.UController()


TESTS = [
    {
        'csv_filter_rules' : [ ['Calc m/z','gte',1100],['Calc m/z','lte',1400]  ],
        'number_of_expected_lines': 4,
    },
    {
        'csv_filter_rules' : [ ['Modifications','contains','Carbamidomethyl'] ],
        'number_of_expected_lines': 9,
    },
    {
        'csv_filter_rules' : [ ['Modifications','contains_not','Carbamidomethyl'] ],
        'number_of_expected_lines': 1,
    },
    {
        'csv_filter_rules' : [ ['Retention Time (s)','gt',1793.82605] ], #last RT
        'number_of_expected_lines': 0,
    },
    {
        'csv_filter_rules' : [ ['Retention Time (s)','lt',1793.82605] ], #last RT
        'number_of_expected_lines': 9,
    },
    {
        'csv_filter_rules' : [ ['Sequence','contains','T'] ],
        'number_of_expected_lines': 4,
    },
    {
        'csv_filter_rules' : [ ['Is decoy','equals','FALSE'] ], # Excel style
        'number_of_expected_lines': 10,
    },
    {
        'csv_filter_rules' : [ ['Is decoy','equals','TRUE'] ], # Excel style
        'number_of_expected_lines': 0,
    },
    {
        'csv_filter_rules' : [
            ['Modifications','contains','Carbamidomethyl'],
            ['PEP','lte',7.121E-05]
        ],
        'number_of_expected_lines': 1,
    },
    {
        'csv_filter_rules' : [
            ['Modifications','regex','Carbamidomethyl\:2']
        ],
        'number_of_expected_lines': 6,
    },
    {
        'csv_filter_rules' : [
            ['Spectrum Title','regex','.25\d*.']
        ],
        'number_of_expected_lines': 8,
    },
    {
        'csv_filter_rules' : [
            ['Sequence','regex','C[T|D]']
        ],
        'number_of_expected_lines': 6,
    },
    {
        'csv_filter_rules' : [
            ['Modifications','contains_element_of_list',['Oxidation', 'Carbamidomethyl']]
        ],
        'number_of_expected_lines': 9,
    },
]


filter_csv_main = R.unodes['filter_csv_1_0_0']['class'].import_engine_as_python_function()

input_csv = os.path.join(
    'tests',
    'data',
    'test_BSA1_omssa_2_1_9_unified_filter_csv_test.csv'
)


def compare_filter_test():
    for test_id, test_dict in enumerate(TESTS):
        yield compare_filter, test_dict


def compare_filter( test_dict ):
    output_csv = filter_csv_main(
        input_file     = input_csv,
        output_file    = os.path.join(
            'tests',
            'data',
            'test_BSA1_omssa_2_1_9_unified_filter_csv_test_filtered.csv'
        ),
        filter_rules   = test_dict['csv_filter_rules'],
    )
    opened_output_csv = open(output_csv, 'r')
    counter = 0
    for line_dict in csv.DictReader(opened_output_csv):
        counter += 1
    opened_output_csv.close()
    assert counter == test_dict['number_of_expected_lines']

    os.remove(output_csv)


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        compare_filter(test_dict)
