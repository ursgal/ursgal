#!/usr/bin/env python3
'''

Tests the reformat peptide function in ucore


'''
import re
import ursgal.ucore

TESTS = [
    {
        'unformated_peptide':   '(ac)SSSLM(ox)RPGPSR',
        'regex_list':[('\(ac\)','Acetyl'), ('\(ox\)','Oxidation') ],
        'result': 'SSSLMRPGPSR#Acetyl:0;Oxidation:5'
    },
    {
        'unformated_peptide':   '(ac)1234(ox)56(ox)7',
        'regex_list':[('\(ac\)','Acetyl'), ('\(ox\)','Oxidation') ],
        'result': '1234567#Acetyl:0;Oxidation:4;Oxidation:6'
    },
    {
        'unformated_peptide':   '(ac)1234(ox)56(ox)7',
        'regex_list':[('\(ox\)','Oxidation'),('\(ac\)','Acetyl')],
        'result': '1234567#Acetyl:0;Oxidation:4;Oxidation:6'
    },
    {
        'unformated_peptide':   '(ox)1234(ac)56(ox)7',
        'regex_list':[('\(ox\)','Oxidation'),('\(ac\)','Acetyl')],
        'result': '1234567#Oxidation:0;Acetyl:4;Oxidation:6'
    },
    {
        'unformated_peptide':   '(ac)1234(ox)56(ox)7',
        'regex_list':[ ('\(ox\)','Oxidation') ],
        'result': '(ac)1234567#Oxidation:8;Oxidation:10'
    },
    {
        'unformated_peptide':   '1234567',
        'regex_list':[ ('\(ox\)','Oxidation') ],
      'result':   '1234567'
    },
    {
        'unformated_peptide':   '1234567#',
        'regex_list':[ ('\(ox\)','Oxidation') ],
      'result':   '1234567'
    },
    {
        'unformated_peptide':   'AIVDC(cm)GFEHPSEVQHEC(cm)IPQAILGM(ox)DVLC(cm)QAK',
        'regex_list':[ ('\(ox\)','Oxidation'), ('\(cm\)','Carbamidomethyl') ],
        'result': 'AIVDCGFEHPSEVQHECIPQAILGMDVLCQAK#Carbamidomethyl:5;Carbamidomethyl:17;Oxidation:25;Carbamidomethyl:29'
    },
    {
        'unformated_peptide':   '12(cm)34(cm)5(ox)6(cm)78',
        'regex_list':[ ('\(ox\)','Oxidation'), ('\(cm\)','Carbamidomethyl') ],
        'result': '12345678#Carbamidomethyl:2;Carbamidomethyl:4;Oxidation:5;Carbamidomethyl:6'
    },
    {
        'unformated_peptide':   '12(cm)34(cm)5(ox)6(cm)78',
       'regex_list': [  ('\(cm\)','Carbamidomethyl'), ('\(ox\)','Oxidation') ],
       'result':  '12345678#Carbamidomethyl:2;Carbamidomethyl:4;Oxidation:5;Carbamidomethyl:6'
    },
    {
       'unformated_peptide':   'M(O)C(Cam)C(Cam)HDWRR',
       'regex_list': [  ('\(Cam\)','Carbamidomethyl'), ('\(O\)','Oxidation') ],
       'result':  'MCCHDWRR#Oxidation:1;Carbamidomethyl:2;Carbamidomethyl:3'
    },
    {
       'unformated_peptide':   '[Acetyl]C(Cam)M(O)M(O)MGASDGK',
       'regex_list': [  ('\(Cam\)','Carbamidomethyl'), ('\(O\)','Oxidation'), ('\[Acetyl\]','Acetyl') ],
       'result':  'CMMMGASDGK#Acetyl:0;Carbamidomethyl:1;Oxidation:2;Oxidation:3'
    },
    {
       'unformated_peptide':   ' SCCPCCM(O)ALHAGC(Carboxymethyl)R',
       'regex_list': [  ('\(Carboxymethyl\)','Carboxymethyl'), ('\(O\)','Oxidation') ],
       'result':  'SCCPCCMALHAGCR#Oxidation:7;Carboxymethyl:13'
    }
]


def handle_entry_test():
    for test_no, test_dict in enumerate(TESTS):
        yield _reformat_peptide, \
            test_no, \
            test_dict


def _reformat_peptide( test_no, test_dict ):
    formated_peptide = test_dict['unformated_peptide']
    for regex_pattern, unimod_name in test_dict['regex_list']:
        formated_peptide = ursgal.ucore.reformat_peptide(
            regex_pattern,
            unimod_name,
            formated_peptide
        )
    print( formated_peptide , test_dict['result'])
    assert formated_peptide == test_dict['result']

if __name__ == '__main__':
    print(__doc__)
    for test_no, test_dict in enumerate(TESTS):
        formated_peptide = test_dict['unformated_peptide']
        for regex_pattern, unimod_name in test_dict['regex_list']:
            formated_peptide = ursgal.ucore.reformat_peptide(
                regex_pattern,
                unimod_name,
                formated_peptide
            )
        print( formated_peptide , test_dict['result'])
        assert formated_peptide == test_dict['result']

