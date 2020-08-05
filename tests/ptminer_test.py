#!/usr/bin/env python3
# encoding: utf-8
'''

Test the ptminer postflight function

'''
import ursgal
import csv
import os

uc = ursgal.UController()

ptminer_wrapper = uc.unodes['ptminer_1_0']['_wrapper_class']

ursgal_input_csv = os.path.join(
    'tests',
    'data',
    'ptminer_1_0',
    'test_ptminer_1_0_ursgal_results.csv'
)

ptminer_input_csv = os.path.join(
    'tests',
    'data',
    'ptminer_1_0',
    'test_ptminer_1_0_annotated_results.txt'
)

output_csv = os.path.join(
    'tests',
    'data',
    'ptminer_1_0',
    'test_ptminer_1_0_merged_results.csv'
)

expected_output_csv = os.path.join(
    'tests',
    'data',
    'ptminer_1_0',
    'test_ptminer_1_0_expected_results.csv'
)

output_csv = ptminer_wrapper.postflight(
    None,
    anno_result=ptminer_input_csv,
    csv_input=ursgal_input_csv,
    merged_results_csv=output_csv
)

ptminer_line_dicts = []
for line_dict in csv.DictReader(open(output_csv, 'r')):
    ptminer_line_dicts.append(sorted(line_dict.items()))
sorted_ptminer_line_dicts = sorted(ptminer_line_dicts, key=lambda item: item[0])

expected_line_dicts = []
for line_dict in csv.DictReader(open(expected_output_csv, 'r')):
    expected_line_dicts.append(sorted(line_dict.items()))
sorted_expected_line_dicts = sorted(expected_line_dicts, key=lambda item: item[0])

def postflight_ptminer_test():
    for test_id, test_dict_items in enumerate(sorted_ptminer_line_dicts):
        expected_dict_items = sorted_expected_line_dicts[test_id]
        yield postflight_ptminer, test_dict_items, expected_dict_items

def postflight_ptminer(test_dict_items, expected_dict_items):
    for i, test_item in enumerate(test_dict_items):
        test_key, test_value = test_item
        expected_item = expected_dict_items[i]
        expected_key, expected_value = expected_item
        assert test_key == expected_key, '''
        test_key = {0}
        expected_key = {1}
        '''.format(test_key, expected_key)
        assert test_value == expected_value, '''
        column = {2}
        test_value = {0}
        expected_value = {1}
        '''.format(test_value, expected_value,test_key)

if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(sorted(ptminer_line_dicts)):
        expected_dict = sorted(expected_line_dicts)[test_id]
        postflight_ptminer(test_dict, expected_dict)