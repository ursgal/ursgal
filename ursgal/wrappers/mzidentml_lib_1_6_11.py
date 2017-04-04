#!/usr/bin/env python3.3
from .mzidentml_lib_1_6_10 import mzidentml_lib_1_6_10 as ml


class mzidentml_lib_1_6_11( ml ):
    '''
    MzidLib 1_6_11 UNode

    Import functions from mzidentml_lib_1_6_10
    '''
    META_INFO = {
        'edit_version'       : 1.00,                                            # flot, inclease number if something is changed (kaz)
        'name'               : 'MzidLib',                                       # str, Software name (kaz)
        'version'            : '1.6.11',                                        # str, Software version name (kaz)
        'release_date'       : None,                                            # None, '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' (kaz)
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'   : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'], # list, extensions (kaz)
        'input_multi_file'   : False,                                           # bool, fill true up if multiple files input is MUST like venn-diagram (kaz)
        'output_extensions'  : ['.csv'],                                        # list, extensions (kaz)
        'output_suffix'      : None,
        'in_development'     : False,
        # 'can_gz'             : True,
        'include_in_git'     : False,
        'utranslation_style' : 'mzidentml_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'mzidentml-lib-1.6.11.jar',
                    'url'            : '',
                    'zip_md5'        : '77757dc40d2eca87c49899a27c3f14a0',
                    'additional_exe' : [],
                },
            },
        },
        'citation'           : 'Reisinger F, Krishna R, Ghali F, Rios D, '\
            'Hermjakob H, Vizcaino JA, Jones AR. (2012) jmzIdentML API: '\
            'A Java interface to the mzIdentML standard for peptide and '\
            'protein identification data.',
    }
    pass
