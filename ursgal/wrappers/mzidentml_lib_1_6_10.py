#!/usr/bin/env python
import ursgal
import sys
import os
import pprint
import subprocess

class mzidentml_lib_1_6_10( ursgal.UNode ):
    """
    MzidLib 1_6_10 UNode

    'Reisinger F, Krishna R, Ghali F, Ríos D, Hermjakob H, Vizcaíno JA, Jones AR. (2012)
    jmzIdentML API: A Java interface to the mzIdentML standard for peptide and protein identification data.'

    Java program to convert results to .mzIdentML and .mzIdentML to .csv

    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MzidLib',
        'version'            : '1.6.10',
        'release_date'       : None,
        'engine_type' : {
            'converter' : True
        },
        'input_extensions'   : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
        'output_extensions'  : ['.csv'],
        'output_suffix'      : None,
        'in_development'     : False,
        'include_in_git'     : False,
        'distributable'      : True,
        'utranslation_style' : 'mzidentml_lib_1_6_10',
        'engine' : {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'mzidentml-lib-1.6.10.jar',
                    'url'            : '',
                    'zip_md5'        : '849e00f50d814d3c44b29466434c2cfb',
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Reisinger F, Krishna R, Ghali F, Rios D, Hermjakob H, '\
            'Vizcaino JA, Jones AR. (2012) jmzIdentML API: A Java interface '\
            'to the mzIdentML standard for peptide and protein identification '\
            'data.',
    }

    def __init__(self, *args, **kwargs):
        super(mzidentml_lib_1_6_10, self).__init__(*args, **kwargs)

    def raw2mzid( self, search_engine=None, translations=None ):
        '''
        Convert raw result files into .mzid result files
        '''
        if self.io['input']['finfo']['is_compressed']:
            self.params['translations']['mzidentml_compress'] = True
        else:
            self.params['translations']['mzidentml_compress'] = False

        if 'tandem' in search_engine:
            tmp_options = [
                '-databaseFileFormatID', 'MS:1001348',
                'massSpecFileFormatID', 'MS:1001062',
                '-idsStartAtZero', 'false'
            ]
            converter_mode = 'Tandem2mzid'
            translations['mzidentml_function']['mzidentml_function'] = converter_mode
            self.print_info('Executing xtandem xml to mzid conversion')
        else:
            self.print_info('''
    Do not know how to convert search results from {input_file} to mzid
            '''.format( **self.params ),caller='Warning')
            sys.exit(1)

        tmp_command_list = [
            'java',
            '-jar',
            self.exe,
        ]

        for translated_key, translation_dict in sorted(translations.items()):
                print(translated_key)
                if translated_key == '-Xmx':
                    self.params[ 'command_list' ].insert(1,'{0}{1}'.format(
                        translated_key,
                        list(translation_dict.values())[0]
                    ))
                elif translated_key == 'mzidentml_function':
                    self.params[ 'command_list' ].insert(4, list(translation_dict.values())[0])
                elif translated_key == 'output_file_incl_path':
                    self.params[ 'command_list' ].insert(6, list(translation_dict.values())[0])
                elif len(translation_dict) == 1:
                    self.params['command_list'].extend((translated_key, str(list(translation_dict.values())[0])))
                else:
                    print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                    print(translation_dict)
                    sys.exit(1)

        tmp_command_list += tmp_options
        proc = subprocess.Popen(
            tmp_command_list,
            stdout=subprocess.PIPE,
        )
        for line in proc.stdout:
            print(line.strip().decode('utf'))
        return

    def preflight( self ):
        '''
        Convert .mzid result files from different search engines
        into .csv result files

        For X!Tandem result files first need to be converted into .mzid
        with raw2mzid
        '''

        translations = self.params['translations']['_grouped_by_translated_key']
        # import pprint
        # pprint.pprint(translations)
        # exit(1)

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        translations['output_file_incl_path']['output_file_incl_path'] = self.params['translations']['output_file_incl_path']

        search_engine = self.get_last_search_engine(
            history = self.stats['history']
        )
        if search_engine is None:
            raise TypeError(
                '\nmzidentml_lib UNode: Last search engine was not found in '\
                'history. Can\'t convert results without knowing which '\
                'search engine was used.'
            )

        FULL_INPUT_PATH = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        if 'tandem' in search_engine:
            # xtandem uses xml output which has first to be converted to .mzid
            self.raw2mzid( search_engine=search_engine, translations=translations)
            run_mz_ident_2_csv = True
        elif 'omssa' in search_engine:
            run_mz_ident_2_csv = False
        elif 'msgf' in search_engine:
            run_mz_ident_2_csv = True
        elif 'myrimatch' in search_engine:
            run_mz_ident_2_csv = True
        elif 'msamanda' in search_engine:
            run_mz_ident_2_csv = False
        else:
            raise Exception("Don't know the search engine that created your file...")

        if run_mz_ident_2_csv:
            assert os.path.exists(FULL_INPUT_PATH), '''
                No mzident file found {0}
            '''.format( FULL_INPUT_PATH )

            self.params[ 'command_list' ] = [
                'java',
                '-jar',
                self.exe,
                FULL_INPUT_PATH,
            ]

            for translated_key, translation_dict in sorted(translations.items()):
                if translated_key == '-Xmx':
                    self.params[ 'command_list' ].insert(1,'{0}{1}'.format(
                        translated_key,
                        list(translation_dict.values())[0]
                    ))
                elif translated_key == 'mzidentml_function':
                    self.params[ 'command_list' ].insert(4, list(translation_dict.values())[0])
                elif translated_key == 'output_file_incl_path':
                    self.params[ 'command_list' ].insert(6, list(translation_dict.values())[0])
                elif len(translation_dict) == 1:
                    self.params['command_list'].extend((translated_key, str(list(translation_dict.values())[0])))
                else:
                    print('The translatd key ', translated_key, ' maps on more than one ukey, but no special rules have been defined')
                    print(translation_dict)
                    exit(1)
            # print( ' '.join(self.params[ 'command_list' ]) )

        else:
            #OMSSA and MS amanda does not need a conversion
            self.params['command_list'] = []
        return
