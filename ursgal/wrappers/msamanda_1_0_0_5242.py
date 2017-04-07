#!/usr/bin/env python3.4
from .msamanda_1_0_0_5243 import msamanda_1_0_0_5243 as msamanda


class msamanda_1_0_0_5242( msamanda ):
    """
    MSAmanda 1_0_0_5242 UNode

    Import functions from msamanda_1_0_0_5243
    """
    META_INFO = {
        'edit_version'       : 1.00,                                            # flot, inclease number if something is changed (kaz)
        'name'               : 'MSAmanda',                                      # str, Software name (kaz)
        'version'            : '1.0.0.5242',                                    # str, Software version name (kaz)
        'release_date'       : None,                                            # None, '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' (kaz)
        'engine_type' : {
            'search_engine' : True,
        },
        'input_extensions'   : ['.mgf'],                                        # list, extensions (kaz)
        'input_multi_file'   : False,                                           # bool, fill true up if multiple files input is MUST like venn-diagram (kaz)
        'output_extensions'  : ['.csv'],                                        # list, extensions (kaz)
        'create_own_folder'  : True,
        'include_in_git'     : True,
        'cannot_distribute'  : True,
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
