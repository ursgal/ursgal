#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os

R = ursgal.UController()

TESTS = [
    {
        'params' : {'database' : os.path.join(os.sep,'tmp','..','mo_fasta.fasta')} ,
        'output' : {'database' : os.path.join(os.path.abspath( os.sep ),'mo_fasta.fasta')}
    },
    {
        'params' : {'mosh' : os.path.join(os.sep,'tmp','..','mo_fasta.fasta')},
        'input_kwargs' : {'param_keys' : ['mosh']},
        'output' : {'mosh' : os.path.join(os.path.abspath( os.sep ),'mo_fasta.fasta')}
    },
]


def abs_paths_for_specific_keys_test():
    for test_id, test_dict in enumerate(TESTS):
        yield abs_paths_for_specific_keys, test_dict


def abs_paths_for_specific_keys( test_dict ):
    if 'input_kwargs' not in test_dict.keys():
        test_dict[ 'input_kwargs' ] = {}
    out_put = R.abs_paths_for_specific_keys(
        test_dict['params'],
        **test_dict['input_kwargs']
    )
    assert out_put == test_dict['output'], 'Abspaths {0} failed'.format(
        test_dict
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        abs_paths_for_specific_keys( test_dict )
