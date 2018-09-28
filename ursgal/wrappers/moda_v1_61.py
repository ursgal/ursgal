#!/usr/bin/env python3.4
from .moda_v1_51 import moda_v1_51 as moda


class moda_v1_61( moda ):
    """
    MODa UNode
    Check http://prix.hanyang.ac.kr/download/moda.jsp for download, new versions and contact information

    Reference:
    Na S, Bandeira N, Paek E. (2012) Fast multi-blind modification search through tandem mass spectrometry.

    Import functions from moda_v1_51
    """
    META_INFO = {
        'edit_version': 1.00,
        'name': 'MODa',
        'version': 'v1.61',
        'release_date': '2018-6-15',
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'input_extensions': ['.mgf', '.pkl', '.dta', '.mzXML'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'utranslation_style': 'moda_style_1',
        'engine': {
            'platform_independent': {
                'arc_independent': {
                    'exe': 'moda_v1.61.jar',
                    'url': '',
                    'zip_md5': '',
                    'additional_exe': [],
                },
            },
        },
        'citation':
        'Na S, Bandeira N, Paek E. (2012) Fast multi-blind modification '
            'search through tandem mass spectrometry.',
    }
    pass
