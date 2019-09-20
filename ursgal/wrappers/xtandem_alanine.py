#!/usr/bin/env python
import ursgal
import os

from .xtandem_vengeance import xtandem_vengeance as xtandem

class xtandem_alanine( xtandem ):
    """
    X!Tandem UNode
    Parameter options at http://www.thegpm.org/TANDEM/api/

    Reference:
    Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem mass spectra.
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'X!Tandem',
        'version'                     : 'ALANINE',
        'release_date'                : '2017-02-01',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : ['.mgf', '.gaml', '.dta', '.pkl', '.mzData', '.mzXML'],
        'output_extensions'           : ['.xml'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'               : False,
        'utranslation_style'          : 'xtandem_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'tandem',
                    'url'            : '',
                    'zip_md5'        : 'f33da624f5bdd2702c60e4dc86e9137c',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '37f087c213dfed3c95e62a865d843fb9',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '78ed3c76271f3596aceea8ea5bc904bc',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem '\
            'mass spectra.',
    }