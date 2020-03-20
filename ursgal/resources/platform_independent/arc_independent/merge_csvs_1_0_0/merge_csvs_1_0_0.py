#!/usr/bin/env python
'''
Merges csvs into one single one.

Usage:
./merge_csvs_1_0_0.py <mzML File1> ... <mzML FileN>

Note: All headers have to be the same, otherwise warning will be printed
'''

from __future__ import print_function
import sys
import os
import csv

# csv.field_size_limit(sys.maxsize)


def main(csv_files=None, output=None):
    '''Merges ident csvs'''
    assert output is not None, 'merge_csv requires output file name'
    buffered_input_files = {}
    all_fieldnames = []
    all_fieldnames_the_same = True
    for i, csv_file in enumerate( csv_files ):
        file_object = open( csv_file , 'r' )
        buffered_input_files[ csv_file ] = csv.DictReader(
            row for row in file_object if not row.startswith('#')
        )
        for fieldname in buffered_input_files[ csv_file ].fieldnames:
            if fieldname not in all_fieldnames:
                all_fieldnames.append( fieldname )
                if i != 0:
                    all_fieldnames_the_same = False

    if all_fieldnames_the_same is False:
        print('''
    WARNING!
    WARNING!   Not all fieldnames / headers of the input csvs were the same!
    WARNING!
        ''')
    out_csv = open( output, 'w')
    csv_kwargs = {}
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'
    csv_writer = csv.DictWriter(
        out_csv,
        all_fieldnames,
        **csv_kwargs
    )
    csv_writer.writeheader()

    for csv_file, csv_dict_reader in buffered_input_files.items():
        for line_dict in csv_dict_reader:
            csv_writer.writerow( line_dict )
    out_csv.close()
    return None


if __name__ == '__main__':
    # parsing command line arguments:
    if len(sys.args) == 1:
        print(__doc__)
        sys.exit(1)
    else:
        main(
            csv_files = sys.argv[1:],
            output = 'merged_csv.py'
        )
