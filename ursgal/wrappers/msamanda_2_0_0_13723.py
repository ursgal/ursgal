#!/usr/bin/env python3.4
from .msamanda_2_0_0_9695 import msamanda_2_0_0_9695 as msamanda


class msamanda_2_0_0_13723( msamanda ):
    """
    MSAmanda 2_0_0_13723 UNode

    Import functions from msamanda_2_0_0_9695
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MSAmanda',
        'version'            : '2.0.0.13723',
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
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'MSAmanda.exe',
                    'url'     : '',
                    'zip_md5' : '',
                },
            }
        },
        'citation' : \
            'Dorfer V, Pichler P, Stranzl T, Stadlmann J, Taus T, Winkler S, '\
            'Mechtler K. (2014) MS Amanda, a universal identification '\
            'algorithm optimized for high accuracy tandem mass spectra.',
    }
    pass
