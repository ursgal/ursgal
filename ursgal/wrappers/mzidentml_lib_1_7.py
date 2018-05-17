#!/usr/bin/env python3.3
from .mzidentml_lib_1_6_10 import mzidentml_lib_1_6_10 as ml


class mzidentml_lib_1_7( ml ):
    '''
    MzidLib 1_7UNode

    Import functions from mzidentml_lib_1_6_10

    Note:

        Please download and install manually from http://www.proteoannotator.org/?q=installation

    '''
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MzidLib',
        'version'            : '1.7',
        'release_date'       : None,
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'   : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'in_development'     : False,
        'output_suffix'      : None,
        'include_in_git'     : None,
        'distributable'      : False,
        'utranslation_style' : 'mzidentml_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'mzidlib-1.7.jar',
                    'url'            : 'http://www.proteoannotator.org/?q=installation',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Reisinger F, Krishna R, Ghali F, Rios D, Hermjakob H, '\
            'Vizcaino JA, Jones AR. (2012) jmzIdentML API: A Java interface '\
            'to the mzIdentML standard for peptide and protein identification '\
            'data.',
    }
    pass
