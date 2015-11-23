#!/usr/bin/env python3
# encoding: utf-8

import ursgal
R = ursgal.UController()

TESTS = [
    {
        'input' : 'test.json',
        'output' : (False, 'test.json')
    },
    {
        'input' : ['test.json'],
        'output' : (False, 'test.json')
    },
    {
        'input' : ['test.json', '2131'],
        'output' : (True, ['test.json', '2131'])
    },
    # {
    #     'input' : 'test_without_database.json',
    #     'output' : '0cdd52e86608855ac678e212bedd0743'
    # }
]


def distinguish_multi_and_single_input_test():
    for test_id, test_dict in enumerate(TESTS):
        yield distinguish_multi_and_single_input, test_dict


def distinguish_multi_and_single_input( test_dict ):
    out_put = R.distinguish_multi_and_single_input( test_dict['input'] )
    print( out_put , test_dict)
    assert out_put == test_dict['output'], 'MD5 {0} failed'.format(
        test_dict
    )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        distinguish_multi_and_single_input( test_dict )
