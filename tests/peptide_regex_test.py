#!/usr/bin/env python3.4
# encoding: utf-8
'''

Test the peptide_regex function

'''
import ursgal
import os

database = os.path.join( 'data', 'BSA.fasta')

R = ursgal.UController(
    profile = 'LTQ XL low res',
    params  = {
        'database' : database
    },
    force   = False
)
# print(R)
# exit()
TESTS = [
    {
        'peptide' : 'SHCIAEVEK',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : 309,
        'stop'    : 318,
        'pre_aa'  : 'K',
        'post_aa' : 'D'
    },
    {
        'peptide' : 'SHCIAEVE',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4', # test short id
        'start'   : 309,
        'stop'    : 317,
        'pre_aa'  : 'K',
        'post_aa' : 'K'
    },
    {
        'peptide' : 'SHUIAEVEK',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : 309,
        'stop'    : 318,
        'pre_aa'  : 'K',
        'post_aa' : 'D'
    },
    {
        'peptide' : 'YOLO',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : None,
        'stop'    : None,
        'pre_aa'  : None,
        'post_aa' : None
    },
    {
        'peptide' : 'SHXIAEVEK',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : None,
        'stop'    : None,
        'pre_aa'  : None,
        'post_aa' : None
    },
    {
        'peptide' : 'SHCIUEVEK',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : 309,
        'stop'    : 318,
        'pre_aa'  : 'K',
        'post_aa' : 'D'
    },
    {
        'peptide' : 'EYEATLEECCAK',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : 374,
        'stop'    : 386,
        'pre_aa'  : 'K',
        'post_aa' : 'D'
    },
    {
        'peptide' : 'EYEATLEEUUAK',
        'protein_id':'sp|P02769|ALBU_BOVIN Serum albumin OS=Bos taurus GN=ALB PE=1 SV=4',
        'start'   : 374,
        'stop'    : 386,
        'pre_aa'  : 'K',
        'post_aa' : 'D'
    },




]
# print(ident_list)
def peptide_regex_test():
    for test_id, test_dict in enumerate(TESTS):
        yield peptide_regex, test_dict

def peptide_regex( test_dict ):
    '''
    peptide_regex(self, database, protein_id, peptide):
    '''
    return_list = R.peptide_regex(
        database,
        test_dict['protein_id'],
        test_dict['peptide'],
    )
    for start,stop,pre_aa,post_aa, protein_id in return_list:
        print(test_dict)
        print(start,stop,pre_aa,post_aa,protein_id)
        print()
        assert start      == test_dict['start']
        assert stop       == test_dict['stop']
        assert pre_aa     == test_dict['pre_aa']
        assert post_aa    == test_dict['post_aa']
        assert protein_id == test_dict['protein_id']






if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        peptide_regex(test_dict)

