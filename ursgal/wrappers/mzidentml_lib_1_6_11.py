#!/usr/bin/env python3.3
from .mzidentml_lib_1_6_10 import mzidentml_lib_1_6_10 as ml


class mzidentml_lib_1_6_11( ml ):
    '''
    MzidLib 1_6_11 UNode

    Import functions from mzidentml_lib_1_6_10
    '''
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MzidLib',
        'version'            : '1.6.11',
        'release_date'       : None,
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'   : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'in_development'     : False,
        'include_in_git'     : False,
        'distributable'      : True,
        'utranslation_style' : 'mzidentml_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'mzidentml-lib-1.6.11.jar',
                    'url'            : '',
                    'zip_md5'        : 'dea5903d3586719228ae1227919f6c01',
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
