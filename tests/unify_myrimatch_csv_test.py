#!/usr/bin/env python3.4
# encoding: utf-8
'''

Test the unify_csv function for myrimatch engine

'''
import ursgal
import csv
import pickle
import os


R = ursgal.UController()

scan_rt_lookup = pickle.load(
    open(
        os.path.join(
            'tests',
            'data',
            '_test_ursgal_lookup.pkl')
        ,
        'rb'
    )
)

unify_csv_main = R.unodes['unify_csv_1_0_0']['class'].import_engine_as_python_function()
input_csv = os.path.join(
    'tests',
    'data',
    'myrimatch_2_1_138',
    'test_BSA1_myrimatch_2_1_138.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'myrimatch_2_1_138',
    'test_BSA1_myrimatch_2_1_138_unified.csv'
)
unify_csv_main(
    input_file     = input_csv,
    output_file    = output_csv,
    scan_rt_lookup = scan_rt_lookup,
    params = {
        'aa_exception_dict' : {
            'U' : {
                'unimod_name' : 'Delta:S(-1)Se(1)',
                'original_aa' : 'C',
                'unimod_name_with_cam': 'SecCarbamidomethyl',
            },
        },
        'modifications' : [
            'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
        ],
        'label' : '15N',
        'decoy_tag': 'decoy_',
    },
    search_engine  = 'myrimatch_2_1_138',
)
# exit()
ident_list = [ ]
for line_dict in csv.DictReader(open(output_csv, 'r')):
    ident_list.append( line_dict )



def unify_myrimtach_test():
    for test_id, test_dict in enumerate(ident_list):
        yield unify_myrimtach, test_dict


def unify_myrimtach( test_dict ):
    assert 'uCalc m/z' in test_dict.keys()
    assert 'scan=' not in test_dict['Spectrum ID']

    for key in [
            'Retention Time (s)',
            'Spectrum ID',
            'Modifications',
            'Spectrum Title'
        ]:
        test_value = test_dict[key]
        expected_value = test_dict['Expected {0}'.format(key)]
        if key == 'Retention Time (s)':
            test_value     = round(float(test_value), 4)
            expected_value = round(float(expected_value), 4)

        assert test_value == expected_value


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(ident_list):
        unify_myrimtach(test_dict)

