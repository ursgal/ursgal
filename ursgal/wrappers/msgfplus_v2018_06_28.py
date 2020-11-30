#!/usr/bin/env python
import ursgal
import os
import subprocess
from .msgfplus_v2016_09_16 import msgfplus_v2016_09_16 as msgf


class msgfplus_v2018_06_28( msgf ):
    """
    MSGF+ UNode
    Parameter options at https://omics.pnl.gov/software/ms-gf

    Reference:
        Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S,
        Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and
        CID/ETD Pairs of Tandem Mass Spectra: Applications to Database Search.

    Import node for version 2016_09_16

    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'MSGF+',
        'version'                     : 'v2018.06.28',
        'release_date'                : '2018-6-28',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : [
            '.mgf',
            '.mzML',
            '.mzXML',
            '.ms2',
            '.pkl',
            '.dta.txt'
        ],
        'output_extensions'           : ['.mzid', '.mzid.gz'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'utranslation_style'          : 'msgfplus_style_1',
        'distributable'               : True,
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'MSGFPlus.jar',
                    'url'            : 'https://github.com/MSGFPlus/msgfplus/releases/download/v2018.06.28/v20180628.zip',
                    'zip_md5'        : 'c1b35ac5a51fd9b2f3e9f7f16d6e7afc',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, '\
            'Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function '\
            'of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: '\
            'Applications to Database Search.',
    }