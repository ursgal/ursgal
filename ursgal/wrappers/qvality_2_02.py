#!/usr/bin/env python3.4
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
    Käll L, Storey JD, Noble WS (2009) QVALITY: non-parametric estimation of q-values and posterior error probabilities.
    """

    META_INFO = {
        'engine_type'            : {
            'controller'        : False,
            'converter'         : False,
            'validation_engine' : True,
            'search_engine'     : False,
            'meta_engine'       : False
        },
        'output_extension'          : '.csv',
        'output_suffix'             : 'qvality_validated',
        'input_types'               : ['.csv'],
        'create_own_folder'         : False,
        'citation'   : 'Käll L, Storey JD, Noble WS (2009) QVALITY: '\
            'non-parametric estimation of q-values and posterior error '\
            'probabilities.',
        'include_in_git'            : False,
        'group_psms'                : True,
        'in_development'            : True,
        'engine': {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'qvality',
                    'url'            : '',
                    'zip_md5'        : '4f2c1a6eb697cb66d066047c98c1f114',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'qvality',
                    'url'            : '',
                    'zip_md5'        : '2ddd863add4095b710e6883abbd5efbf',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'qvality.exe',
                    'url'            : '',
                    'zip_md5'        : '45c98d18d99f46578d938362c3302804',
                    'additional_exe' : [],
                },
                '32bit' : {
                    'exe'            : 'qvality.exe',
                    'url'            : '',
                    'zip_md5'        : 'f10aee7feec1340364c64eccc6f75a3c',
                    'additional_exe' : [],
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super(qvality_2_02, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formating the command line to via self.params
        '''
        self.params['tmp_output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self._generate_qvality_input_files()

        self.created_tmp_files += [
            self.params['target']['path'],
            self.params['decoy']['path'],
        ]

        self.params['command_list'] =[
            self.exe,
            '-n','{qvality_number_of_bins}'.format(**self.params), #number of bins
            '-v','{qvality_verbose}'.format(**self.params),#medium verbose
            '-s','{qvality_epsilon_step}'.format(**self.params),#epsilon step #The relative step size used as treshhold before cross validation error is calculated, qvality determines step size automatically when set to 0
            '-c','{qvality_cross_validation}'.format(**self.params),#cross validation, The relative crossvalidation step size used as treshhold before ending the iterations, qvality determines step size automatically when set to 0commandLine: -c
            '-o', '{tmp_output_file_incl_path}'.format(**self.params),
        ]

        if self.params['bigger_scores_better'] == False:
            self.params['command_list'].append('-r') #False: lower scores are better e.g.OMSSA, scores have to be reversed for qvality
        if self.params['validation_generalized']:
            self.params['command_list'].append('-g')  # '-g','False',#Generalized target decoy competition, situations where PSMs known to more frequently be incorrect are mixed in with the correct PSMs
        self.params['command_list'] += [
            self.params['target']['path'],
            self.params['decoy']['path'],
        ]

    def postflight( self ):
        '''
        Parse the qvality output and merge it back into the csv file
        '''
        score_2_pep_and_qvalue_lookup = {}
        with open( self.params['tmp_output_file_incl_path'], 'r' ) as qvio:
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
            open(
                os.path.join(
                    self.params['output_dir_path'],
                    self.params['output_file']
                )
                , 'w' ),
            csv_input.fieldnames + ['PEP','q-value'],
            **csv_kwargs
        )


        csv_output.writeheader()
        for line_dict in csv_input:
            #we skip all decoys
            # if line_dict['Is decoy'].upper() == 'TRUE':
            #     continue
            # if self.params['decoy_tag'] in line_dict['proteinacc_start_stop_pre_post_;']:
            #     continue
            formatted_score = FLOAT_FORMAT_STRING.format(
                float(
                    line_dict[
                        self.params['validation_score_field']
                    ]
                )
            )
            if formatted_score in score_2_pep_and_qvalue_lookup.keys():
                pep, qvalue              = score_2_pep_and_qvalue_lookup[ formatted_score ]
                line_dict['PEP']         = pep
                line_dict['q-value']     = qvalue
                # print(line_dict)
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
                #         exit()



    def _generate_qvality_input_files( self ):
        '''
        creates target and decoy score txt files for qvality
        '''
        crazy_tmp_files = {}
        for tag in [ 'target', 'decoy' ]:
            self.params[tag] = {}
            self.params[tag]['path'] = '{0}_{1}_scores.txt'.format(
                os.path.join(
                    self.params['output_dir_path'],
                    self.params['file_root']
                    ),
                tag,
            )
            crazy_tmp_files[ tag ] = open(self.params[tag]['path'], 'w')
        defline_key = 'proteinacc_start_stop_pre_post_;'
        for spectrum_title, grouped_psm_list in self.params['grouped_psms'].items():
            score_2_write, psm_dict = grouped_psm_list[0]
            if self.params['decoy_tag'] in psm_dict[ defline_key ]:
                tag = 'decoy'
            else:
                tag = 'target'
            if score_2_write < self.params[ 'validation_minimum_score' ]:
                score_2_write = self.params[ 'validation_minimum_score' ]
            print(
                score_2_write,
                file = crazy_tmp_files[ tag ]
            )
        for tag in [ 'target', 'decoy' ]:
            crazy_tmp_files[ tag ].close()
