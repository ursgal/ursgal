#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import ursgal.unimod_mapper

M = ursgal.unimod_mapper.UnimodMapper()

UNIMODMAPPER_FUNCTIONS = [
    M.name2mass,
    M.name2mass,
    M.name2composition,
    M.name2id,
    M.id2mass,
    M.id2composition,
    M.id2name,
    M.mass2name_list,
    M.mass2id_list,
    M.mass2composition_list,
    M.appMass2id_list,
    M.appMass2element_list,
    M.appMass2name_list,
    M.composition2name_list,
    M.composition2id_list
]

TESTS = [
    [
        {
            'in' : {
                'args': ['ICAT-G:2H(8)']
            },
            'out': 494.30142
        },  # First test : ursgal.UnimodMapper.name2mass,
        {
            'in' : {
                'args': [' ICAT-G:2H(8)']
            },
            'out': 494.30142
        },  # second test that passes to many whitespaces :),
        {
            'in' : {
                'args': ['ICAT-G:2H(8)']
            },
            'out': {'H': 30, 'C': 22, 'O': 6, 'S': 1, '2H': 8, 'N': 4}
        },  # ursgal.UnimodMapper.name2composition,
        {
            'in' : {
                'args': ['ICAT-G:2H(8)']
            },
            'out' : '9'
        },  # ursgal.UnimodMapper.name2id,
        {
            'in' : {
                'args': ['9']
            },
            'out': 494.30142
        },  # ursgal.UnimodMapper.id2mass,
        {
            'in' : {
                'args': ['9']
            },
            'out' : {'N': 4, 'S': 1, '2H': 8, 'O': 6, 'C': 22, 'H': 30}
        },  # ursgal.UnimodMapper.id2composition,
        {
            'in' : {
                'args': '9'
            },
            'out' : 'ICAT-G:2H(8)'
        },  # ursgal.UnimodMapper.id2name,
        {
            'in' : {
                'args': [494.30142]
            },
            'out': ['ICAT-G:2H(8)']
        },  # ursgal.UnimodMapper.mass2name_list,
        {
            'in' : {
                'args': [494.30142]
            },
            'out' : ['9']
        },  # ursgal.UnimodMapper.mass2id_list,
        {
            'in' : {
                'args': [494.30142]
            },
            'out' : [{'N': 4, 'S': 1, '2H': 8, 'O': 6, 'C': 22, 'H': 30}]
        },  # ursgal.UnimodMapper.mass2composition_list,
        {
            'in' : {
                'args': [18],
                'kwargs': {'decimal_places': 0 }
            },
            'out': ['127', '329', '608', '1079', '1167']
        },  # ursgal.UnimodMapper.appMass2id_list
        {
            'in' : {
                'args': [18],
                'kwargs': {'decimal_places': 0 }
            },
            'out': [{'F': 1, 'H': -1}, {'13C': 1, 'H': -1, '2H': 3}, {'H': -2, 'C': -1, 'S': 1}, {'H': 2, 'C': 4, 'O': -2}, {'H': -2, 'C': -1, 'O': 2}]
        },  # ursgal.UnimodMapper.appMass2element_list
        {
            'in' : {
                'args': [18],
                'kwargs': {'decimal_places': 0 }
            },
            'out': ['Fluoro', 'Methyl:2H(3)13C(1)', 'Xle->Met', 'Glu->Phe', 'Pro->Asp']
        },  # ursgal.UnimodMapper.appMass2name_list
        {
            'in' : {
                'args': ['C(2)H(3)N(1)O(1)'],
            },
            'out': ['Carbamidomethyl', 'Ala->Gln', 'Gly->Asn', 'Gly']
        },
        {
            'in' : {
                'args': [ 'C(22)H(30)2H(8)N(4)O(6)S(1)'],
            },
            'out': ['9']
        },



        # end of first data set ...
    ]
]


def test_set_integrity_test():
    for test_id, list_of_test in enumerate(TESTS):
        yield input_list_check, list_of_test


def input_list_check( list_of_test ):
    '''
    Checks that the number of tests can actually be zipped
    with the unimodMapper functions
    '''
    assert len(list_of_test) <= len(UNIMODMAPPER_FUNCTIONS)


def unimodMapper_conversion_test():
    for test_id, list_of_test in enumerate(TESTS):
        test_function_association = zip( list_of_test, UNIMODMAPPER_FUNCTIONS )
        for test_dict, mapper_function in test_function_association:
            if 'kwargs' not in test_dict['in'].keys():
                test_dict['in']['kwargs'] = {}
            yield mapper_function_check, test_dict, mapper_function


def mapper_function_check( test_dict, mapper_function):
        mapper_output = mapper_function(
            *test_dict['in']['args'],
            **test_dict['in']['kwargs']
        )
        print(mapper_output,test_dict['out'])
        assert mapper_output == test_dict['out']


if __name__ == '__main__':
    print('Yes!')
