#!/usr/bin/env python

from .myrimatch_2_1_138 import myrimatch_2_1_138 as myri


class myrimatch_2_2_140( myri ):
    """
    Myrimatch UNode

    Import functions from myrimatch_2_1_138
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'Myrimatch',
        'version'                     : '2.2.140',
        'release_date'                : None,
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : ['.mzML'],
        'output_extensions'           : ['.mzid'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'               : True,
        'utranslation_style'          : 'myrimatch_style_1',
        'engine' : {
            'win32' : {
                '64bit' : {
                    'exe'            : 'myrimatch.exe',
                    'url'            : '',
                    'zip_md5'        : '36e6e118ca0a8efda19b2556bd18f41e',
                    'additional_exe' : [],
                },
                # '32bit' : {
                #     'exe'            : 'myrimatch.exe',
                #     'url'            : '',
                #     'zip_md5'        : '59d00d759ae6f9225f42ed72844a9ca2',
                #     'additional_exe' : [],
                # },
            },
        },
        'citation' : \
            'Tabb DL, Fernando CG, Chambers MC. (2007) MyriMatch: highly '\
            'accurate tandem mass spectral peptide identification by '\
            'multivariate hypergeometric analysis.',
    }
    pass
