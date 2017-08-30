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
        'enzyme'   : ('KR', 'C'),
    },
    {
        'sequence' : 'IKI',
        'result'   : ['IK','I',],
        'enzyme'   : ('KR', 'C'),
    },
    {
        'sequence' : 'FMWY',
        'result'   : ['F','M','W','Y'],
        'enzyme'   : ('FMWY', 'C'),
    },
    {
        'sequence' : 'RKRK',
        'result'   : ['RK','RK'],
        'enzyme'   : ('K', 'C'),
    },
    {
        'sequence' : 'RKRK',
        'result'   : ['R','KR', 'K'],
        'enzyme'   : ('K', 'N'),
    },
    {
        'sequence' : 'PEPTID',
        'result'   : ['P','EP','TID'],
        'enzyme'   : ('P', 'C'),
    },
]

def digest_test():
    for test_id, test_dict in enumerate(TESTS):
        yield digest, test_dict

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



if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        digest(test_dict)
