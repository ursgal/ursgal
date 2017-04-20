#!/usr/bin/env python3.4

from .xtandem_sledgehammer import xtandem_sledgehammer as tandem


class xtandem_jackhammer( tandem ):
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'X!Tandem',
        'version'                     : 'Jackhammer',
        'release_date'                : '2013-6-15',
        'engine_type' : {
            'search_engine' : True,
        },
        'input_extensions'            : ['.mgf', '.gaml', '.dta', '.pkl', '.mzData', '.mzXML'],
        'input_multi_file'            : False,
        'output_extensions'           : ['.xml'],
        'create_own_folder'           : True,
        'compress_raw_search_results' : True,
        'include_in_git'              : False,
        'in_development'              : False,
        'utranslation_style'          : 'xtandem_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'tandem',
                    'url'            : '',
                    'zip_md5'        : '65a270dd63acca8c29a66cbe1406c9ba',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '4f53c35f9adae43f01106db95fe6419c',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '0241c62699bde4d81995f2b9df56f781',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem '\
            'mass spectra.',
    }
    pass
