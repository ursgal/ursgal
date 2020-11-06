#!/usr/bin/env python3
# encoding: utf-8
'''

Test the ucore.digest function

Rules:
'enzyme' : {
    'argc' :            ('R', 'C'),
    'aspn' :            ('D', 'N'),
    'chymotrypsin' :    ('FMWY', 'C'),
    'chymotrypsin_p' :  ('FMWY', 'C'),
    'clostripain' :     ('R', 'C'),
    'cnbr' :            ('M', 'C'),
    'elastase' :        ('AGILV', 'C'),
    'formicacid' :      ('D', 'C'),
    'gluc' :            ('DE', 'C'),
    'gluc_bicarb' :     ('E', 'C'),
    'iodosobenzoate' :  ('W', 'C'),
    'lysc' :            ('K', 'C'),
    'lysc_p' :          ('K', 'C'),
    'lysn' :            ('K', 'N'),
    'lysn_promisc' :    ('AKRS', 'N'),
    'pepsina' :         ('FL', 'C'),
    'protein_endopeptidase' : ('P', 'C'),
    'staph_protease' :  ('E', 'C'),
    'trypsin' :         ('KR', 'C'),
    'trypsin_p' :       ('KR', 'C'),
    'trypsin/cnbr' :    ('KRM', 'C'),
    'trypsin/gluc' :    ('DEKR', 'C'),
}


'''
import ursgal.ucore
import os


TESTS = [
    {
        'sequence' : 'RKRK',
        'result'   : ['R','K','R','K'],
        'mc3_result':['RK', 'RKR', 'RKRK', 'KR', 'KRK', 'RK', 'R', 'K', 'R', 'K'],
        'no_missed_cleavages_result': ['RK', 'RKR', 'KR', 'KRK', 'RK', 'R', 'K', 'R', 'K'],
        'enzyme'   : ('KR', 'C'),
    },
    {
        'sequence' : 'IKI',
        'result'   : ['IK','I',],
        'mc3_result' : ['IKI', 'IK', 'I'],
        'no_missed_cleavages_result': ['IKI', 'IK', 'I'],
        'enzyme'   : ('KR', 'C'),
    },
    {
        'sequence' : 'FMWY',
        'result'   : ['F','M','W','Y'],
        'mc3_result': ['FM', 'FMW', 'FMWY', 'MW', 'MWY', 'WY', 'F', 'M', 'W', 'Y'],
        'no_missed_cleavages_result': ['FM', 'FMW', 'MW', 'MWY', 'WY', 'F', 'M', 'W', 'Y'],
        'enzyme'   : ('FMWY', 'C'),
    },
    {
        'sequence' : 'RKRK',
        'result'   : ['RK','RK'],
        'mc3_result' : ['RKRK', 'RK', 'RK'],
        'no_missed_cleavages_result': ['RKRK', 'RK', 'RK'],
        'enzyme'   : ('K', 'C'),
    },
    {
        'sequence' : 'RKRK',
        'result'   : ['R','KR', 'K'],
        'mc3_result' : ['RKR', 'RKRK', 'KRK', 'R', 'KR', 'K'],
        'no_missed_cleavages_result': ['RKR', 'RKRK', 'KRK', 'R', 'KR', 'K'],
        'enzyme'   : ('K', 'N'),
    },
    {
        'sequence' : 'PEPTID',
        'result'   : ['P','EP','TID'],
        'mc3_result': ['PEP', 'PEPTID', 'EPTID', 'P', 'EP', 'TID'],
        'no_missed_cleavages_result': ['PEP', 'PEPTID', 'EPTID', 'P', 'EP', 'TID'],

        'enzyme'   : ('P', 'C'),
    },
    {
        'sequence': 'PEPTIDELIVSRPPAWVMLEHFPYQFRSVAPDDVDIDIEEEK',
        'result':['PEPTIDELIVSR', 'PPAWVMLEHFPYQFR', 'SVAPDDVDIDIEEEK'],
        'mc3_result':['PEPTIDELIVSRPPAWVMLEHFPYQFR',
                     'PEPTIDELIVSRPPAWVMLEHFPYQFRSVAPDDVDIDIEEEK',
                     'PPAWVMLEHFPYQFRSVAPDDVDIDIEEEK',
                     'PEPTIDELIVSR',
                     'PPAWVMLEHFPYQFR', 'SVAPDDVDIDIEEEK'],
        'no_missed_cleavages_result': ['PEPTIDELIVSRPPAWVMLEHFPYQFR',
                       'PEPTIDELIVSRPPAWVMLEHFPYQFRSVAPDDVDIDIEEEK',
                       'PPAWVMLEHFPYQFRSVAPDDVDIDIEEEK', 'PEPTIDELIVSR',
                       'PPAWVMLEHFPYQFR', 'SVAPDDVDIDIEEEK'],
        'enzyme': ('KR', 'C'),
    },
]

def digest_test():
     for test_id, test_dict in enumerate(TESTS):
         yield digest_msc1, test_dict

     for test_id, test_dict in enumerate(TESTS):
         yield digest, test_dict

     for test_id, test_dict in enumerate(TESTS):
            yield digest_not_missed_cl, test_dict



def digest( test_dict ):
    '''
    peptide_regex(self, database, protein_id, peptide):
    '''
    digest_result = ursgal.ucore.digest(
        test_dict['sequence'],
        test_dict['enzyme'],
        no_missed_cleavages = True
    )
    assert digest_result == test_dict['result']

def digest_msc1( test_dict ):
    '''
    peptide_regex(self, database, protein_id, peptide):
    '''
    digest_result = ursgal.ucore.digest(
        test_dict['sequence'],
        test_dict['enzyme'],
        count_missed_cleavages=3
    )

    assert digest_result == test_dict['mc3_result']

def digest_not_missed_cl( test_dict ):
    '''
    peptide_regex(self, database, protein_id, peptide):
    '''
    digest_result = ursgal.ucore.digest(
        test_dict['sequence'],
        test_dict['enzyme'],
        no_missed_cleavages = False
    )
    assert digest_result == test_dict['no_missed_cleavages_result']



if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        #digest(test_dict)
        digest_msc1(test_dict)
