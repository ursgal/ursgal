#!/usr/bin/env python3
# encoding: utf-8
'''

Test the unify_csv function for xtandem engine

'''
import ursgal
import csv
import pickle
import os

psm_defining_colnames = [
    'Spectrum Title',
    'Sequence',
    'Modifications',
    'Mass difference',
    'Charge',
    'Is decoy',
]

input_csv = os.path.join(
    'tests',
    'data',
    'test_merge_duplicate_rows.csv'
)
# output_csv = os.path.join(
#     'tests',
#     'data',
#     'test_merge_duplicate_rows_merged_duplicates.csv'
# )
expected_csv = os.path.join(
    'tests',
    'data',
    'test_merge_duplicate_rows_expected.csv'
)

psm_counter = ursgal.ucore.count_distinct_psms(
    csv_file_path=input_csv,
    psm_defining_colnames=psm_defining_colnames
)

results = ursgal.ucore.merge_duplicate_psm_rows(
    csv_file_path=input_csv,
    psm_counter=psm_counter,
    joinchar=';',
    psm_defining_colnames=psm_defining_colnames,
    overwrite_file=False,
)

merge_line_dicts = []
for line_dict in csv.DictReader(open(results, 'r')):
    merge_line_dicts.append(sorted(line_dict.items()))
sorted_merge_line_dicts = sorted(merge_line_dicts)

expected_line_dicts = []
for line_dict in csv.DictReader(open(expected_csv, 'r')):
    expected_line_dicts.append(sorted(line_dict.items()))
sorted_expected_line_dicts = sorted(expected_line_dicts)

def merge_duplicate_rows_test():
    assert max(psm_counter.values()) > 1, '''
    count_distinct_psms is incorrect:
    No entries > 1
    '''
    for test_id, test_dict_items in enumerate(sorted_merge_line_dicts):
        expected_dict_items = sorted_expected_line_dicts[test_id]
        yield merge_rows, test_dict_items, expected_dict_items


def merge_rows(test_dict_items, expected_dict_items):
    for i, test_item in enumerate(test_dict_items):
        test_key, test_value = test_item
        expected_item = expected_dict_items[i]
        expected_key, expected_value = expected_item
        assert test_key == expected_key, '''
        test_key = {0}
        expected_key = {1}
        '''.format(test_key, expected_key)
        assert test_value == expected_value, '''
        test_value = {0}
        expected_value = {1}
        '''.format(test_value, expected_value)


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(sorted(merge_line_dicts)):
        expected_dict = sprted(expcted_line_dicts)[test_id]
        merge_rows(test_dict, expected_dict)
