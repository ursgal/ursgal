#!/usr/bin/env python3
# encoding: utf-8
'''

Test the unify_csv function for omssa engine

'''
import ursgal
import csv
import pickle
import os

uc = ursgal.UController(
    profile = 'LTQ XL low res',
    force  = False
)

upeptide_mapper_main = uc.unodes['upeptide_mapper_1_0_0']['class'].import_engine_as_python_function(
    'main'
)

input_csv = os.path.join(
    'tests',
    'data',
    'test_upeptide_mapper.csv'
)
output_csv = os.path.join(
    'tests',
    'data',
    'test_upeptide_mapper_pmap.csv'
)

params = {
    'translations' : {
        'modifications' : [
            'M,opt,any,Oxidation',        # Met oxidation
            'C,fix,any,Carbamidomethyl',  # Carbamidomethylation
            '*,opt,Prot-N-term,Acetyl',    # N-Acteylation[]
        ],
        'aa_exception_dict' : {
            'J' : {
                'original_aa' : ['I', 'L'],
            },
            'O' : {
                'original_aa' : ['K'],
                'unimod_name' : 'Methylpyrroline',
            },
        },
        'protein_delimiter'        : '<|>',
        'decoy_tag'                : 'decoy_',
        'word_len'                 : 6,
        'database' : os.path.join(
            'tests',
            'data',
            'BSA.fasta'
        ),
    },
    'prefix' : None
}

all_mapped_peptides = set()
ident_list = [ ]
for peptide_mapper_class_version in [ 'UPeptideMapper_v3', 'UPeptideMapper_v4' ]:
    params['translations']['peptide_mapper_class_version'] = peptide_mapper_class_version
    upeptide_mapper_main(
        input_file     = input_csv,
        output_file    = output_csv,
        params         = params,
    )

    for line_dict in csv.DictReader(open(output_csv, 'r')):
        ident_list.append( line_dict )
        all_mapped_peptides.add(line_dict['Sequence'])

def upeptide_mapper_test():
    for test_id, test_dict in enumerate(ident_list):
        yield upeptide_mapper, test_dict


def upeptide_mapper( test_dict ):
    for key in [
            'Sequence',
            'Modifications',
            'Is decoy',
            'Protein ID',
            'Sequence Start',
            'Sequence Stop',
            'Sequence Pre AA',
            'Sequence Post AA',
        ]:
        test_value = test_dict[key]
        expected_value = test_dict[ 'Expected {0}'.format(key) ]
        assert test_value == expected_value, '''
Unexpected value in column "{0}":
    test value:     {1}
    expected value: {2}
            '''.format(key, test_value, expected_value)

def non_map_test():
    ''' 
    LERAA would be an overlap of ProtD and ProtE and should not be mapped.
    '''
    assert 'LERAAA' not in all_mapped_peptides

if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(ident_list):
        upeptide_mapper(test_dict)
