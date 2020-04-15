#!/usr/bin/env python

from .xtandem_sledgehammer import xtandem_sledgehammer as tandem


class xtandem_cyclone_2010( tandem ):
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'X!Tandem',
        'version'                     : 'Cyclone',
        'release_date'                : '2010-12-1',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : ['.mgf', '.gaml', '.dta', '.pkl', '.mzData', '.mzXML'],
        'output_extensions'           : ['.xml'],
        'create_own_folder'           : True,
        'include_in_git'              : False,
        'in_development'              : False,
        'distributable'               : True,
        'utranslation_style'          : 'xtandem_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'tandem',
                    'url'            : '',
                    'zip_md5'        : '1a7043ab013e18d4f9ce0768e4063609',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '68962495adb049f30ecda2d71338ed47',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : 'cc38f6c02a9edc73481c7282ac3801ab',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem '\
            'mass spectra.',
    }
    pass
