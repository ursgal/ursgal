#!/usr/bin/env python3.4
'''
Convert .csv files to counted result files (.csv)

usage:
    ./csv2counted_results_1_0_0.py <input_file> <output_file>

Note:
    The input_file should be a unified, merged (if applicable) result file

'''

import sys
import os
import csv
import ursgal

if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


def main(
    input_file=None,
    output_file=None,
    identifier_colum_names  = None, #list of fieldnames
    count_column_names   = None, #list of fieldnames
    count_by_file           = True,
    convert2sfinx           = False,
):
    '''
    Results (.csv) are summarized as table (.csv) containing all identified
    proteins, peptides, or other specified identifiers. For each sample,
    the peptide or spectral count for each identifier is given.
    
    This can be used to convert .csv files to SFINX input files.

    This is a .csv file containing unique peptide counts
    for all identified proteins. However, this can be modified
    using the keywords "identifier_colum_names" and "count_column_names"

    Keyword arguments:

        input_file (str): name including path for the input file
        output_file (str): name including path for  the output file
        identifier_colum_names (list): list of column headers
            that define the identifier. Multiple column names are
            joined for combined identifiers.
        count_column_names (list): list of column headers which
            are used for counting.
        count_by_file (bool): the number of unique hits for each
            identifier is given in seperate columns for each raw file
            (file name as defiened in Spectrum Title)
        convert2sfinx (bool): If True, the header of the identifier column
            is "rownames". If False, the joined header name will be used. 
    '''

    csv_kwargs = {}
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'

    output_file_object = open(output_file,'w')
    
    if convert2sfinx:
        first_column = 'rownames'
    else:
        first_column = '#'.join(identifier_colum_names)

    new_fieldnames = [
        first_column,
    ]

    count_dict, all_filenames = count_results(
        identifier_colum_names = identifier_colum_names,
        count_column_names = count_column_names,
        count_by_file = True,
        input_file = input_file,
    )
    for filename in sorted(all_filenames):
        new_fieldnames.append(filename)

    csv_output = csv.DictWriter(
            output_file_object,
            new_fieldnames,
            **csv_kwargs
        )
    csv_output.writeheader()

    for identifier in count_dict.keys():
        out_dict = {}
        out_dict[first_column] = identifier
        for filename in all_filenames:
            out_dict[filename] = len(count_dict[identifier].get(filename, []))
        csv_output.writerow( out_dict )


def count_results(
    identifier_colum_names  = None, #list of fieldnames
    count_column_names   = None, #list of fieldnames
    count_by_file           = True,
    input_file              = None,
):
    count_dict = {}
    all_filenames = set()
    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader( in_file )
        for csv_line_dict in csv_input:
            identifier = []
            for column_name in identifier_colum_names:
                identifier.append(csv_line_dict[column_name])
            identifier = '#'.join(identifier)
            if identifier not in count_dict.keys():
                count_dict[identifier] = {}
            if count_by_file:
                filename = csv_line_dict['Spectrum Title'].split('.')[0]
            else:
                filename = 'all'
            all_filenames.add(filename)
            if filename not in count_dict[identifier].keys():
                count_dict[identifier][filename] = set()
            countable = []
            for column_name in count_column_names:
                countable.append(csv_line_dict[column_name])
            countable = '#'.join(countable)
            count_dict[identifier][filename].add(countable)

    return count_dict, all_filenames

if __name__ == '__main__':
    main(
        input_file     = sys.argv[1],
        output_file    = sys.argv[2],
        identifier_colum_names = ['Protein ID'],
        count_column_names = ['Sequence'],
        count_by_file = True,
    )
