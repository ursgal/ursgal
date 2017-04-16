#!/usr/bin/env python3.4
# encoding: utf-8
import ursgal
import glob
import os.path
import sys
import tempfile
import time


def main():
    uc = ursgal.UController( verbose=True)
    # test_start = uc.time_point( tag='2s sleep test', format_time=True)
    # print( test_start )
    # time.sleep(2)
    # uc.print_execution_time( tag='2s sleep test')
    temp_int, temp_fpath = tempfile.mkstemp(prefix='ursgal_', suffix='.csv')
    temp_fobject = open( temp_fpath, 'w')
    print('test 1,2,3', file=temp_fobject)
    temp_fobject.close()
    test_1 = uc.execute_unode( temp_fpath, '_test_node')
    test_2 = uc.execute_unode( test_1, '_test_node')

if __name__ == "__main__":
    main()
