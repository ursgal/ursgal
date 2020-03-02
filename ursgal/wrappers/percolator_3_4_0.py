#!/usr/bin/env python3
# coding: latin1
import ursgal
from .percolator_3_2_1 import percolator_3_2_1


class percolator_3_4_0(percolator_3_2_1):
    """
    Percolator 3.4.0 UNode

    q-value and posterior error probability calculation
    by a semi-supervised learning algorithm that dynamically
    learns to separate target from decoy peptide-spectrum matches (PSMs)

    Reference:
    Matthew The, Michael J. MacCoss, William S. Noble, Lukas Käll "Fast and Accurate Protein False Discovery Rates on Large-Scale Proteomics Data Sets with Percolator 3.0"

    Noe:
    Please download Percolator corresponding to your OS from: https://github.com/percolator/percolator/releases
    """
    META_INFO = {
        'engine_type': {
            'controller': False,
            'converter': False,
            'validation_engine': True,
            'search_engine': False,
            'meta_engine': False
        },
        'edit_version': 1.00,
        'name': 'percolator',
        'version': '3.4.0',
        'release_date': None,
        'output_extensions': ['.csv'],
        'output_suffix': 'percolator_3_4_0_validated',
        'input_extensions': ['.csv'],
        'create_own_folder': False,
        'citation' : 'Matthew The, Michael J. MacCoss, William S. Noble, Lukas Kall' \
            'Fast and Accurate Protein False Discovery Rates on Large-Scale Proteomics Data Sets with Percolator 3.0',
        'include_in_git': False, # True for now, but upload dat shit later on
        'distributable': False,
        'group_psms': True,
        'in_development': False,
        'utranslation_style': 'percolator_style_1',
        'engine': {
            'darwin': {
                '64bit': {
                    'exe': 'percolator_3_4_0',
                    'url': '',
                    'zip_md5': '',
                    'additional_exe': [],
                },
            },
            'linux': {
                '64bit': {
                    'exe': 'percolator',
                    'url': '',
                    'zip_md5': '',
                    'additional_exe': [],
                },
            },
            'win32': {
                '64bit': {
                    'exe': 'percolator.exe',
                    'url': '',
                    'zip_md5': '',
                    'additional_exe': [],
                },
                '32bit': {
                    'exe': 'percolator.exe',
                    'url': '',
                    'zip_md5': '',
                    'additional_exe': [],
                },
            },
        }
    }

    def __init__(self, *args, **kwargs):
        super(percolator_3_4_0, self).__init__(*args, **kwargs)

