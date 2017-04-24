#!/usr/bin/env python3
# encoding: utf-8

import ursgal
import os
import sys

R = ursgal.UController()

TESTS = [
    {
        'input' : os.path.join('tests', 'data', 'test.json'),
        'output' : {
            'unix' : '379450895e2c116886b2e92dfcd68b2b',
            'win32': '54c19ed069413037dc857a0130dd2527'
        }
    },
    {
        'input' : os.path.join('tests', 'data', 'test_without_database.json'),
        'output' : {
            'unix' : 'deb20d01ff369188a583decf203cf769',
            'win32': '26cc3e0850d3ab95c74e4cf680475335'
        }
    }
]


def check_md5_test():
    for test_id, test_dict in enumerate(TESTS):
        yield check_md5, test_dict


def check_md5( test_dict ):
    out_put = R.calc_md5( test_dict['input'] )
    # print( out_put , test_dict)
    # platform = sys.platform
    # if sys.platform != 'win32':
    #     platform = 'unix'

    assert out_put in [test_dict['output']['unix']]+[test_dict['output']['win32']], '''
        MD5 {0} failed
        output: {1}'''.format(
            test_dict,
            out_put
        )


if __name__ == '__main__':
    for test_id, test_dict in enumerate(TESTS):
        check_md5( test_dict )
