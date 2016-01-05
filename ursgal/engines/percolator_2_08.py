#!/usr/bin/env python3.4
import ursgal
import math
import csv
import bisect
import os
from collections import defaultdict as ddict
import sys

PROTON = 1.00727646677


def transform_score( score, minimum_score ):
    '''Transform scores for "bigger_is_better" == False into linear and positive space'''
    minimum_score_transformed = -1 * math.log( minimum_score, 10 )
    try:
        transformed_score = -1 * math.log( score, 10 )
    except:
        transformed_score = minimum_score_transformed

    if transformed_score >= minimum_score_transformed:
        transformed_score = minimum_score_transformed
    return transformed_score


class percolator_2_08( ursgal.UNode ):
    """
    Percolator 2_08 UNode

    q-value and posterior error probability calculation
    by a semi-supervised learning algorithm that dynamically
    learns to separate target from decoy peptide-spectrum matches (PSMs)

    Reference:
    Käll L, Canterbury JD, Weston J, Noble WS, MacCoss MJ. (2007) Semi-supervised learning for peptide identification from shotgun proteomics datasets.
    """
    def __init__(self, *args, **kwargs):
        super(percolator_2_08, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formating the command line to via self.params
        '''

        self.params['csv_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['file_root'] + '.csv'
        )

        self.params['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        # this file will contain the decoys only (we need it for fdr calculations and such)
        self.params['decoy_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            "decoysOnly_" + self.params['output_file']
        )

        self.params['percolator_in'] = \
            '{output_file_incl_path}.tsv'.format(
                **self.params
        )

        self.params['percolator_out'] = \
            '{output_file_incl_path}.psms'.format(**self.params)

        # writing the Percolator input file (tab separated format)
        o = open( self.params['percolator_in'], 'w')
        writer = csv.DictWriter(
            o,
            list(self._kb.PERCOLATOR_FIELDS.keys()),
            delimiter='\t'
        )
        writer.writeheader()

        self.params['percolator_decoy_out'] = \
            '{decoy_output_file_incl_path}.psms'.format(**self.params)
        self.params['command_list'] = [
            # percolator -X pout.xml pin.tab >| yeast-01.psms
            self.exe,
            '--only-psms',
            '{percolator_in}'.format(**self.params),
            '--results-psms',
            '{percolator_out}'.format(**self.params),
            '--decoy-results-psms',
            '{percolator_decoy_out}'.format(**self.params)
        ]

        last_search_engine = self.get_last_search_engine(
            history = self.stats['history']
        )
        self.params['_score_list'] = self.generating_score_list()
        minimum_score = None
        if self.params['bigger_scores_better'] is False:
            for p, _score in enumerate(self.params['_score_list']):
                if _score <= 0:
                    # jumping over truely zero or negative values ...
                    continue
                else:
                    s = -1 * math.log( _score, 10 )
                    if minimum_score is None:
                        minimum_score = _score
                # OMSSA HACK OMG PLEASE HELP US ALL
                if "OMSSA" in last_search_engine.upper():
                    fo = transform_score(_score, minimum_score)
                    if fo < 100:
                        minimum_score = _score
                        break
                else:
                    break

        for n, spectrum_title in enumerate( self.params['grouped_psms'].keys()):
            best_score = self.params['grouped_psms'][ spectrum_title ][0][0]
            worst_score = self.params['grouped_psms'][ spectrum_title ][ -1 ][0]
                        
            if self.params['bigger_scores_better'] is False:
                best_score = transform_score(best_score, minimum_score)
                worst_score = transform_score(worst_score, minimum_score)

            for m, (score, line_dict) in enumerate(
                    self.params['grouped_psms'][ spectrum_title ]):
                t = {}
                if self.params['bigger_scores_better'] is True:
                    rank_of_score = bisect.bisect_right(
                        self.params['_score_list'],
                        score
                    )
                else:
                    rank_of_score = bisect.bisect_left(
                        self.params['_score_list'],
                        score
                    )
                    rank_of_score = len( self.params['_score_list'] ) - rank_of_score
                #
                # t['lnrSp'] = math.log( 1 + rank_of_score )
                # t['Sp'] = rank_of_score
                #
          
                charge      = float(line_dict['Charge'])
                exp_mz      = float(line_dict['Exp m/z'])
                t['Mass']   = ( exp_mz * charge ) - ( charge - 1 ) * PROTON
                #
                t['Xcorr'] = score
                if self.params['bigger_scores_better'] is False:
                    t['Xcorr'] = transform_score(t['Xcorr'], minimum_score)

                t['PepLen'] = len( line_dict['Sequence'] )
                t['Charge{Charge}'.format(**line_dict)] = 1

                normalization = t['Xcorr']
                if t['Xcorr'] < 1:
                    normalization = 1
                if m == len( self.params['grouped_psms'][ spectrum_title ] ) - 1:
                    # last entry
                    deltLCn = 0
                    deltCn = 0
                else:
                    deltLCn = (t['Xcorr'] - worst_score) / normalization
                    next_score = self.params['grouped_psms'][ spectrum_title ][m + 1][0]
                    if self.params['bigger_scores_better'] is False:
                        next_score = transform_score(next_score, minimum_score)

                    deltCn = (t['Xcorr'] - next_score ) / normalization
                t['deltCn'] = deltCn
                t['deltLCn'] = deltLCn
                if line_dict['Is decoy'].upper() == 'TRUE':
                    t['Label'] = -1
                else:
                    t['Label'] = 1

                if self.params['decoy_tag'] in line_dict['proteinacc_start_stop_pre_post_;']:
                    # bug mzIdentML msgf+ convert
                    t['Label'] = -1

                # this - is - sparta (or, if you like mzIdentML) ...
                splitted = line_dict['proteinacc_start_stop_pre_post_;'].split('_')
                # aka http://imgur.com/WjiX9
                pre_aa = splitted[-2]
                post_aa = splitted[-1]
                if pre_aa in ['R', 'K', '-']:
                    t['enzN'] = 1
                else:
                    t['enzN'] = 0
                if line_dict['Sequence'][-1] in ['R', 'K'] or post_aa == '-':
                    t['enzC'] = 1
                else:
                    t['enzC'] = 0
                t['enzInt'] = 0
                for aa in line_dict['Sequence'][:-1]:
                    if aa in ['R', 'K']:
                        t['enzInt'] += 1

                t['dM'] = float(line_dict['Calc m/z']) - float(line_dict['Exp m/z'])
                t['absdM'] = abs(t['dM'])

                mods = line_dict['Modifications']
                t['Peptide'] = '{0}.{Sequence}#{1}.{2}'.format(
                    pre_aa,
                    mods,
                    post_aa,
                    **line_dict
                )
                for per_key in self._kb.PERCOLATOR_FIELDS.keys():
                    mapped_key = self._kb.PERCOLATOR_FIELDS[ per_key ]['csv_field']
                    if 'Charge' in per_key:
                        if per_key not in t.keys():
                            t[ per_key ] = 0
                    if mapped_key != '':
                        t[ per_key ] = line_dict[ mapped_key ]
                writer.writerow( t )
        o.close()


        # marking temporary files for deletion:
        self.created_tmp_files += [
            self.params['decoy_output_file_incl_path'],
            self.params['percolator_in'],
            '{output_file_incl_path}.psms'.format( **self.params ),
            '{output_file_incl_path}.peptides'.format( **self.params ),
        ]


    def postflight( self ):
        '''
        read the output and merge in back to the ident csv
        '''

        potential_buggy_percolator_output = self.params['percolator_out'] + '.psms'
        if os.path.exists( potential_buggy_percolator_output ):
            print('WTF Percolator ?')
            print('Renaming: \n{percolator_out}.psms ->> {percolator_out}'.format(
                **self.params
            ))
            os.rename(
                self.params['output_file_incl_path'] + '.psms.psms',
                self.params['output_file_incl_path'] + '.psms'
            )
            os.rename(
                self.params['decoy_output_file_incl_path'] + '.psms.psms',
                self.params['decoy_output_file_incl_path'] + '.psms'
            )
            os.rename(
                self.params['output_file_incl_path'] + '.psms.peptides',
                self.params['output_file_incl_path'] + '.peptides'
            )

        s2l = {
            'target': ddict(list),
            'decoy' : ddict(list)
        }
        for pkey, p_out in [('target','percolator_out'), ('decoy','percolator_decoy_out')]:

            percolator_output_dict_reader = csv.DictReader(
                open(
                    self.params[ p_out ],
                    'r'
                ),
                delimiter='\t'
            )
            for line_dict in percolator_output_dict_reader:

                peptide = line_dict['peptide'].split('.')[1]
                psmid_pep_key = (
                    line_dict['PSMId'],
                    peptide,
                )
                if psmid_pep_key not in s2l[ pkey ].keys():
                    s2l[ pkey ][ psmid_pep_key ] = line_dict


        opened_file = open( self.params[ 'csv_input_file' ], 'r' )
        csv_input = csv.DictReader( row for row in opened_file if not row.startswith('#') )

        if "PEP" not in csv_input.fieldnames and "q-value" not in csv_input.fieldnames:
            csv_input.fieldnames += ['PEP', 'q-value']
        csv_kwargs = {}

        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'

        csv_output = csv.DictWriter(
            open( self.params['output_file_incl_path'], 'w' ),
            csv_input.fieldnames,
            **csv_kwargs
        )

        csv_output.writeheader()
        for line_dict in csv_input:

            # check if the current line is a decoy or a target
            # so we know in which percolator output file we have to look for it.
            psm_type = "target"
            if line_dict['Is decoy'].upper() == 'TRUE':
                psm_type = "decoy"
            if self.params['decoy_tag'] in line_dict['proteinacc_start_stop_pre_post_;']:
                line_dict['Is decoy'] = "true"
                psm_type = "decoy"

            seq_and_mods = '#'.join( [line_dict['Sequence'], line_dict['Modifications']] )
            _psmid_pep_key = (
                line_dict['Spectrum Title'],
                seq_and_mods,
            )
            if _psmid_pep_key in s2l[ psm_type ].keys():
                line_dict['PEP']     =  s2l[ psm_type ][ _psmid_pep_key ]['posterior_error_prob']
                line_dict['q-value'] =  s2l[ psm_type ][ _psmid_pep_key ]['q-value']
                # write all results including decoy into the full csv:
                csv_output.writerow( line_dict )
            else:
                print(
                    'WARNING! The key {0} has no entry in s2l dict'.format(
                        _psmid_pep_key
                    )
                )


    def generating_score_list( self ):
        scores = []
        for k, v in self.params['grouped_psms'].items():
            for score, line_dict in v:
                scores.append( score )
        # this will depnd on the scoring scheme ...
        # e.g. OMSSA smaller better - XTandem bigger better
        scores.sort()  # reverse=params['bigger_scores_better'])
        return scores
