#!/usr/bin/env python3.4

from .myrimatch_2_1_138 import myrimatch_2_1_138 as myri


class myrimatch_2_2_140( myri ):
    """
    Myrimatch UNode

    Import functions from myrimatch_2_1_138
    """
    META_INFO = {
        'engine_type' : {
            'search_engine' : True,
        },
        'input_types'               : ['.mzML'],
        'output_extension'          : '.mzid',
        'create_own_folder'         : True,
        'compress_raw_search_results' : True,

        'citation'                  : 'Tabb DL, Fernando CG, Chambers MC. '\
            '(2007) MyriMatch: highly accurate tandem mass spectral peptide '\
            'identification by multivariate hypergeometric analysis.',
        'in_development'            : False,
        'include_in_git'            : False,
        'utranslation_style'        : 'myrimatch_style_1',
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'myrimatch.exe',
                    'url'            : '',
                    'zip_md5'        : 'afc021ece562109e753b49333fe75df1',
                    'additional_exe' : [],
                },
                '32bit' : {
                    'exe'            : 'myrimatch.exe',
                    'url'            : '',
                    'zip_md5'        : '59d00d759ae6f9225f42ed72844a9ca2',
                    'additional_exe' : [],
                },
            },
        },
    }
    pass
