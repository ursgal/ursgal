#!/usr/bin/env python3.4
from .pparse_2_0 import pparse_2_0 as pparse


class pparse_2_2_1( pparse ):
    """
    Unode for pParse included in pGlyco 2.2.2
    For further information visit
    http://pfind.ict.ac.cn/software/pParse/#Downloads

    Note:
        Please download pParse manually as part of pGlyco 2.2.2
        https://github.com/pFindStudio/pGlyco2

    Reference:
    Yuan ZF, Liu C, Wang HP, Sun RX, Fu Y, Zhang JF, Wang LH,
    Chi H, Li Y, Xiu LY, Wang WP, He SM (2012)
    pParse: a method for accurate determination of monoisotopic peaks 
    in high-resolution mass spectra. Proteomics 12(2)
    """
    META_INFO = {
        'edit_version': 1.00,
        'name': 'pParse',
        'version': '2.2.1',
        'release_date': '2020-01-02',
        'utranslation_style': 'pparse_style_1',
        'input_extensions': ['.raw'],
        'output_extensions': ['.mgf'],
        'output_suffix' : None,
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'converter': True,
        },
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'pParse.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Yuan ZF, Liu C, Wang HP, Sun RX, Fu Y, Zhang JF, Wang LH,'
            'Chi H, Li Y, Xiu LY, Wang WP, He SM (2012)'
            'pParse: a method for accurate determination of monoisotopic peaks '
            'in high-resolution mass spectra. Proteomics 12(2)'
    }
    pass
