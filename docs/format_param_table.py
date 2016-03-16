#!/usr/bin/env python3.4
# encoding: utf-8

import glob
import os
import xlrd


if __name__ == '__main__':
    print('''
        Converting parameter tables from xls into rst files for the docs
''')
    book = xlrd.open_workbook('source/ursgal_params.xls')
    # print("The number of worksheets is", book.nsheets)
    # print("Worksheet name(s):", book.sheet_names())
    sh = book.sheet_by_index(0)
    # print(sh.name, sh.nrows, sh.ncols)
    # print("Cell A1 is", sh.cell_value(rowx=0, colx=0))
    with open('source/parameter_description.inc', 'w') as io:
        print('Ursgal Descriptions',file=io)
        print('-------------------',file=io)
        print('',file=io)
        for row in range(3, sh.nrows):
            name = sh.cell_value(rowx=row, colx=0)
            if '--' in name:
                continue
            default = sh.cell_value(rowx=row, colx=1)
            value = sh.cell_value(rowx=row, colx=2)
            if isinstance(default,str):
                default = default.strip()
            if value == '':
                continue
            print('{0}'.format(name),file=io)
            print('^'*len(name),file=io)
            print('',file=io)
            # print()
            print('\t| {0}'.format(value), file=io)
            if default == '':
                print('\t| default: {0}'.format(default), file=io)
            else:
                print('\t| default: *{0}*'.format(default), file=io)
            print('',file=io)


