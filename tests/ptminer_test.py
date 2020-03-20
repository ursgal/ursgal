#!/usr/bin/env python3
# encoding: utf-8
'''

Test the ptminer postflight function

'''
import ursgal
import csv
import os

uc = ursgal.UController()

ptminer_wrapper = uc.unodes['ptminer_1_0']['_wrapper_class']()

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
    'test_ptminer_1_0_annotated_results.csv'
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
    anno_result=ptminer_input_csv, 
    csv_input=ursgal_input_csv,
    merged_results_csv=output_csv
    )

# ident_list = [ ]
# for line_dict in csv.DictReader(open(output_csv, 'r')):
#     ident_list.append( line_dict )
#check if the two files are the same
content_file1 = None
content_file2 = None
with open(output_csv, 'r') as file1, open(expected_output_csv, 'r') as file2:
    content_file1 = file1.readlines()
    content_file2 = file2.readlines()

def postflight_ptminer_test():
    for line in content_file2:
        yield postflight_ptminer, line, content_file1
    for line in content_file1:
        yield postflight_ptminer, line, content_file2

def postflight_ptminer(line, content_file):
    assert line in content_file

if __name__ == '__main__':
    print(__doc__)
    for line in content_file2:
        postflight_ptminer(line, content_file1)
    for line in content_file1:
        postflight_ptminer(line, content_file2)

