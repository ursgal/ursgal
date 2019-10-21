#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle

class xtandem2csv_1_0_0( ursgal.UNode ):
    """xtandem2csv_1_0_0 UNode"""
    META_INFO = {
        'edit_version'      : 1.00,
        'name'              : 'xtandem2csv',
        'version'           : '1.0.0',
        'release_date'      : None,
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'  : ['.xml', '.xml.gz'],
        'output_extensions' : ['.csv'],
        'output_suffix'     : None,
        'in_development'    : False,
        'include_in_git'    : True,
        'distributable'      : True,
        'utranslation_style' : 'xtandem2csv_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'xtandem2csv_1_0_0.py',
                },
            },
        },
        'citation' : \
            '',
    }

    def __init__(self, *args, **kwargs):
        super(xtandem2csv_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        XML result files from X!Tandem are converted to CSV

        Input file has to be a .xml

        Creates a .csv file and returns its path

        '''
        print('[ -ENGINE- ] Executing conversion ..')
        # self.time_point(tag = 'execution')
        xtandem2csv_main = self.import_engine_as_python_function()
        # if self.params['output_file'].lower().endswith('.xml') is False:
        #     raise ValueError('Trying to convert a non-xml file')

        output_file = os.path.join(
                self.params['output_dir_path'],
                self.params['output_file']
            )
        input_file  = os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            )

        xtandem2csv_main(
            input_file     = input_file,
            output_file    = output_file,
            decoy_tag      = self.params['translations']['decoy_tag'],
        )

        # self.print_execution_time(tag='execution')
        return output_file
