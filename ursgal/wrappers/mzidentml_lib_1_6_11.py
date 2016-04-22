#!/usr/bin/env python3.3
from .mzidentml_lib_1_6_10 import mzidentml_lib_1_6_10 as ml


class mzidentml_lib_1_6_11( ml ):
    '''
    MzidLib 1_6_10 UNode

    Import functions from mzidentml_lib_1_6_10
    '''
    META_INFO = {
        'in_development'    : False,
        'engine_type' : {
            'search_engine' : False,
            'converter'     : True
        },
        'output_extension'  : '.csv',
        'output_suffix'     : None,
        'input_types'       : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
        # 'can_gz': True,
        'citation'       : 'Reisinger F, Krishna R, Ghali F, Rios D, '\
            'Hermjakob H, Vizcaino JA, Jones AR. (2012) jmzIdentML API: '\
            'A Java interface to the mzIdentML standard for peptide and '\
            'protein identification data.',
        'include_in_git'            : False,
        'utranslation_style'    : 'mzidentml_style_1',
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'mzidentml-lib-1.6.11.jar',
                    'url'            : '',
                    'zip_md5'        : '77757dc40d2eca87c49899a27c3f14a0',
                    'additional_exe' : [],
                },
            },
        },
    }
    pass
