#!/usr/bin/env python3
# encoding: utf-8

import ursgal

TESTS = [
    {
        'input'  : [
            {'XTandem': '34', 'Spectrum ID': '5', 'PEP': '3.5'},
            {'XTandem': '1', 'Spectrum ID': '5', 'PEP': '2'}
        ],
        'output' : {
            'XTandem': 34, 'Spectrum ID': '5', 'PEP': '3.5;2'
        },
        'type_merge' : 'max_value'
    },
    {
        'input'  : [
            {'XTandem': '34', 'Spectrum ID': '5', 'PEP': '3.5'},
            {'XTandem': '1', 'Spectrum ID': '5', 'PEP': '2'}],
        'output' : {
            'XTandem': 1, 'Spectrum ID': '5', 'PEP': '3.5;2'
        },
        'type_merge' : 'min_value'
    },
    {
        'input'  : [
            {'XTandem': '34', 'Spectrum ID': '5', 'PEP': '3.5'},
            {'XTandem': '25', 'Spectrum ID': '5', 'PEP': '2'}
        ],
        'output' : {
            'XTandem': 29.5, 'Spectrum ID': '5', 'PEP': '3.5;2'
        },
        'type_merge' : 'avg_value'
    },
    {
        'input'  : [
            {'XTandem': '34', 'Spectrum ID': '5', 'PEP': '3.5'},
            {'XTandem': '1', 'Spectrum ID': '5', 'PEP': '2'},
            {'XTandem': '1', 'Spectrum ID': '5', 'PEP': '2'}
        ],
        'output' : {
            'XTandem': '1', 'Spectrum ID': '5', 'PEP': '3.5;2;2'
        },
        'type_merge' : 'most_frequent'
    },
    {
        'input'  : [
            {'XTandem': '34', 'Spectrum ID': '5', 'PEP': '3.5'},
            {'XTandem': '34', 'Spectrum ID': '5', 'PEP': '2'},
            {'XTandem': '1', 'Spectrum ID': '5', 'PEP': '2'},
            {'XTandem': '1', 'Spectrum ID': '5', 'PEP': '2'},
            {'XTandem': '2', 'Spectrum ID': '5', 'PEP': '2'}

        ],
        'output' : {
            'XTandem': '34;1', 'Spectrum ID': '5', 'PEP': '3.5;2;2;2;2'
        },
        'type_merge' : 'most_frequent'
    },

]


def merge_rowdicts_test():
    for test_id, test_dict in enumerate(TESTS):
        yield merge_rowdicts, test_dict


def merge_rowdicts(test_dict):
    output = ursgal.ucore.merge_rowdicts(
        list_of_rowdicts=test_dict['input'],
        joinchar=';',
        psm_colnames_to_merge_multiple_values={
            'XTandem': test_dict['type_merge']
        },
    )

    print(output, test_dict)
    assert output == test_dict['output'], '''
        merge_rowdicts failed!
        expected output:
        {0}
        produced putput:
        {1}'''.format(
        test_dict['output'],
        output
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        merge_rowdicts(test_dict)
