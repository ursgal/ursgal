#!/usr/bin/env python3
# encoding: utf-8
'''

Test the unify_csv function for msgfplus engine

'''
import ursgal
import csv
import pickle
import os


modifications = [
    'M,opt,any,Oxidation',        # Met oxidation
    'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
    '*,opt,Prot-N-term,Acetyl'    # N-Acteylation
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

unify_csv_main = R.unodes['unify_csv_1_0_0']['class'].import_engine_as_python_function()
input_csv = os.path.join(
    'tests',
    'data',
    'novor_1_1beta',
    'test_BSA1_novor_1_1beta.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'novor_1_1beta',
    'test_BSA1_novor_1_1beta_unified.csv'
)
unify_csv_main(
    input_file     = input_csv,
    output_file    = output_csv,
    scan_rt_lookup = scan_rt_lookup,
    params = {
        'translations' : {
            'aa_exception_dict' : {
                'U' : {
                    'unimod_name' : 'Delta:S(-1)Se(1)',
                    'original_aa' : 'C',
                    'unimod_name_with_cam': 'SecCarbamidomethyl',
                },
            },
            'enzyme' : 'KR;C;P',
            'semi_enzyme' : False,
            'protein_delimiter' : '<|>',
            'precursor_mass_tolerance_minus': 5,
            'precursor_mass_tolerance_plus' : 5,
            'precursor_isotope_range' : "0,1",
            'rounded_mass_decimals' : 3,
            'use_pyqms_for_mz_calculation' : False
        },
        'label' : '',
        'mods' : R.params['mods'],
    },
    search_engine  = 'novor_1_1beta',
)

ident_list = [ ]
for line_dict in csv.DictReader(open(output_csv, 'r')):
    ident_list.append( line_dict )


def unify_novor_test():
    for test_id, test_dict in enumerate(ident_list):
        yield unify_novor, test_dict


def unify_novor( test_dict ):
    assert 'uCalc m/z' in test_dict.keys()

    for key in [
            'Retention Time (s)',
            'Spectrum ID',
            'Charge',
            'Modifications',
            'Spectrum Title',
            'Sequence'
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
        unify_novor(test_dict)
