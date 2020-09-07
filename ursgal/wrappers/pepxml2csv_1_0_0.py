#!/usr/bin/env python
import ursgal
# import importlib
import os
# import sys
# import pickle

class pepxml2csv_1_0_0( ursgal.UNode ):
    """pepxml2csv_1_0_0 UNode"""
    META_INFO = {
        'edit_version'      : 1.00,
        'name'              : 'pepxml2csv_1_0_0',
        'version'           : '1.0.0',
        'release_date'      : None,
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'  : ['.xml'],
        'output_extensions' : ['.csv'],
        'output_suffix'     : None,
        'in_development'    : False,
        'include_in_git'    : True,
        'distributable'      : True,
        'utranslation_style' : 'pepxml2csv_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'pepxml2csv_1_0_0.py',
                },
            },
        },
        'citation' : \
            '',
    }

    def __init__(self, *args, **kwargs):
        super(pepxml2csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        PEP.XML result files from Comet are converted to CSV

        Input file has to be a .pep.xml

        Creates a .csv file and returns its path

        '''
        print('[ -ENGINE- ] Executing conversion ..')
        comet2csv_main = self.import_engine_as_python_function()

        output_file = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file']
            )
        input_file  = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        comet2csv_main(
            input_file     = input_file,
            output_file    = output_file,
            decoy_tag      = self.params['translations']['decoy_tag'],
        )

        return output_file
