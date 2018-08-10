#!/usr/bin/env python3
# encoding: utf-8
'''

Test the unify_csv function for msamanda engine

'''
import ursgal
import csv
import pickle
import os

modifications = [
    'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
]

R = ursgal.UController(
    params = {
        'modifications' : modifications
    }    
)
R.map_mods()

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

unify_csv = R.unodes['unify_csv_2_0_0']['class'].import_engine_as_python_module()

input_csv = os.path.join(
    'tests',
    'data',
    'msamanda_1_0_0_5243',
    'test_BSA1_msamanda_1_0_0_5243.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'msamanda_1_0_0_5243',
    'test_BSA1_msamanda_1_0_0_5243_unified.csv'
)
unify_csv.main(
    input_file     = input_csv,
    output_file    = output_csv,
    scan_rt_lookup = scan_rt_lookup,
    params = {
        'translations': {
            'decoy_tag': 'decoy_',
            'enzyme' : 'KR;C;P',
            'semi_enzyme' : False,
            'database': os.path.join(
                'tests',
                'data',
                'BSA.fasta'
            ),
            'protein_delimiter' : '<|>',
            'psm_merge_delimiter' : ';',
            'keep_asp_pro_broken_peps':True,
            'precursor_mass_tolerance_minus': 5,
            'precursor_mass_tolerance_plus' : 5,
            'precursor_isotope_range' : "0,1",
            'max_missed_cleavages':2,
            'rounded_mass_decimals' : 3,
        },
        'label' : '',
        'mods' : R.params['mods'],
    },
    meta_info = {
        'search_engine'  : 'msamanda_1_0_0_5243',
        'score_colname' : None,
        'raw_data_location' : os.path.join(
            'tests',
            'data',
            'BSA1.mzML'
        ),
        'cross_link_search_engine'                : False,
        'de_novo_search_engine'                   : False,
        'protein_database_search_engine'          : True,
        'protein_database_open_mod_search_engine' : False,
        'spectral_library_search_engine'          : False,
    }
)

ident_list = [ ]
for line_dict in csv.DictReader(open(output_csv, 'r')):
    ident_list.append( line_dict )


def unify_msamanda_test():
    for test_id, test_dict in enumerate(ident_list):
        yield unify_msamanda, test_dict


def unify_msamanda( test_dict ):
    assert 'uCalc m/z' in test_dict.keys()
    assert test_dict['uCalc m/z'] == test_dict['Calc m/z']

    for key in [
            'Retention Time (s)',
            'Spectrum ID',
            'Modifications',
            'Spectrum Title',
            'Calc m/z',
            'Sequence',
        ]:
        test_value = test_dict[key]
        expected_value = test_dict['Expected {0}'.format(key)]
        if key in [ 'Retention Time (s)', 'Calc m/z' ]:
            test_value     = round(float(test_value), 4)
            expected_value = round(float(expected_value), 4)
        print(test_value, expected_value)
        assert test_value == expected_value


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(ident_list):
        unify_msamanda(test_dict)
