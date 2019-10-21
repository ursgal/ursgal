#!/usr/bin/env python
import ursgal
import os
from collections import defaultdict as ddict
import csv
import sys


class thermo_raw_file_parser_1_1_2(ursgal.UNode):
    """
    Unode for ThermoRawFileParser
    For further information visit
    https://github.com/compomics/ThermoRawFileParser

    Note:
        Please download ThermoRawFileParser manually from
        https://github.com/compomics/ThermoRawFileParser

    Reference:
    Hulstaert N, Sachsenberg T, Walzer M, Barsnes H, Martens L and 
    Perez-Riverol Y (2019) ThermoRawFileParser: modular, scalable and 
    cross-platform RAW file conversion. bioRxiv https://doi.org/10.1101/622852
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'ThermoRawFileParser',
        'version': '1.1.2',
        'release_date': '2019-04-25',
        'utranslation_style': 'thermo_raw_file_parser_style_1',
        'input_extensions': ['.raw'],
        'output_extensions': ['.mzML', '.mgf',],
        'output_suffix': None,
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'converter': True,
        },
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'ThermoRawFileParser.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Hulstaert N, Sachsenberg T, Walzer M, Barsnes H, Martens L and '
            'Perez-Riverol Y (2019) ThermoRawFileParser: modular, scalable and '
            'cross-platform RAW file conversion. bioRxiv https://doi.org/10.1101/622852'
    }

    def __init__(self, *args, **kwargs):
        super(thermo_raw_file_parser_1_1_2, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        '''
        Formatting the command line via self.params

        Returns:
            dict: self.params

        ThermoRawFileParser.exe  usage is (use -option=value for the optional arguments):
          -h, --help                 Prints out the options.
          -i, --input=VALUE          The raw file input.
          -o, --output=VALUE         The output directory.
          -f, --format=VALUE         The output format for the spectra (0 for MGF, 1
                                       for mzML, 2 for indexed mzML, 3 for Parquet, 4
                                       for MGF with profile data excluded)
          -m, --metadata=VALUE       The metadata output format (0 for JSON, 1 for TXT).
          -g, --gzip                 GZip the output file if this flag is specified (
                                       without value).
          -u, --s3_url[=VALUE]       Optional property to write directly the data into
                                       S3 Storage.
          -k, --s3_accesskeyid[=VALUE]
                                     Optional key for the S3 bucket to write the file
                                       output.
          -t, --s3_secretaccesskey[=VALUE]
                                     Optional key for the S3 bucket to write the file
                                       output.
          -n, --s3_bucketName[=VALUE]
                                     S3 bucket name
          -v, --verbose              Enable verbose logging.
          -e, --ignoreInstrumentErrors
                                     Ignore missing properties by the instrument.
        '''
        self.params['translations']['raw_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        # self.created_tmp_files.append(self.param_file_name)

        if sys.platform in ['win32']:
            self.params['command_list'] = []
        else:
            self.params['command_list'] = ['mono']

        self.params['command_list'].extend([
            self.exe,
            '-i={0}'.format(self.params['translations']['raw_input_file']),
            '-o={0}'.format(self.params['output_dir_path']),
            '-f={0}'.format(self.params['translations']['output_file_type']),
        ])

        for flag, value in self.params['translations']['thermo_raw_file_parser_options'].items():
            if value is not None:
                self.params['command_list'].append(
                    '{0}={1}'.format(flag, value)
                )
            else:
                self.params['command_list'].append(
                    '{0}'.format(flag)
                )

        return self.params