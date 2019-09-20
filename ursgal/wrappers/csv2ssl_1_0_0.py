#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import shutil

class csv2ssl_1_0_0( ursgal.UNode ):
    """csv2ssl_1_0_0 UNode"""

    META_INFO = {
        'edit_version'           : 1.00,
        'name'                   : 'Convert CSV to SSL',
        'version'                : '1.0.0',
        'release_date'           : None,
        'engine_type' : {
            'converter'     : True
        },
        'output_extensions' : ['.ssl'],
        'input_extensions'  : ['.csv'],
        'output_suffix'    : 'converted',
        'in_development'   : False,
        'utranslation_style'    : 'csv2ssl_style_1',
        'include_in_git'   : True,
        'distributable'      : True,
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'csv2ssl_1_0_0.py',
                },
            },
        },
        'citation' : '',
    }


    def __init__(self, *args, **kwargs):
        super(csv2ssl_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Result files (.csv) are converted to spectrum sequence list (.ssl) files.
        These .ssl can be used as input files for BiblioSpec.

        Input file has to be a .csv

        Creates a _converted.csv file and returns its path.
        '''

        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag = 'execution')
        csv2ssl_main = self.import_engine_as_python_function()
        if self.params['input_file'].lower().endswith('.csv') is False:
            raise ValueError('Trying to convert a non-csv file')

        output_file = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file']
            )
        input_file  = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        csv2ssl_main(
            input_file     = input_file,
            output_file    = output_file,
            score_column_name    = self.params['translations']['ssl_score_column_name'],
            score_type           = self.params['translations']['ssl_score_type'],
        )

        self.print_execution_time(tag='execution')
        return output_file
