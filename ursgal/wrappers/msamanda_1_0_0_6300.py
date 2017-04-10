#!/usr/bin/env python3.4
from .msamanda_1_0_0_5243 import msamanda_1_0_0_5243 as msamanda


class msamanda_1_0_0_6300( msamanda ):
    """
    MSAmanda 1_0_0_6300 UNode

    Import functions from msamanda_1_0_0_5243
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MSAmanda',
        'version'            : '1.0.0.6300',
        'release_date'       : None,
        'engine_type' : {
            'search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],
        'input_multi_file'   : False,
        'output_extensions'  : ['.csv'],
        'create_own_folder'  : True,
        'include_in_git'     : None,
        'cannot_distribute'  : True,
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
