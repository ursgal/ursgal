#!/usr/bin/env python3
# encoding: utf-8
'''

Test the peptide_regex function

'''
import ursgal
import os

database = os.path.join( 'tests', 'data', 'BSA.fasta')

R = ursgal.UController(
    profile = 'LTQ XL low res',
    params  = {
        'database' : database
    },
    force   = False
)

TESTS = [
    {
        'peptide' : 'SHCIAEVEK',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : 310,
        'stop1'    : 318,
        'pre_aa1'  : 'K',
        'post_aa1' : 'D'
    },
    {
        'peptide' : 'SHCIAEVE',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4', # test short id
        'start1'   : 310,
        'stop1'    : 317,
        'pre_aa1'  : 'K',
        'post_aa1' : 'K'
    },
    {
        'peptide' : 'YOLO',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : None,
        'stop1'    : None,
        'pre_aa1'  : None,
        'post_aa1' : None
    },
    {
        'peptide' : 'SHXIAEVEK',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : None,
        'stop1'    : None,
        'pre_aa1'  : None,
        'post_aa1' : None
    },

    {
        'peptide' : 'EYEATLEECCAK',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : 375,
        'stop1'    : 386,
        'pre_aa1'  : 'K',
        'post_aa1' : 'D'
    },
    {
        'peptide' : 'LR',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : 104,
        'stop1'    : 105,
        'pre_aa1'  : 'S',
        'post_aa1' : 'E',
        'start2'   : 221,
        'stop2'    : 222,
        'pre_aa2'  : 'R',
        'post_aa2' : 'C',
        'start3'   : 370,
        'stop3'    : 371,
        'pre_aa3'  : 'L',
        'post_aa3' : 'L'
    },
    {
        'peptide' : 'MKWVTFISLLLLFSSAYSR',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : 1,
        'stop1'    : 19,
        'pre_aa1'  : '-',
        'post_aa1' : 'G'
    },
    {
        'peptide' : 'LVVSTQTALA',
        'protein_id1':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start1'   : 598,
        'stop1'    : 607,
        'pre_aa1'  : 'K',
        'post_aa1' : '-'
    },

]

def peptide_regex_test():
    for test_id, test_dict in enumerate(TESTS):
        yield peptide_regex, test_dict

def peptide_regex( test_dict ):
    '''
    peptide_regex(self, database, protein_id, peptide):
    '''
    return_list = R.peptide_regex(
        database,
        test_dict['protein_id1'],
        test_dict['peptide'],
    )
    print(return_list)
    for n, proteins in enumerate(return_list):
        for m, pep_regex in enumerate(proteins): 
            start,stop,pre_aa,post_aa, protein_id = pep_regex
            print(test_dict)
            print(start,stop,pre_aa,post_aa,protein_id)
            print()
            assert start      == test_dict['start{0}'.format(m+1)]
            assert stop       == test_dict['stop{0}'.format(m+1)]
            assert pre_aa     == test_dict['pre_aa{0}'.format(m+1)]
            assert post_aa    == test_dict['post_aa{0}'.format(m+1)]
            assert protein_id == test_dict['protein_id{0}'.format(n+1)]


if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        peptide_regex(test_dict)

