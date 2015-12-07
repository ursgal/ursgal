#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os

R = ursgal.UController()

TESTS = [
    {
        'input' : os.path.join('data', 'test.json'),
        'output' : '379450895e2c116886b2e92dfcd68b2b'
    },
    {
        'input' : os.path.join('data', 'test_without_database.json'),
        'output' : 'deb20d01ff369188a583decf203cf769'
    }
]


def check_md5_test():
    for test_id, test_dict in enumerate(TESTS):
        yield check_md5, test_dict


def check_md5( test_dict ):
    out_put = R.calc_md5( test_dict['input'] )
    print( out_put , test_dict)
    assert out_put == test_dict['output'], '''
        MD5 {0} failed
        output: {1}'''.format(
            test_dict,
            out_put
        )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        check_md5( test_dict )
