#!/usr/bin/env python
import ursgal
import pprint
import csv
import os
import sys

FLOAT_FORMAT_STRING = '{0:1.1e}'


class qvality_2_02( ursgal.UNode ):
    """
    qvality_2_02 UNode

    q-value and posterior error probability calculation from score distributions

    Reference:
    Kﾃ､ll L, Storey JD, Noble WS (2009) QVALITY: non-parametric estimation of q-values and posterior error probabilities.
    """

    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'QVALITY',
        'version'            : '1.0.0',
        'release_date'       : '2009-4-1',
        'engine_type' : {
            'validation_engine' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : 'qvality_2_02_validated',
        'create_own_folder'  : False,
        'include_in_git'     : False,
        'group_psms'         : True,
        'in_development'     : False,
        'distributable'      : True,
        'utranslation_style' : 'qvality_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'qvality',
                    'url'            : '',
                    'zip_md5'        : 'e578317394afff0cdbc121e0203d128b',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'qvality',
                    'url'            : '',
                    'zip_md5'        : '50455452da7fb4124a6a433ed198c10d',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'qvality.exe',
                    'url'            : '',
                    'zip_md5'        : '2b6bb4edc54b5712e61edb44baba41d5',
                    'additional_exe' : [],
                },
                # '32bit' : {
                #     'exe'            : 'qvality.exe',
                #     'url'            : '',
                #     'zip_md5'        : 'f10aee7feec1340364c64eccc6f75a3c',
                #     'additional_exe' : [],
                # },
            },
        },
        'citation' : \
            'Kall L, Storey JD, Noble WS (2009) QVALITY: non-parametric '\
            'estimation of q-values and posterior error probabilities.',
    }

    def __init__(self, *args, **kwargs):
        super(qvality_2_02, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formating the command line to via self.params
        '''
        self.params['last_engine'] = self.get_last_search_engine( history = self.stats['history'] )

        translations = self.params['translations']['_grouped_by_translated_key']

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        translations['-o']['output_file_incl_path'] = self.params['translations']['output_file_incl_path']

        self._generate_qvality_input_files()

        self.created_tmp_files += [
            self.params['translations']['target']['path'],
            self.params['translations']['decoy']['path'],
        ]

        self.params['command_list'] =[
            self.exe,
        ]

        for translated_key, translation_dict in translations.items():
            if list(translation_dict.values())[0] == None:
                continue
            elif translated_key in ['validation_minimum_score', 'validation_score_field', 'decoy_tag', '-r']:
                continue
            elif len(translation_dict) == 1:
                self.params['command_list'].extend((translated_key, str(list(translation_dict.values())[0])))
            else:
                print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                print(translation_dict)
                sys.exit(1)

        if self.UNODE_UPARAMS['bigger_scores_better']['uvalue_style_translation'][self.params['last_engine']] is False:
            self.params['command_list'].append('-r') #False: lower scores are better e.g.OMSSA, scores have to be reversed for qvality
        self.params['command_list'] += [
            self.params['translations']['target']['path'],
            self.params['translations']['decoy']['path'],
        ]

    def postflight( self ):
        '''
        Parse the qvality output and merge it back into the csv file
        '''
        score_2_pep_and_qvalue_lookup = {}
        with open( self.params['translations']['output_file_incl_path'], 'r' ) as qvio:
            qvio.readline() # header gone ...
            for line in qvio:
                if line.strip() != '':
                    score, pep, qvalue = line.strip().split()
                    # if float(pep) >= self.params['maximum_pep_for_ident_csv']:
                    #     continue
                    formatted_score = FLOAT_FORMAT_STRING.format( float(score) )
                    if formatted_score not in score_2_pep_and_qvalue_lookup.keys():
                        score_2_pep_and_qvalue_lookup[ formatted_score ] = ( pep, qvalue )
                    else:
                        pass
        qvio.close()
        opened_file = open(
            os.path.join(
                self.params['input_dir_path'],
                self.params[ 'input_file' ]
            )
            , 'r' )
        csv_kwargs = {}
        if sys.platform == 'win32':
            csv_kwargs['lineterminator'] = '\n'
        else:
            csv_kwargs['lineterminator'] = '\r\n'

        csv_input = csv.DictReader( row for row in opened_file if not row.startswith('#') )

        csv_output = csv.DictWriter(
            open( self.params['translations']['output_file_incl_path'], 'w' ),
            csv_input.fieldnames + ['PEP','q-value'],
            **csv_kwargs
        )

        csv_output.writeheader()
        for line_dict in csv_input:
            #we skip all decoys ... not anymore, please use the filter functon instead
            # if line_dict['Is decoy'].upper() == 'TRUE':
            #     continue
            # if self.params['decoy_tag'] in line_dict['proteinacc_start_stop_pre_post_;']:
            #     continue
            formatted_score = FLOAT_FORMAT_STRING.format(
                float(
                    line_dict[
                        self.UNODE_UPARAMS['validation_score_field']['uvalue_style_translation'][self.params['last_engine']]
                    ]
                )
            )
            if formatted_score in score_2_pep_and_qvalue_lookup.keys():
                pep, qvalue              = score_2_pep_and_qvalue_lookup[ formatted_score ]
                line_dict['PEP']         = pep
                line_dict['q-value']     = qvalue
                csv_output.writerow( line_dict )
            else:
                pass
                # this code should sover the cases when a score is not found in the
                # lookup but was the best score in the spectrum...
                # use for debugging
                # psm_list = self.params['grouped_psms'][line_dict['Spectrum Title']]
                # for pos, (score_2_compare,psm_dict) in enumerate(psm_list):
                #     formatted_score_2_compare = FLOAT_FORMAT_STRING.format(
                #         score_2_compare
                #     )
                #     if formatted_score == formatted_score_2_compare and pos == 0:
                #         # some checking should be done, at least for debugging
                #         print('WARNING - qvality output scores could not be mapped and score was the best for spectrum!')
                #         print('Scores: ', formatted_score, formatted_score_2_compare )
                #         pprint.pprint( psm_list )
                #         sys.exit(1)



    def _generate_qvality_input_files( self ):
        '''
        creates target and decoy score txt files for qvality
        '''
        crazy_tmp_files = {}
        for tag in [ 'target', 'decoy' ]:
            self.params['translations'][tag] = {}
            self.params['translations'][tag]['path'] = '{0}_{1}_scores.txt'.format(
                os.path.join(
                    self.params['output_dir_path'],
                    self.params['file_root']
                    ),
                tag,
            )
            crazy_tmp_files[ tag ] = open(self.params['translations'][tag]['path'], 'w')
        defline_key = 'Protein ID'
        for spectrum_title, grouped_psm_list in self.params['grouped_psms'].items():
            score_2_write, psm_dict = grouped_psm_list[0]
            if psm_dict[ 'Is decoy'].upper() == 'TRUE':
                tag = 'decoy'
            else:
                tag = 'target'

            min_score = self.UNODE_UPARAMS['validation_minimum_score']['uvalue_style_translation'][self.params['last_engine']]
            if score_2_write < min_score:
                score_2_write = min_score
            print(
                score_2_write,
                file = crazy_tmp_files[ tag ]
            )
        for tag in [ 'target', 'decoy' ]:
            crazy_tmp_files[ tag ].close()
