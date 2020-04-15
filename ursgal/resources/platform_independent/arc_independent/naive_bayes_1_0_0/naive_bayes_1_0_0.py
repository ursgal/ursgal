#!/usr/bin/python

import csv
import functools
import operator
from collections import defaultdict


def naive_bayes(prob_list):
    '''
    Independent probabilities a, b, c can be combined like this:

                             a*b*c
    combined_prob = -------------------------
                    a*b*c + (1-a)*(1-b)*(1-c)

    For a straightforward explanation, see
    http://www.paulgraham.com/naivebayes.html
    '''

    # multiplying all probabilities: a*b*c
    multiplied_probs = \
        functools.reduce(operator.mul, prob_list, 1)
    # multiplying the opposite of all probabilities: (1-a)*(1-b)*(1-c)
    multiplied_opposite_probs = \
        functools.reduce(operator.mul, (1-p for p in prob_list), 1)
    return multiplied_probs / (multiplied_probs + multiplied_opposite_probs)


def get_row_key(row, columns_for_grouping):
    return tuple( row[c] for c in columns_for_grouping )
        

def list_to_sorted_tuple(l):
    return tuple(sorted(set(l)))


def main(columns_for_grouping=None, input_csvs=None, output_csv=None,
         input_sep=None, output_sep=None, join_sep=None, pep_colname=None,
         input_engines=None):
    '''
    Merges CSVs from different search engines and adds a column called
    'combined PEP' that contains the combination of all engine PEPs
    as computed with the naive Bayes method.
    '''
    assert len(input_csvs) > 1, 'Input must be at least 2 files.'
    columns_for_grouping = list_to_sorted_tuple(columns_for_grouping)

    merged_fieldnames_set = set(['combined PEP', 'engines'])
    merged_dict = defaultdict(dict)
    for input_csv, input_engine in zip(input_csvs, input_engines):
        # give the engine its own PEP column:
        engine_PEP_colname = ':'.join([input_engine, pep_colname])
        merged_fieldnames_set.add(engine_PEP_colname)
        with open(input_csv, 'r', encoding='utf8') as csv_object:
            reader = csv.DictReader(csv_object, delimiter=input_sep)
            merged_fieldnames_set |= set(reader.fieldnames)
            for row in reader:
                row['engines'] = input_engine
                row_key = get_row_key(row, columns_for_grouping)
                for col, val in row.items():
                    if col == pep_colname:
                        merged_dict[row_key][engine_PEP_colname] = val
                        # store the PEP of that PSM in a list that is
                        # used to compute combined PEP later
                        if 'combined PEP' not in merged_dict[row_key]:
                            merged_dict[row_key]['combined PEP'] = []
                        merged_dict[row_key]['combined PEP'].append(val)
                        continue
                    if col not in merged_dict[row_key]:
                        merged_dict[row_key][col] = val
                    elif val == merged_dict[row_key][col]:
                        continue
                        # value is already there, no need to do anything
                    elif val != merged_dict[row_key][col]:
                        #print("WARNING! Conflicting field values in column {0}: {1} and {2}".format(col, val, merged_dict[row_key][col]))
                        old_vals = set(merged_dict[row_key][col].split(join_sep))
                        old_vals.add(val)
                        old_vals.discard('')
                        merged_dict[row_key][col] = join_sep.join(sorted(old_vals))
                    else:
                        raise Exception('This is impossibru!')


    merged_fieldnames = list(columns_for_grouping) + sorted(merged_fieldnames_set - set(columns_for_grouping))
    merged_fieldnames.remove(pep_colname)
    with open(output_csv, 'w', encoding='utf8') as outf:
        writer = csv.DictWriter(outf, fieldnames=merged_fieldnames, delimiter=output_sep)
        writer.writeheader()
        for out_row in merged_dict.values():
            all_PEPs = [float(p) for p in out_row['combined PEP']]
            out_row['combined PEP'] = naive_bayes(all_PEPs)
            writer.writerow(out_row)
    return


def parse_args(verbose=True):
    '''
    Parses command line arguments and returns them in a dict.
    Only used when executing this script without Ursgal.
    '''
    import argparse
    # no need to import argparse when script is executed from ursgal

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input_csvs', type=str, nargs='+', required=True,
        help='Paths to unified input CSV files (2 or more)')
    parser.add_argument(
        '-c', '--columns_for_grouping', type=str, nargs='+', required=True,
        help='Column names by which the rows should be grouped')
    parser.add_argument(
        '-o', '--output_csv', type=str, help='Output CSV name')
    parser.add_argument(
        '-is', '--input_sep', type=str, default=',',
        help='Input file column delimiter character')
    parser.add_argument(
        '-os', '--output_sep', type=str, default=',',
        help='Output file column delimiter character')
    parser.add_argument(
        '-js', '--join_sep', type=str, default=';',
        help='Delimiter for multiple values in the same field')
    parser.add_argument(
        '-e', '--input_engines', type=str, required=True,
        help='The search engines of each input file (must be same order as input_csvs)')

    args = vars(parser.parse_args())  # convert to dict
    if verbose:
        print('You are using the following settings:')
        for arg, val in sorted(args.items()):
            print('  {0: <13}:  {1}'.format(arg, val))
        print()
    return args


if __name__ == '__main__':
    command_line_args = parse_args()
    main(**command_line_args)