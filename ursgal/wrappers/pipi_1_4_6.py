#!/usr/bin/env python
import ursgal
import os
from collections import defaultdict as ddict
import csv
import itertools
import sys
from .pipi_1_4_5 import pipi_1_4_5 as pipi

class pipi_1_4_6( pipi ):
    """
    Unode for PIPI: PTM-Invariant Peptide Identification
    For furhter information see: http://bioinformatics.ust.hk/pipi.html

    Note:
        Please download and extract PIPI manually from 
        http://bioinformatics.ust.hk/pipi.html

    Reference:
    Yu, F., Li, N., Yu, W. (2016) PIPI: PTM-Invariant Peptide Identification 
    Using Coding Method. J Prot Res 15(12)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'PIPI',
        'version': '1.4.6',
        'release_date': '2018-08-23',
        'utranslation_style': 'pipi_style_1',
        'input_extensions': ['.mgf', '.mzML', '.mzXML'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': True,
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'PIPI-1.4.6.jar',
                    'url': 'http://bioinformatics.ust.hk/pipi.html',
                    'zip_md5' : '21f8ebbb90acd0b6c58fec59d0c4f55b',
                    'additional_exe': [],
                },
            },
        },
        'citation':
        'Yu, F., Li, N., Yu, W. (2016) PIPI: PTM-Invariant '
            'Peptide Identification Using Coding Method. '
            'J Prot Res 15(12)'
    }
