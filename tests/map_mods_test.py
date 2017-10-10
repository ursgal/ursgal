#!/usr/bin/env python3
# encoding: utf-8
'''

Test the filter_csv function for xtandem engine

'''
import ursgal
import csv
import os


R = ursgal.UController()


TESTS = [
    {
        'modifications' : [ 'M,opt,any,Oxidation' ],
        'type' : 'opt',
        'result_dict': {
            '_id'   : 0,
            'aa'    : 'M',
            'mass'  : 15.994915,
            'pos'   : 'any',
            'name'  : 'Oxidation',
            'composition' : {'O': 1},
            'org'   : 'M,opt,any,Oxidation',
            'id'    : '35',
            'unimod': True,
        },
    },
    {
        'modifications' : [ 'C,fix,any,Carbamidomethyl' ],
        'type' : 'fix',
        'result_dict': {
            '_id'   : 0,
            'aa'    : 'C',
            'mass'  : 57.021464,
            'pos'   : 'any',
            'name'  : 'Carbamidomethyl',
            'composition' : {'O': 1, 'N': 1, 'C': 2, 'H': 3},
            'org'   : 'C,fix,any,Carbamidomethyl',
            'id'    : '4',
            'unimod': True,
        },
    },
]

def map_mods_test():
    for test_id, test_dict in enumerate(TESTS):
        yield map_mods, test_dict

def map_mods( test_dict ):
    R = ursgal.UController(
        params = {'modifications' : test_dict['modifications']}
        )
    ursgal.UNode.map_mods(R)
    map_mod_dict = R.params[ 'mods' ][test_dict['type']][0]
    for k, v in test_dict['result_dict'].items():
        assert v == map_mod_dict[k]
    # os.remove(output_csv)

if __name__ == '__main__':
    print(__doc__)
    for test_id, test_dict in enumerate(TESTS):
        map_mods(test_dict)
