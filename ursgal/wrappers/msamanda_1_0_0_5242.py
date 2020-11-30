#!/usr/bin/env python
from .msamanda_1_0_0_5243 import msamanda_1_0_0_5243 as msamanda


class msamanda_1_0_0_5242( msamanda ):
    """
    MSAmanda 1_0_0_5242 UNode

    Import functions from msamanda_1_0_0_5243
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MSAmanda',
        'version'            : '1.0.0.5242',
        'release_date'       : None,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],
        'output_extensions'  : ['.csv'],
        'create_own_folder'  : True,
        'include_in_git'     : None,
        'distributable'  : False,
        'in_development'     : False,
        'utranslation_style' : 'msamanda_style_1',
        'engine' : {
            'win32' : {
                '64bit' : {
                    'exe'            : 'MSAmanda.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Dorfer V, Pichler P, Stranzl T, Stadlmann J, Taus T, Winkler S, '\
            'Mechtler K. (2014) MS Amanda, a universal identification '\
            'algorithm optimized for high accuracy tandem mass spectra.',
    }
    pass
