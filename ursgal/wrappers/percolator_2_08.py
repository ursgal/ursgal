#!/usr/bin/env python
import ursgal
import math
import csv
import bisect
import os
from collections import defaultdict as ddict
from collections import OrderedDict
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
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'Percolator',
        'version'            : '2.08',
        'release_date'       : None,
        'engine_type' : {
            'validation_engine' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'percolator_2_08_validated',
        'create_own_folder'  : False,
        'include_in_git'     : False,
        'distributable'      : True,
        'group_psms'         : True,
        'in_development'     : False,
        'utranslation_style' : 'percolator_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'percolator_2_08',
                    'url'            : '',
                    'zip_md5'        : '3a5f5433ec3875532e74ef54c96da3ba',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'percolator',
                    'url'            : '',
                    'zip_md5'        : '6213411f3c56684667d56ba1a8b020ae',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'percolator.exe',
                    'url'            : '',
                    'zip_md5'        : '60bc939789ef83e11cde4e75cb4ca9e2',
                    'additional_exe' : [],
                },
                # '32bit' : {
                #     'exe'            : 'percolator.exe',
                #     'url'            : '',
                #     'zip_md5'        : '8b1387860c15d07e938a517ddd2cfffa',
                #     'additional_exe' : [],
                # },
            },
        },
        'citation' : \
            'Käll L, Canterbury JD, Weston J, Noble WS, MacCoss MJ. (2007) '\
            'Semi-supervised learning for peptide identification from shotgun '\
            'proteomics datasets.',
    }

    def __init__(self, *args, **kwargs):
        super(percolator_2_08, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formating the command line to via self.params
        '''

        PERCOLATOR_FIELDS = OrderedDict([
            (
                'SpecId', {
                    'csv_field': 'Spectrum Title',
                    'DefaultDirection': 'DefaultDirection'
                }
            ),
            (
                'Label', {
                    'csv_field': '',
                    'DefaultDirection': '-'
                }
            ),
            (
                'ScanNr', {
                    'csv_field': 'Spectrum ID',
                    'DefaultDirection': '-'
                }
            ),
            (
                'lnrSp', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                'The natural logarithm of the rank of the match based on the Sp score'
                }
            ),
            (
                'deltLCn', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                "The difference between this PSM's XCorr and the XCorr of the last-ranked \
                PSM for this spectrum, divided by this PSM's XCorr or 1, whichever is larger."
                }
            ),
            (
                'deltCn', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                    "The difference between this PSM's XCorr and the XCorr of the next-ranked \
                PSM for this spectrum, divided by this PSM's XCorr or 1, whichever is larger. \
                Note that this definition differs from that of the standard delta Cn reported \
                by SEQUEST・ゑｽｮ"
                        }
            ),
            (
                'Xcorr', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                        "The SEQUEST cross-correlation score"
                        }
            ),
            (
                'Sp', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                "The preliminary SEQUEST score."
                        }
            ),
            (
                'IonFrac', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                "The fraction of b and y ions theoretical ions matched to the spectrum"
                        }
            ),
            (
                'Mass',    {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': \
                "The observed mass [M+H]+"
                        }
            ),
            # (
            #     'PepLen',  {
            #         'csv_field': '',
            #         'DefaultDirection': 0,
            #         'description': \
            #     "The length of the matched peptide, in residues"
            #     }
            # ),
            (
                'Charge1', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge2', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge3', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge4', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge5', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge6', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge7', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge8', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge9', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'Charge10', {
                    'csv_field': '',
                    'DefaultDirection': 0
                }
            ),
            (
                'enzN', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': "Is the peptide preceded by an enzymatic (tryptic) site?"
                }
            ),
            (
                'enzC', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': "Does the peptide have an enzymatic (tryptic) C-terminus?"
                }
            ),
            (
                'enzInt', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': "Number of missed internal enzymatic (tryptic) sites"
                }
            ),
            (
                'lnNumSP', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': "The natural logarithm of the number of database peptides within the \
                    specified precursor range"
                }
            ),
            (
                'dM', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': "The difference between the calculated and observed mass"
                }
            ),
            (
                'absdM', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': "The absolute value of the difference between the calculated and \
                    observed mass"
                }
            ),
            (
                'Peptide', {
                    'csv_field': '',
                    'DefaultDirection': 0,
                    'description': ""
                }
            ),
            (
                'Proteins', {
                    'csv_field': 'Protein ID',
                    'DefaultDirection': 0,
                    'description': ""
                }
            ),
        ])


        self.params['translations']['csv_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        # this file will contain the decoys only (we need it for fdr calculations and such)
        self.params['translations']['decoy_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            "decoysOnly_" + self.params['output_file']
        )

        self.params['translations']['percolator_in'] = \
            '{output_file_incl_path}.tsv'.format(
                **self.params['translations']
        )

        self.params['translations']['percolator_out'] = \
            '{output_file_incl_path}.psms'.format(**self.params['translations'])

        # writing the Percolator input file (tab separated format)
        o = open( self.params['translations']['percolator_in'], 'w')
        writer = csv.DictWriter(
            o,
            list(PERCOLATOR_FIELDS.keys()),
            delimiter='\t',
            extrasaction='ignore'
        )
        writer.writeheader()

        self.params['translations']['percolator_decoy_out'] = \
            '{decoy_output_file_incl_path}.psms'.format(**self.params['translations'])
        self.params['command_list'] = [
            # percolator -X pout.xml pin.tab >| yeast-01.psms
            self.exe,
            '--only-psms',
            '{percolator_in}'.format(**self.params['translations']),
            '--results-psms',
            '{percolator_out}'.format(**self.params['translations']),
            '--decoy-results-psms',
            '{percolator_decoy_out}'.format(**self.params['translations'])
        ]

        last_search_engine = self.get_last_search_engine(
            history = self.stats['history']
        )
        self.params['_score_list'] = self.generating_score_list()
        minimum_score = None

        bigger_scores_better = self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][last_search_engine]

        if bigger_scores_better is False:
            for p, _score in enumerate(self.params['_score_list']):
                if _score <= 0:
                    # jumping over truly zero or negative values ...
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

            if bigger_scores_better is False:
                best_score = transform_score(best_score, minimum_score)
                worst_score = transform_score(worst_score, minimum_score)

            for m, (score, line_dict) in enumerate(
                    self.params['grouped_psms'][ spectrum_title ]):
                t = {}

                if bigger_scores_better is True:
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
                if 'Mascot:Rank' in line_dict.keys():
                    rank_of_score = int(line_dict['Mascot:Rank'])
                    # if best_score <= 5:
                    #     continue
                t['lnrSp'] = math.log( 1 + rank_of_score )
                t['Sp'] = rank_of_score
                #
                charge      = float(line_dict['Charge'])
                exp_mz      = float(line_dict['Exp m/z'])
                t['Mass']   = ( exp_mz * charge ) - ( charge - 1 ) * PROTON
                #
                t['Xcorr'] = score
                if bigger_scores_better is False:
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
                    if bigger_scores_better is False:
                        next_score = transform_score(next_score, minimum_score)

                    deltCn = (t['Xcorr'] - next_score ) / normalization
                t['deltCn'] = deltCn
                t['deltLCn'] = deltLCn
                if line_dict['Is decoy'].upper() == 'TRUE':
                    t['Label'] = -1
                else:
                    t['Label'] = 1

                # if self.params['translations']['decoy_tag'] in line_dict['proteinacc_start_stop_pre_post_;']:
                #     # bug mzIdentML msgf+ convert
                #     t['Label'] = -1

                # this - is - sparta (or, if you like mzIdentML) ...
                # splitted = line_dict['proteinacc_start_stop_pre_post_;'].split('_')
                # aka http://imgur.com/WjiX9
                pre_aa = []
                for prot_pre_aa in line_dict['Sequence Pre AA'].split(self.params['translations']['protein_delimiter']):
                    for p_pre_aa in prot_pre_aa.split(';'):
                        pre_aa.append(p_pre_aa)
                post_aa = []
                for prot_post_aa in line_dict['Sequence Post AA'].split(self.params['translations']['protein_delimiter']):
                    for p_post_aa in prot_post_aa.split(';'):
                        post_aa.append(p_post_aa)
                allowed_aa = set(self.params['translations']['enzyme'].split(';')[0] + '-')
                cleavage_site = self.params['translations']['enzyme'].split(';')[1]
                inhibitor_aa = self.params['translations']['enzyme'].split(';')[2]
                final_pre_aa = pre_aa[0]
                final_post_aa = post_aa[0]
                t['enzN'] = 0
                t['enzC'] = 0
                if cleavage_site == 'C':
                    for i, aa in enumerate(pre_aa):
                        if aa in allowed_aa  \
                            or line_dict['Sequence Start'] in ['1', '2']:
                            t['enzN'] = 1
                            final_pre_aa = aa
                            final_post_aa = post_aa[i]
                        if line_dict['Sequence'][-1] in allowed_aa\
                            or '-' in post_aa:
                            t['enzC'] = 1
                elif cleavage_site == 'N':
                    for i, aa in enumerate(post_aa):
                        if aa in allowed_aa:
                            t['enzC'] = 1
                            final_post_aa = aa
                            final_pre_aa = pre_aa[i]
                        if line_dict['Sequence'][0] in allowed_aa\
                            or line_dict['Sequence Start'] in ['1','2']:
                            t['enzN'] = 1

                t['enzInt'] = 0
                if self.params['translations']['enzyme'] != 'ACDEFGHIKLMNPQRSTVWY;C;':
                    for aa in line_dict['Sequence'][:-1]:
                        if aa in allowed_aa:
                            t['enzInt'] += 1

                t['dM'] = float(line_dict['Calc m/z']) - float(line_dict['Exp m/z'])
                t['absdM'] = abs(t['dM'])

                mods = line_dict['Modifications']
                if mods.strip() == '':
                    t['Peptide'] = '{0}.{Sequence}.{1}'.format(
                        sorted(pre_aa)[0],
                        sorted(post_aa)[0],
                        **line_dict
                    )
                else:
                    t['Peptide'] = '{0}.{Sequence}#{1}.{2}'.format(
                        sorted(pre_aa)[0],
                        mods,
                        sorted(post_aa)[0],
                        **line_dict
                    )
                # although peptides without mod ill have # at their end,
                # mapping further down will still work ...

                for per_key in PERCOLATOR_FIELDS.keys():
                    mapped_key = PERCOLATOR_FIELDS[ per_key ]['csv_field']
                    if 'Charge' in per_key:
                        if per_key not in t.keys():
                            t[ per_key ] = 0
                    if mapped_key != '':
                        t[ per_key ] = line_dict[ mapped_key ].strip()
                writer.writerow( t )
        o.close()


        # marking temporary files for deletion:
        self.created_tmp_files += [
            self.params['translations']['decoy_output_file_incl_path'],
            self.params['translations']['percolator_in'],
            '{output_file_incl_path}.psms'.format( **self.params['translations'] ),
            '{output_file_incl_path}.peptides'.format( **self.params['translations'] ),
        ]


    def postflight( self ):
        '''
        read the output and merge in back to the ident csv
        '''
        percolator_log_file_name  = self.params['translations']['output_file_incl_path'].replace(
            '.csv',
            '_percolator_log.txt'
        )
        percolator_log_file = open(
            percolator_log_file_name,
            'w'
        )
        potential_buggy_percolator_output = self.params['translations']['percolator_out'] + '.psms'
        if os.path.exists( potential_buggy_percolator_output ):
            print('WTF Percolator ?')
            print('Renaming: \n{percolator_out}.psms ->> {percolator_out}'.format(
                **self.params['translations']
            ))
            os.rename(
                self.params['translations']['output_file_incl_path'] + '.psms.psms',
                self.params['translations']['output_file_incl_path'] + '.psms'
            )
            os.rename(
                self.params['translations']['decoy_output_file_incl_path'] + '.psms.psms',
                self.params['translations']['decoy_output_file_incl_path'] + '.psms'
            )
            os.rename(
                self.params['translations']['output_file_incl_path'] + '.psms.peptides',
                self.params['translations']['output_file_incl_path'] + '.peptides'
            )

        s2l = {
            'target': ddict(list),
            'decoy' : ddict(list)
        }
        for pkey, p_out in [('target','percolator_out'), ('decoy','percolator_decoy_out')]:

            percolator_output_dict_reader = csv.DictReader(
                open(
                    self.params['translations'][ p_out ],
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


        opened_file = open( self.params['translations'][ 'csv_input_file' ], 'r' )
        csv_input = csv.DictReader( row for row in opened_file if not row.startswith('#') )

        if "PEP" not in csv_input.fieldnames and "q-value" not in csv_input.fieldnames:
            csv_input.fieldnames += ['PEP', 'q-value']
        csv_kwargs = {}

        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'

        percolator_stats = ddict(int)
        csv_output = csv.DictWriter(
            open( self.params['translations']['output_file_incl_path'], 'w' ),
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
            # if self.params['translations']['decoy_tag'] in line_dict['proteinacc_start_stop_pre_post_;']:
            #     line_dict['Is decoy'] = "true"
            #     psm_type = "decoy"
            if line_dict['Modifications'].strip() != '':
                seq_and_mods = '#'.join( [line_dict['Sequence'], line_dict['Modifications']] )
            else:
                seq_and_mods = line_dict['Sequence']
            _psmid_pep_key = (
                line_dict['Spectrum Title'],
                seq_and_mods,
            )
            if _psmid_pep_key in s2l[ psm_type ].keys():
                line_dict['PEP']     = s2l[ psm_type ][ _psmid_pep_key ]['posterior_error_prob']
                line_dict['q-value'] = s2l[ psm_type ][ _psmid_pep_key ]['q-value']
                # write all results including decoy into the full csv:
                csv_output.writerow( line_dict )
                percolator_stats['PSMs accepted and kept by Percolator'] += 1
            else:
                print(
                    'Original PSM :{0} could not be found in percolator output file, most probably because PSM was filtered by percolator, (multiple peptides to one spectrum match)'.format(
                        _psmid_pep_key
                    ),
                    file = percolator_log_file
                )
                percolator_stats['PSMs filtered and removed by Percolator'] += 1
        for title, count in sorted(percolator_stats.items()):
            self.print_info(
                '{0} : {1}'.format(
                    title,
                    count
                ),
                caller = 'Info'

            )
        self.print_info(
            'Please refer to file {0} for details'.format(percolator_log_file_name),
            caller = 'Info'
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
