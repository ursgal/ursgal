#!/usr/bin/env python3.4

from .myrimatch_2_1_138 import myrimatch_2_1_138 as myri


class myrimatch_2_2_140( myri ):
    """
    Myrimatch UNode

    Import functions from myrimatch_2_1_138
    """
    META_INFO = {
        'edit_version'                : 1.00,                                   # flot, inclease number if something is changed (kaz)
        'name'                        : 'Myrimatch',                            # str, Software name (kaz)
        'version'                     : '2.2.140',                              # str, Software version name (kaz)
        'release_date'                : None,                                   # None, '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' (kaz)
        'engine_type' : {
            'search_engine' : True,
        },
        'input_extensions'            : ['.mzML'],                              # list, extensions (kaz)
        'input_multi_file'            : False,                                  # bool, fill true up if multiple files input is MUST like venn-diagram (kaz)
        'output_extensions'           : ['.mzid'],                              # list, extensions (kaz)
        'create_own_folder'           : True,
        'compress_raw_search_results' : True,
        'in_development'              : False,
        'include_in_git'              : True,
        'utranslation_style'          : 'myrimatch_style_1',
        'engine' : {
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
        'citation' : \
            'Tabb DL, Fernando CG, Chambers MC. (2007) MyriMatch: highly '\
            'accurate tandem mass spectral peptide identification by '\
            'multivariate hypergeometric analysis.',
    }
    pass
