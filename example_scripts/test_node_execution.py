#!/usr/bin/env python3
# encoding: utf-8
import ursgal
import glob
import os.path
import sys
import tempfile
import time


def main():
    '''
    Testscript for executing the test node, which also tests the run time
    determination function.

    Usage:
        ./test_node_excution.py

    '''
    uc = ursgal.UController(verbose=True)
    temp_int, temp_fpath = tempfile.mkstemp(
        prefix='ursgal_',
        suffix='.csv'
    )
    temp_fobject = open(temp_fpath, 'w')
    print('test 1,2,3', file=temp_fobject)
    temp_fobject.close()
    test_1 = uc.execute_unode(
        temp_fpath,
        '_test_node'
    )
    test_2 = uc.execute_unode(
        test_1,
        '_test_node'
    )

if __name__ == "__main__":
    main()
