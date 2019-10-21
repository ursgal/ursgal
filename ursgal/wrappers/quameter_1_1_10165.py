#!/usr/bin/env python
import ursgal
import os
import pprint
from collections import defaultdict as ddict
import csv
import shutil

class quameter_1_1_10165( ursgal.UNode ):
    """
    QuaMeter unode

    Note:
        Please download and install Quameter manually. It comes with Proteowizard
        Bumbershoot.

    Warning:
        Still in testing phase

    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'QuaMeter',
        'version'                     : '1.1.10165',
        'release_date'                : '2016-11-07',
        'utranslation_style'          : 'quameter_style_1',
        'input_extensions'            : ['.raw', '.mzML'],
        'output_extensions'           : ['.tsv'],
        'create_own_folder'           : False,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'           : False,
        'engine_type'                 : {
            'misc_engine' : True,
        },
        'engine'                      : {
            'linux'    : {
                '64bit' : {
                    'exe'            : 'quameter',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation'                   : \
            'Ma, Z. Q., Polzin, K. O., Dasari, S., Chambers, M. C., Schilling, B., '
            'Gibson, B. W., Tran, B. Q., Vega-Montoto, L., Liebler, D. C., and Tabb, D. L. '
            '(2012) QuaMeter: Multivendor performance metrics for LC-MS/MS proteomics '
            'instrumentation. Anal. Chem. 84, 5845–5850'
    }

    def __init__(self, *args, **kwargs):
        super(quameter_1_1_10165, self).__init__(*args, **kwargs)
        pass

    def write_params_file(self):

        return 

    def preflight( self ):
        '''
        Formatting the command line via self.params

        Returns:
                dict: self.params
        '''

        # pprint.pprint(self.params['translations']['_grouped_by_translated_key'])
        # pprint.pprint(self.params)
        # exit()
        
        self.input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        if self.input_file.lower().endswith('.mzml') or \
            self.input_file.lower().endswith('.raw'):
            self.params['translations']['mzml_input_file'] = self.input_file
        elif self.input_file.lower().endswith('.mgf'):
            self.params['translations']['mzml_input_file'] = \
                self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf( self.input_file )
            self.print_info(
                'QuaMeter can only read RAW or mzML,'
                'thecorresponding mzML file {0} will be used instead.'.format(
                    os.path.abspath(self.params['translations']['mzml_input_file'])
                ),
                caller = "INFO" 
            )
        else:
            raise Exception('QuaMeter input spectrum file must be in mzML or RAW format!')

        self.params[ 'command_list' ] = [
            self.exe,
            self.params['translations']['mzml_input_file'],
            '-MetricsType',
            'idfree'
        ]

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        return self.params

    def postflight(self):
        '''
        Read tsvs and write final output file
        '''
        output_file_2_move = self.params['translations']['mzml_input_file'].replace(
            '.mzML',
            '.qual.tsv'
        )
        shutil.move(
            output_file_2_move,
            self.params['translations']['output_file_incl_path']
        )       
        return
