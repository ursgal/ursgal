#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle


class upeptide_mapper_1_0_0( ursgal.UNode ):
    """
    upeptide_mapper_1_0_0 UNode

    Note:
        Different converter versions can be used (see parameter
        'peptide_mapper_converter_version') as well as different classes
        inside the converter node (see parameter
        'peptide_mapper_class_version' )

    Available converter classes of upeptide_mapper_1_0_0
        * UPeptideMapper_v3 (default)
        * UPeptideMapper_v4 (no buffering and enhanced speed to v3)
        * UPeptideMapper_v2
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'UpeptideMapper',
        'version'            : '1.0.0',
        'release_date'       : None,
        'engine_type' : {
            'misc_engine'     : True
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'output_suffix'     : 'pmap',
        'include_in_git'    : True,
        'in_development'    : False,
        'distributable'      : True,
        'utranslation_style': 'upeptide_mapper_style_1',
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe' : 'upeptide_mapper_1_0_0.py',
                },
            },
        },
        'citation'          : 'Kremer, L. P. M., Leufken, J., '\
            'Oyunchimeg, P., Schulze, S. & Fufezan, C. (2016) '\
            'Ursgal, Universal Python Module Combining Common Bottom-Up '\
            'Proteomics Tools for Large-Scale Analysis. '\
            'J. Proteome res. 15, 788-794.',
    }

    def __init__(self, *args, **kwargs):
        super(upeptide_mapper_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Peptides from search engine csv file are mapped to the given database(s)

        '''
        print('[ -ENGINE- ] Executing conversion ..')
        upeptide_mapper_main = self.import_engine_as_python_function()
        if self.params['output_file'].lower().endswith('.csv') is False:
            raise ValueError('Trying to use a non-csv file')

        output_file = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        input_file  = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        tmp_files = upeptide_mapper_main(
            input_file      = input_file,
            output_file     = output_file,
            params          = self.params,
        )
        for tmp_file in tmp_files:
            self.created_tmp_files.append(tmp_file)

        return output_file
