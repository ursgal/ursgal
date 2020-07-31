#!/usr/bin/env python3.4
from .pglyco_db_2_2_0 import pglyco_db_2_2_0 as pglyco


class pglyco_db_2_2_2( pglyco ):
    """
    Unode for pGlyco 2.2.2
    For furhter information see: https://github.com/pFindStudio/pGlyco2

    Note:
        Please download pGlyco 2.2.2 manually from
        https://github.com/pFindStudio/pGlyco2

    Reference:
    Liu MQ, Zeng WF,, Fang P, Cao WQ, Liu C, Yan GQ, Zhang Y, Peng C, Wu JQ,
    Zhang XJ, Tu HJ, Chi H, Sun RX, Cao Y, Dong MQ, Jiang BY, Huang JM, Shen HL,
    Wong CCL, He SM, Yang PY. (2017) pGlyco 2.0 enables precision N-glycoproteomics
    with comprehensive quality control and one-step mass spectrometry
    for intact glycopeptide identification.
    Nat Commun 8(1)
    """
    META_INFO = {
        'edit_version': 1.00,
        'name': 'pGlyco',
        'version': '2.2.2',
        'release_date': '2020-01-02',
        'utranslation_style': 'pglyco_db_style_1',
        'input_extensions': ['.mgf'],
        'output_extensions': ['.csv'],
        'create_own_folder': True,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'protein_database_search_engine': True,
        },
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'pGlycoDB.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Liu MQ, Zeng WF, Fang P, Cao WQ, Liu C, Yan GQ, Zhang Y, Peng C, Wu JQ,'
            'Zhang XJ, Tu HJ, Chi H, Sun RX, Cao Y, Dong MQ, Jiang BY, Huang JM, Shen HL,'
            'Wong CCL, He SM, Yang PY. (2017) pGlyco 2.0 enables precision N-glycoproteomics '
            'with comprehensive quality control and one-step mass spectrometry'
            'for intact glycopeptide identification.'
            'Nat Commun 8(1)'
    }
    pass
