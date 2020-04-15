#!/usr/bin/env python

from .xtandem_sledgehammer import xtandem_sledgehammer as tandem


class xtandem_jackhammer( tandem ):
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'X!Tandem',
        'version'                     : 'Jackhammer',
        'release_date'                : '2013-6-15',
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
                    'zip_md5'        : '00a58b8f04d31daa23afcf8cbd8535ae',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '262376f74f5887f98bfbd09a4e220764',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '3d142db4365c705c83eb5559665a6d76',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem '\
            'mass spectra.',
    }
    pass
