#!/usr/bin/env python
import ursgal
import importlib
import os
import sys
import pickle
import csv
import copy
import re
import pprint
from .msgfplus2csv_v2016_09_16 import msgfplus2csv_v2016_09_16 as msgf2csv


class msgfplus2csv_v2017_01_27( msgf2csv ):
    """
    msgfplus2csv_v2017_01_27 UNode
    Parameter options at https://omics.pnl.gov/software/ms-gf

    Reference:

        Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S,
        Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and
        CID/ETD Pairs  of Tandem Mass Spectra: Applications to Database Search.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'msgfplus2csv',
        'version'            : 'v2017.01.27',
        'release_date'       : '2017-1-27',
        'engine_type' : {
            'converter'     : True
        },
        'input_extensions'   : ['.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'include_in_git'     : False,
        'in_development'     : False,
        'distributable'  : False,
        'utranslation_style' : 'msgfplus_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'MSGFPlus.jar',
                    'url'     : '',
                    'zip_md5' : '',
                },
            },
        },
        'citation' : \
            'Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, '\
            'Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function '\
            'of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: '\
            'Applications to Database Search.',
        'uses_unode' : 'msgfplus_v2017_01_27',
    }
