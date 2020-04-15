#!/usr/bin/env python
'''
Sanitize the result csvs

usage:
    ./sanitize_csv_1_0_0.py <input_file> <output_file> <validation_score_field> <bigger_scores_better> <score_diff_threshold> <log10_threshold> <accept_conflicting_psms> <num_compared_psms> <remove_redundant_psms>


'''
import sys
import os
import csv
import ursgal
import math
import operator
from collections import defaultdict as ddict

if sys.platform != 'win32':
    csv.field_size_limit(sys.maxsize)


def main( 
    input_file=None, 
    output_file=None,
    grouped_psms=None,
    validation_score_field=None, 
    bigger_scores_better=None,
    score_diff_threshold=2.0,
    log10_threshold=True,
    accept_conflicting_psms=False,
    num_compared_psms=2,
    remove_redundant_psms=False,
):
    '''
    Spectra with multiple PSMs are sanitized, i.e. only the PSM with best PEP score is accepted
    and only if the best hit has a PEP that is at least two orders of magnitude smaller than the others
    '''

    # un = ursgal.UNode()
    # grouped_psms = un._group_psms( input_file, validation_score_field=validation_score_field, bigger_scores_better=bigger_scores_better )

    if grouped_psms is None:
        grouped_psms = group_psms( input_file, validation_score_field=validation_score_field, bigger_scores_better=bigger_scores_better )

    all_line_dicts = []
    for spec_title, grouped_psm_list in grouped_psms.items():
        spec_line_dicts = []
        best_score = None
        psm_names = set()
        for n, grouped_psm in enumerate(grouped_psm_list):
            score, line_dict = grouped_psm
            if n == 0:
                best_score = score
                psm_names.add(line_dict['Sequence']+line_dict['Modifications']+line_dict['Charge'])
                spec_line_dicts.append(line_dict)
            elif n < num_compared_psms:
                psm = line_dict['Sequence']+line_dict['Modifications']+line_dict['Charge']
                if psm in psm_names and remove_redundant_psms is True:
                    continue
                if log10_threshold is True:
                    if abs(math.log10(best_score)) - abs(math.log10(score)) >= score_diff_threshold:
                        break
                    else:
                        spec_line_dicts.append(line_dict)
                        psm_names.add(psm)
                else:
                    if abs(best_score) - abs(score) >= score_diff_threshold:
                        break
                    else:
                        spec_line_dicts.append(line_dict)
                        psm_names.add(psm)
        if accept_conflicting_psms is False and len(spec_line_dicts) >= 2:
            continue   
        else:
            all_line_dicts.extend(spec_line_dicts)


    csv_kwargs = {}
    if sys.platform == 'win32':
        csv_kwargs['lineterminator'] = '\n'
    else:
        csv_kwargs['lineterminator'] = '\r\n'

    output_file_object = open(output_file,'w')

    with open( input_file, 'r' ) as in_file:
        csv_input  = csv.DictReader( in_file )
        fieldnames = csv_input.fieldnames
    in_file.close()
        
    csv_output = csv.DictWriter(
        output_file_object,
        list(fieldnames),
        **csv_kwargs
    )
    csv_output.writeheader()
    for line_dict in all_line_dicts:
        csv_output.writerow( line_dict )
    output_file_object.close()
    return output_file

def group_psms(input_file, validation_score_field=None, bigger_scores_better=None):
    '''
    reads an input csv and returns a defaultdict with the spectrum title
    mapping to a sorted list of tuples containing each
    a) score (from validation_score_field) and
    b) the whole line dict
    '''
    print('[ GROUPING ] Parsing {0}'.format( input_file ))

    if validation_score_field is None:
        search_engine = self.get_last_search_engine( history = self.stats['history'] )
        assert search_engine, 'Can\'t convert results from no specified search engine.'
        assert 'multiple engines:' not in search_engine, 'Can\'t convert merged results from multiple different engines.'
        validation_score_field = self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][search_engine]

    if bigger_scores_better is None:
        bigger_scores_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][search_engine]

    grouped_psms = ddict(list)
    opened_file = open( input_file, 'r')
    csv_dict_reader_object = csv.DictReader(
        row for row in opened_file if not row.startswith('#')
    )
    n = 0

    for n, line_dict in enumerate(csv_dict_reader_object):
        assert validation_score_field in line_dict.keys(), \
            '''defined validation_score_field {0} is not found,
            please check/add it to uparams.py['validation_score_field']'''.format(validation_score_field)


        grouped_psms[ line_dict[ 'Spectrum Title' ] ].append(
            (
                float(
                    line_dict[ validation_score_field ]
                ),
                line_dict
            )
        )
    for spectrum_title in grouped_psms.keys():
        grouped_psms[ spectrum_title ].sort(
            key     = operator.itemgetter(0),
            reverse = bigger_scores_better
        )
    print(
        "[ GROUPING ] Grouped {0} PSMs into {1} unique spectrum titles".format(
            n,
            len( grouped_psms.keys())
        )
    )
    return grouped_psms


if __name__ == '__main__':
    if len(sys.argv) < 10:
        print(__doc__)
        sys.exit(1)

    main(
        input_file              = sys.argv[1],
        output_file             = sys.argv[2],
        validation_score_field  = sys.argv[3], 
        bigger_scores_better    = bool(sys.argv[4]),
        score_diff_threshold    = int(sys.argv[5]),
        log10_threshold         = bool(sys.argv[6]),
        accept_conflicting_psms = bool(sys.argv[7]),
        num_compared_psms       = int(sys.argv[8]),
        remove_redundant_psms   = bool(sys.argv[9]),
    )
