#!/usr/bin/env python
from .msamanda_2_0_0_9695 import msamanda_2_0_0_9695 as msamanda


class msamanda_2_0_0_9706( msamanda ):
    """
    MSAmanda 2_0_0_9706 UNode

    Import functions from msamanda_2_0_0_9695
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MSAmanda',
        'version'            : '2.0.0.9706',
        'release_date'       : None,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],
        'output_extensions'  : ['.csv'],
        'create_own_folder'  : True,
        'include_in_git'     : False,
        'distributable'  : False,
        'in_development'     : False,
        'utranslation_style' : 'msamanda_style_1',
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe'            : 'MSAmanda.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
            'darwin' : {
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
