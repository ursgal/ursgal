#!/usr/bin/env python3.4
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

    Java program to convert resulta to .mzIdentML and .mzIdentML to .csv

    """
    META_INFO = {
        'engine_type' : {
            'search_engine' : False,
            'converter'     : True
        },
        'output_extension'  : '.csv',
        'output_suffix'     : None,
        'input_types'       : ['.xml', '.xml.gz', '.csv', '.mzid', '.mzid.gz'],
        # 'can_gz': True,
        'citation'       : 'Reisinger F, Krishna R, Ghali F, Ríos D, '\
            'Hermjakob H, Vizcaíno JA, Jones AR. (2012) jmzIdentML API: '\
            'A Java interface to the mzIdentML standard for peptide and '\
            'protein identification data.',
        'in_development'            : True,
        'include_in_git'            : False,

        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'mzidentml-lib-1.6.10.jar',
                    'url'            : '',
                    'zip_md5'        : '61451563e924b13eebca24e903340da9',
                    'additional_exe' : [],
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        super(mzidentml_lib_1_6_10, self).__init__(*args, **kwargs)

    def raw2mzid( self, search_engine=None ):
        '''
        Convert raw result files into .mzid result files
        '''
        if self.io['input']['finfo']['is_compressed']:
            self.params['mzidentml_compress'] = True
        else:
            self.params['mzidentml_compress'] = False

        tmp_options = [
            self.exe,
            '-outputFragmentation',
            '{mzidentml_outputFragmentation}'.format(**self.params),
            '-decoyRegex',
            '{decoy_tag}'.format(**self.params),
            '-compress', '{mzidentml_compress}'.format(**self.params),
        ]

        if 'tandem' in search_engine:
            tmp_options += [
                '-databaseFileFormatID', 'MS:1001348',
                'massSpecFileFormatID', 'MS:1001062',
                '-idsStartAtZero', 'false'
            ]
            converter_mode = 'Tandem2mzid'
            self.print_info('Executing xtandem xml to mzid conversion')
        else:
            self.print_info('''
    Do not know how to convert search results from {input_file} to mzid
            '''.format( **self.params ),caller='Warning')
            sys.exit(1)
        tmp_command_list = [
            'java', '-Xmx{java_-Xmx}'.format( **self.params),
            '-jar', self.exe,
            converter_mode,
            os.path.join(
                self.params['input_dir_path'],
                self.params['input_file']
            ),
            self.params['input_fileds'],
        ]

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
        search_engine = self.get_last_search_engine(
            history = self.stats['history']
        )
        if search_engine is None:
            raise TypeError(
                '\nmzidentml_lib UNode: Last search engine was not found in '\
                'history. Can\'t convert results without knowing which '\
                'search engine was used.'
            )

        # self.params['input_file'] = os.path.join(
        #     self.params['output_dir_path'],
        #     self.params['file_root'] + '.mzid'
        # )
        FULL_INPUT_PATH = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        if 'tandem' in search_engine:
            # xtandem uses xml outpur which has first to be converted to .mzid
            self.raw2mzid( search_engine=search_engine)
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
                'java', '-Xmx{java_-Xmx}'.format( **self.params),
                '-jar', self.exe,
                'Mzid2Csv',
                FULL_INPUT_PATH,
                os.path.join(
                    self.params['output_dir_path'],
                    self.params['output_file']
                ),
                '-exportType'    , '{mzidentml_exportType}'.format(**self.params),
                '-verboseOutput' , '{mzidentml_verboseOutput}'.format(**self.params),
                '-compress'      , '{mzidentml_compress}'.format(**self.params),
            ]
        else:
            #OMSSA and MS amanda does not need a conversion
            self.params['command_list'] = []
        return
