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
import gzip
import subprocess
from .msgfplus2csv_v2017_07_04 import msgfplus2csv_v2017_07_04 as msgfc


class msgfplus2csv_v1_2_0( msgfc ):
    """
    msgfplus_C_mzid2csv_v1.2.0 UNode
    Parameter options at https://omics.pnl.gov/software/ms-gf

    Reference:
    Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: Applications to Database Search.
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'msgfplus_C_mzid2csv',
        'version'            : 'v1.2.0',
        'release_date'       : '2018-02-01',
        'engine_type' : {
            'converter'     : True
        },
        'input_extensions'   : ['.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'include_in_git'     : False,
        'in_development'     : False,
        'distributable'      : True,
        'utranslation_style' : 'msgfplus_style_1',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'MzidToTsvConverter.exe',
                    'url'     : '',
                    'zip_md5' : 'e6923e1f1726f0056d3e9b8bf31016ca'
                },
            },
        },
        'citation' : \
            'Kim S, Mischerikow N, Bandeira N, Navarro JD, Wich L, '\
            'Mohammed S, Heck AJ, Pevzner PA. (2010) The Generating Function '\
            'of CID, ETD, and CID/ETD Pairs of Tandem Mass Spectra: '\
            'Applications to Database Search.',
    }
