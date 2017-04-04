#!/usr/bin/env python3.4

from .xtandem_sledgehammer import xtandem_sledgehammer as tandem


class xtandem_jackhammer( tandem ):
    META_INFO = {
        'edit_version'                : 1.00,                                   # flot, inclease number if something is changed (kaz)
        'name'                        : 'X!Tandem',                             # str, Software name (kaz)
        'version'                     : 'Jackhammer',                           # str, Software version name (kaz)
        'release_date'                : '2013-6-15',                            # None, '%Y-%m-%d' or '%Y-%m-%d %H:%M:%S' (kaz)
        'engine_type' : {
            'search_engine' : True,
        },
        'input_types'                 : ['mgf', 'gaml', 'dta', 'pkl', 'mzData', 'mzXML'], # list, extensions without a dot (kaz)
        'multiple_files'              : False,                                  # bool, fill true up if multiple files input is MUST like venn-diagram (kaz)
        'output_extension'            : ['xml'],                                # list, extensions without a dot (kaz)
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
        'citation'                    : 'Craig R, Beavis RC. (2004) TANDEM: '\
            'matching proteins with tandem mass spectra.',
    }
    pass
