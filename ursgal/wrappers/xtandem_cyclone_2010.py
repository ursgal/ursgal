#!/usr/bin/env python3.4

from .xtandem_sledgehammer import xtandem_sledgehammer as tandem


class xtandem_cyclone_2010( tandem ):
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'X!Tandem',
        'version'                     : 'Cyclone',
        'release_date'                : '2010-12-1',
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
                    'zip_md5'        : 'cfa6c1c966fc39b6fe8f8cceaa3c6f84',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '5803f1bab8f54e46d12d9f6a75734b86',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : 'b60c83e752bf3e4bfbaf42a9f38220f8',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem '\
            'mass spectra.',
    }
    pass
