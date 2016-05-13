#!/usr/bin/env python3.4
from .msamanda_1_0_0_5243 import msamanda_1_0_0_5243 as msamanda


class msamanda_1_0_0_6300( msamanda ):
    """
    MSAmanda 1_0_0_6300 UNode

    Import functions from msamanda_1_0_0_5243
    """
    META_INFO = {
        'engine_type': {
            'search_engine': True,
        },
        'output_extension'          : '.csv',
        'input_types'               : ['.mgf'],
        'create_own_folder'         : True,
        'citation'                  : 'Dorfer V, Pichler P, Stranzl T, '\
            'Stadlmann J, Taus T, Winkler S, Mechtler K. (2014) MS Amanda, '\
            'a universal identification algorithm optimized for high accuracy '\
            'tandem mass spectra.',
        'include_in_git'            : None,
        'cannot_distribute'         : True,
        'in_development'            : False,
        'utranslation_style'        : 'msamanda_style_1',
        'engine': {
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

    }
    pass
