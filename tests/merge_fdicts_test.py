#!/usr/bin/env python3
# encoding: utf-8

import ursgal
R = ursgal.UController()

TESTS = [
    {
        'input'  : [{'1': 0, '2': 0 }, {'1': 1, '2': 0 }],
        'output' : {'1': [0, 1], '2': [0, 0]}
    },
]


def merge_fdicts_test():
    for test_id, test_dict in enumerate(TESTS):
        yield merge_fdicts, test_dict


def merge_fdicts( test_dict ):
    output = R.merge_fdicts( *test_dict['input'] )
    print( output , test_dict)
    assert output == test_dict['output'], '''
        merge_fdicts {0} failed with output {1}'''.format(
        test_dict,
        output
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        merge_fdicts( test_dict )
